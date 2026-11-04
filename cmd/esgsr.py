"""
ESG-efficient frontier: Pedersen, Fitzgibbons & Pomorski (2021), Section 2.2.

Solves Eq. (5):

    SR(s_bar) = max_x   x'mu / sqrt(x' Sigma x)
                s.t.    x'1 = 1   and   x's = s_bar

for a universe of stocks, given
    - a DataFrame of prices   (DatetimeIndex, one column per ticker)
    - a DataFrame of stock info containing an ESG score per stock
      (one row per ticker).

Main entry points
-----------------
prepare_inputs(...)      -> mu, Sigma, s, tickers   (estimation step)
solve_esg_sr(...)        -> optimal portfolio for ONE target ESG score (Eq. 5, numerical)
esg_sr_closed_form(...)  -> same thing via Propositions 2-3 (analytical, for checking)
esg_sr_frontier(...)     -> the whole frontier over a grid of s_bar
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def prepare_inputs(
    prices: pd.DataFrame,
    info: pd.DataFrame,
    esg_col: str = "esg",
    ticker_col: str | None = None,
    rf_annual: float = 0.0,
    periods_per_year: int = 252,
    cov_shrinkage: bool = False,
    zscore_esg: bool = True,
    min_obs: int = 60,
):
    """
    Estimate annualised expected excess returns (mu), covariance (Sigma) and
    ESG scores (s) for the stocks present in BOTH dataframes.

    Parameters
    ----------
    prices : DataFrame, DatetimeIndex, columns = tickers, values = prices.
    info   : DataFrame with one row per stock. Tickers are either the index
             (ticker_col=None) or the column `ticker_col`.
    esg_col : column in `info` with the ESG score.
    rf_annual : annual risk-free rate (decimal). Eq. 5 uses EXCESS returns.
    periods_per_year : 252 daily, 52 weekly, 12 monthly.
    cov_shrinkage : use Ledoit-Wolf shrinkage (needs scikit-learn); otherwise
                    the plain sample covariance. Recommended when the number of
                    stocks is not << number of observations.
    zscore_esg : cross-sectional z-score of the ESG score, as in Section 4.2
                 of the paper (0 = average stock, 2 = two std. dev. better).
    min_obs : drop stocks with fewer valid return observations than this.

    Returns
    -------
    mu : (n,) ndarray    annualised expected excess returns
    Sigma : (n, n) ndarray annualised covariance matrix of excess returns
    s : (n,) ndarray     ESG scores
    tickers : list[str]  ordering of the three objects above
    """
    # ESG scores indexed by ticker
    esg = info.set_index(ticker_col)[esg_col] if ticker_col else info[esg_col]
    esg = esg.astype(float).dropna()
    esg = esg[~esg.index.duplicated(keep="first")]

    # returns
    prices = prices.sort_index()
    rets = prices.pct_change(fill_method=None).iloc[1:]
    rets = rets.replace([np.inf, -np.inf], np.nan)
    rets = rets.loc[:, rets.notna().sum() >= min_obs]

    tickers = [t for t in rets.columns if t in esg.index]
    if len(tickers) < 3:
        raise ValueError(
            "Fewer than 3 tickers are shared between `prices` columns and "
            "`info`; check ticker naming / `ticker_col`."
        )
    rets = rets[tickers]
    # Covariance needs a rectangular panel: keep dates where every stock has data
    rets = rets.dropna(how="any")
    if len(rets) < min_obs:
        raise ValueError(
            f"Only {len(rets)} dates with complete data for the selected "
            "stocks; reduce the universe or lower `min_obs`."
        )

    excess = rets - rf_annual / periods_per_year

    mu = excess.mean().values * periods_per_year

    if cov_shrinkage:
        try:
            from sklearn.covariance import LedoitWolf

            cov = LedoitWolf().fit(excess.values).covariance_
        except ImportError:
            cov = excess.cov().values
    else:
        cov = excess.cov().values
    Sigma = cov * periods_per_year
    Sigma = 0.5 * (Sigma + Sigma.T)  # enforce symmetry

    s = esg.loc[tickers].values.astype(float)
    if zscore_esg:
        s = (s - s.mean()) / s.std(ddof=0)

    return mu, Sigma, s, tickers


def solve_esg_sr(
    mu: np.ndarray,
    Sigma: np.ndarray,
    s: np.ndarray,
    s_bar: float,
    bounds: list[tuple[float, float]] | tuple[float, float] | None = None,
    x0: np.ndarray | None = None,
    tol: float = 1e-12,
    maxiter: int = 1000,
):
    """
    Maximise the Sharpe ratio subject to x'1 = 1 and x's = s_bar  (Eq. 5).

    Parameters
    ----------
    bounds : None (default) -> long/short, as in the paper's baseline.
             (0, 1)         -> long-only (s_bar must then lie in [min(s), max(s)]).
             list of (lo, hi) per asset for anything else.
    x0     : optional starting weights (useful for warm starts along the frontier).

    Returns
    -------
    dict with keys: 'weights', 'sharpe', 'esg' (achieved x's), 'ret', 'vol',
                    'success', 'message'
    """
    mu = np.asarray(mu, float)
    s = np.asarray(s, float)
    n = len(mu)

    if bounds is not None and isinstance(bounds, tuple):
        bounds = [bounds] * n

    ones = np.ones(n)

    def neg_sr(x):
        return -(x @ mu) / np.sqrt(x @ Sigma @ x)

    def neg_sr_grad(x):
        sd = np.sqrt(x @ Sigma @ x)
        return -(mu / sd - (x @ mu) * (Sigma @ x) / sd**3)

    constraints = [
        {"type": "eq", "fun": lambda x: x.sum() - 1.0, "jac": lambda x: ones},
        {"type": "eq", "fun": lambda x: x @ s - s_bar, "jac": lambda x: s},
    ]

    # Feasible starting point: minimum-norm solution of  A x = b
    if x0 is None:
        A = np.vstack([ones, s])
        b = np.array([1.0, s_bar])
        x0 = np.linalg.pinv(A) @ b
        if bounds is not None:  # clip into the box, then SLSQP repairs feasibility
            lo = np.array([bd[0] for bd in bounds])
            hi = np.array([bd[1] for bd in bounds])
            x0 = np.clip(x0, lo, hi)

    res = minimize(
        neg_sr,
        x0,
        jac=neg_sr_grad,
        bounds=bounds,
        constraints=constraints,
        method="SLSQP",
        options={"ftol": tol, "maxiter": maxiter},
    )

    x = res.x
    return {
        "weights": x,
        "sharpe": -res.fun,
        "esg": float(x @ s),
        "ret": float(x @ mu),
        "vol": float(np.sqrt(x @ Sigma @ x)),
        "success": bool(res.success),
        "message": res.message,
    }


def esg_sr_closed_form(mu, Sigma, s, s_bar):
    """
    Closed form of Eq. (5) when no extra constraints (bounds) are imposed.

    SR(s_bar) = sqrt( c_mm - (c_sm - s_bar c_1m)^2 / (c_ss - 2 s_bar c_1s + s_bar^2 c_11) )
    with c_ab = a' Sigma^{-1} b.   (Proposition 2, Eq. 9)

    Returns dict with 'sharpe', 'weights' (normalised to sum to 1), 's_star'
    (ESG score of the tangency portfolio, where SR is globally maximal).
    """
    mu = np.asarray(mu, float)
    s = np.asarray(s, float)
    ones = np.ones(len(mu))
    Si = np.linalg.inv(Sigma)

    c = lambda a, b: a @ Si @ b
    c_mm, c_sm, c_1m = c(mu, mu), c(s, mu), c(ones, mu)
    c_ss, c_1s, c_11 = c(s, s), c(ones, s), c(ones, ones)

    den = c_ss - 2 * s_bar * c_1s + s_bar**2 * c_11
    sr = np.sqrt(c_mm - (c_sm - s_bar * c_1m) ** 2 / den)

    # Proposition 3 / Eq. (11): x ∝ Sigma^{-1} (mu + pi (s - 1 s_bar))
    pi = (c_1m * s_bar - c_sm) / den
    x = Si @ (mu + pi * (s - ones * s_bar))
    x = x / x.sum()

    return {"sharpe": float(sr), "weights": x, "s_star": float(c_sm / c_1m)}


def esg_sr_frontier(
    mu,
    Sigma,
    s,
    tickers=None,
    s_grid=None,
    n_points: int = 41,
    bounds=None,
):
    """
    Solve Eq. (5) over a grid of target ESG scores (warm-starting each solve
    from the previous one).

    Returns
    -------
    frontier : DataFrame indexed by s_bar with columns
               ['sharpe', 'esg_achieved', 'ret', 'vol', 'success']
    weights  : DataFrame (rows = s_bar, columns = tickers) of optimal weights
    """
    mu, s = np.asarray(mu, float), np.asarray(s, float)
    if s_grid is None:
        if bounds is None:  # long/short: ESG range is unbounded; use a sensible window
            s_grid = np.linspace(-2.0, 4.0, n_points)
        else:  # long-only: feasible range is [min(s), max(s)]
            s_grid = np.linspace(s.min(), s.max(), n_points)

    rows, W, x_prev = [], [], None
    for sb in s_grid:
        out = solve_esg_sr(mu, Sigma, s, sb, bounds=bounds, x0=x_prev)
        x_prev = out["weights"] if out["success"] else None
        rows.append(
            {
                "s_bar": sb,
                "sharpe": out["sharpe"],
                "esg_achieved": out["esg"],
                "ret": out["ret"],
                "vol": out["vol"],
                "success": out["success"],
            }
        )
        W.append(out["weights"])

    frontier = pd.DataFrame(rows).set_index("s_bar")
    weights = pd.DataFrame(W, index=frontier.index, columns=tickers)
    return frontier, weights


# ----------------------------------------------------------------------------
# Example / self-test with synthetic data
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    n, T = 30, 1500
    tick = [f"S{i:02d}" for i in range(n)]

    # synthetic prices (one-factor structure) and ESG scores
    mkt = rng.normal(0.0004, 0.01, T)
    beta = rng.uniform(0.6, 1.4, n)
    esg_raw = rng.normal(5, 2, n)
    drift = 0.0002 + 0.00005 * (esg_raw - esg_raw.mean())
    rets = mkt[:, None] * beta + rng.normal(0, 0.015, (T, n)) + drift
    prices = pd.DataFrame(
        100 * np.cumprod(1 + rets, axis=0),
        index=pd.bdate_range("2018-01-01", periods=T),
        columns=tick,
    )
    info = pd.DataFrame({"esg": esg_raw}, index=tick)

    mu, Sigma, s, names = prepare_inputs(prices, info, esg_col="esg", rf_annual=0.02)

    # one target ESG level, numerical vs analytical
    target = 1.0
    num = solve_esg_sr(mu, Sigma, s, target)
    ana = esg_sr_closed_form(mu, Sigma, s, target)
    print(f"s_bar = {target}")
    print(
        f"  numerical SR : {num['sharpe']:.6f}  (ESG achieved {num['esg']:.4f}, ok={num['success']})"
    )
    print(f"  analytical SR: {ana['sharpe']:.6f}")
    print(
        f"  max |w_num - w_ana| = {np.abs(num['weights'] - ana['weights']).max():.2e}"
    )
    print(f"  tangency-portfolio ESG score s* = {ana['s_star']:.3f}")

    frontier, weights = esg_sr_frontier(mu, Sigma, s, tickers=names)
    print(frontier.round(4).iloc[::5])
