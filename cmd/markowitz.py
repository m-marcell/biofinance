import numpy as np
import pandas as pd
from scipy.optimize import minimize


def mean_variance_utility(rp, gamma=3.0, periods_per_year=250):
    """U = E[r_p] - (gamma/2) Var[r_p], annualized."""
    return (
        rp.mean() * periods_per_year - 0.5 * gamma * rp.var(ddof=1) * periods_per_year
    )


def optimize_portfolio(prices, utility=mean_variance_utility, n_starts=1, seed=0):
    prices = prices.sort_index()  # oldest -> newest
    rets = prices.pct_change().dropna()

    # Diagnostics for the usual causes of solver failures
    if not np.isfinite(rets.values).all():
        raise ValueError("Returns contain NaN/inf - check for missing or zero prices.")
    if (rets.std() == 0).any():
        raise ValueError(
            f"Constant price column(s): {list(rets.columns[rets.std() == 0])}"
        )
    if np.linalg.matrix_rank(rets.cov().values) < rets.shape[1]:
        print(
            "Warning: covariance matrix is singular (collinear stocks or too few observations)."
        )

    R = rets.values
    n = R.shape[1]

    def expand(x):
        return np.append(x, 1.0 - x.sum())

    def neg_utility(x):
        return -utility(R @ expand(x))

    rng = np.random.default_rng(seed)
    starts = [np.full(n - 1, 1.0 / n)] + [
        rng.normal(1.0 / n, 0.3, n - 1) for _ in range(n_starts - 1)
    ]

    best = None
    for x0 in starts:
        res = minimize(neg_utility, x0, method="BFGS")
        if best is None or res.fun < best.fun:
            best = res

    w = pd.Series(expand(best.x), index=prices.columns, name="weight")
    rp = R @ w.values
    return {
        "weights": w,
        "utility": -best.fun,
        "converged": best.success,
        "annual_return": rp.mean() * 252,
        "annual_vol": rp.std(ddof=1) * np.sqrt(252),
    }
