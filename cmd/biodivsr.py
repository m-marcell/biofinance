"""
ESG-SR frontier, closed-form solution.
Pedersen, Fitzgibbons & Pomorski (2021), Propositions 2 and 3.

For a target average ESG score s_bar, the solution of Eq. (5)

    max_x  x'mu / sqrt(x'Sigma x)    s.t.  x'1 = 1,  x's = s_bar

is, with c_ab = a' Sigma^{-1} b:

    SR(s_bar) = sqrt( c_mm - (c_sm - s_bar*c_1m)^2 / (c_ss - 2*s_bar*c_1s + s_bar^2*c_11) )   (Eq. 9)
    pi        = (c_1m*s_bar - c_sm) / (c_ss - 2*c_1s*s_bar + c_11*s_bar^2)                    (Eq. 11)
    x  ∝  Sigma^{-1} ( mu + pi*(s - 1*s_bar) )                                                (Eq. 10)

with x rescaled so that x'1 = 1.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd


# ----------------------------------------------------------------------------
# 1. Inputs: turn the two dataframes into (mu, Sigma, s)
# ----------------------------------------------------------------------------
def prepare_inputs(
    prices: pd.DataFrame,
    info: pd.DataFrame,
    esg_col: str = "esg",
    ticker_col: str | None = None,
    rf_annual: float = 0.0,
    periods_per_year: int = 250,
    cov_shrinkage: bool = True,
    zscore_esg: bool = True,
    min_obs: int = 60,
    mu_method: str = "factor",
    esg_in_mu: bool = True,
    extra_chars: pd.DataFrame | None = None,
):
    esg = info.set_index(ticker_col)[esg_col] if ticker_col else info[esg_col]
    esg = esg.astype(float).dropna()
    esg = esg[~esg.index.duplicated(keep="first")]

    rets = prices.sort_index().pct_change(fill_method=None).iloc[1:]
    rets = rets.replace([np.inf, -np.inf], np.nan)
    rets = rets.loc[:, rets.notna().sum() >= min_obs]

    tickers = [t for t in rets.columns if t in esg.index]
    if len(tickers) < 3:
        raise ValueError("Fewer than 3 tickers shared by `prices` and `info`.")
    rets = rets[tickers].dropna(how="any")
    if len(rets) < min_obs:
        raise ValueError(
            f"Only {len(rets)} dates with complete data; reduce the universe."
        )

    excess = rets - rf_annual / periods_per_year
    mu_sample = excess.mean().values * periods_per_year

    if cov_shrinkage:
        try:
            from sklearn.covariance import LedoitWolf

            cov = LedoitWolf().fit(excess.values).covariance_
        except ImportError:
            cov = excess.cov().values
    else:
        cov = excess.cov().values
    Sigma = 0.5 * (cov + cov.T) * periods_per_year

    s = esg.loc[tickers].values.astype(float)
    if zscore_esg:
        s = (s - s.mean()) / s.std(ddof=0)

    if mu_method == "factor":
        cols = [np.ones(len(s))] + (
            [(s - s.mean()) / s.std(ddof=0)] if esg_in_mu else []
        )
        if extra_chars is not None:
            ex = extra_chars.reindex(tickers).astype(float)
            if ex.isna().any().any():
                raise ValueError("`extra_chars` has missing values for some tickers.")
            ex = (ex - ex.mean()) / ex.std(ddof=0)
            cols += [ex[col].values for col in ex.columns]
        mu = factor_model_mu(mu_sample, Sigma, np.column_stack(cols))
    elif mu_method == "sample":
        mu = mu_sample
    else:
        raise ValueError("mu_method must be 'factor' or 'sample'")

    return mu, Sigma, s, tickers


def factor_model_mu(mu_sample, Sigma, X):
    Si_X = np.linalg.solve(Sigma, X)
    EF = np.linalg.solve(X.T @ Si_X, Si_X.T @ mu_sample)
    return X @ EF


# ----------------------------------------------------------------------------
# 2. Closed form
# ----------------------------------------------------------------------------
def _c_terms(mu, Sigma, s):
    mu, s = np.asarray(mu, float), np.asarray(s, float)
    ones = np.ones(len(mu))
    Si_mu = np.linalg.solve(Sigma, mu)
    Si_s = np.linalg.solve(Sigma, s)
    Si_1 = np.linalg.solve(Sigma, ones)
    return {
        "Si_mu": Si_mu,
        "Si_s": Si_s,
        "Si_1": Si_1,
        "mm": mu @ Si_mu,
        "sm": s @ Si_mu,
        "1m": ones @ Si_mu,
        "ss": s @ Si_s,
        "1s": ones @ Si_s,
        "11": ones @ Si_1,
    }


def esg_sr_closed_form(mu, Sigma, s, s_bar, c=None):
    mu, s = np.asarray(mu, float), np.asarray(s, float)
    c = c or _c_terms(mu, Sigma, s)

    den = c["ss"] - 2 * s_bar * c["1s"] + s_bar**2 * c["11"]
    sr = np.sqrt(max(c["mm"] - (c["sm"] - s_bar * c["1m"]) ** 2 / den, 0.0))  # Eq. 9
    pi = (c["1m"] * s_bar - c["sm"]) / den  # Eq. 11

    # Eq. 10 in four-fund form: Sigma^{-1}mu + pi*(Sigma^{-1}s - s_bar*Sigma^{-1}1)
    x_raw = c["Si_mu"] + pi * (c["Si_s"] - s_bar * c["Si_1"])
    net_long = x_raw.sum()
    if net_long <= 0:
        warnings.warn(
            f"s_bar={s_bar:.3f}: the Sharpe-maximising portfolio is net SHORT "
            "(sum of weights <= 0). The paper restricts to x'1 > 0, so the "
            "formula does not apply here. This usually means the average "
            "excess return in your data is negative."
        )
    x = x_raw / net_long

    ret = float(x @ mu)
    vol = float(np.sqrt(x @ Sigma @ x))
    return {
        "sharpe": float(sr),
        "weights": x,
        "ret": ret,
        "vol": vol,
        "sharpe_from_weights": ret / vol,
        "esg": float(x @ s),
        "s_star": float(c["sm"] / c["1m"]),
        "net_long": float(net_long),
    }


def esg_sr_frontier(mu, Sigma, s, tickers=None, s_grid=None, n_points=61):
    mu, s = np.asarray(mu, float), np.asarray(s, float)
    c = _c_terms(mu, Sigma, s)
    if s_grid is None:
        s_star = c["sm"] / c["1m"]
        s_grid = np.linspace(s_star - 3, s_star + 3, n_points)

    rows, W = [], []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # net-short points are flagged in `net_long`
        for sb in s_grid:
            o = esg_sr_closed_form(mu, Sigma, s, sb, c=c)
            rows.append(
                {"s_bar": sb, **{k: o[k] for k in ("sharpe", "ret", "vol", "net_long")}}
            )
            W.append(o["weights"])
    frontier = pd.DataFrame(rows).set_index("s_bar")
    return frontier, pd.DataFrame(W, index=frontier.index, columns=tickers)


# ----------------------------------------------------------------------------
# 5. Mean-variance frontiers (Fig. 1, Panel B)
# ----------------------------------------------------------------------------
def _mv_setup(mu, Sigma, base_rows, base_b):
    B = np.vstack(base_rows)
    b = np.asarray(base_b, float)
    k = len(b)
    coef, *_ = np.linalg.lstsq(B.T, mu, rcond=None)
    if np.linalg.norm(B.T @ coef - mu) <= 1e-8 * max(np.linalg.norm(mu), 1e-300):
        Si_Bt = np.linalg.solve(Sigma, B.T)
        sd_min = float(np.sqrt(b @ np.linalg.inv(B @ Si_Bt) @ b))
        return {"degenerate": True, "m_const": float(coef @ b), "sd_min": sd_min}

    A = np.vstack([B, mu])
    Si_At = np.linalg.solve(Sigma, A.T)
    Ginv = np.linalg.inv(A @ Si_At)
    q2, q1, q0 = Ginv[k, k], float(Ginv[k, :k] @ b), float(b @ Ginv[:k, :k] @ b)
    return {
        "degenerate": False,
        "q": (q2, q1, q0),
        "m_g": -q1 / q2,
        "sd_min": float(np.sqrt(q0 - q1**2 / q2)),
        "u": Si_At @ Ginv[:, :k] @ b,
        "v": Si_At @ Ginv[:, k],  # x(m) = u + m v
    }


def _mv_points(setup, sigma_max, n_points):
    if setup["degenerate"]:
        std = np.linspace(setup["sd_min"], max(sigma_max, setup["sd_min"]), n_points)
        return np.full(n_points, setup["m_const"]), std
    q2, q1, q0 = setup["q"]
    d = np.sqrt(max(sigma_max**2 - setup["sd_min"] ** 2, 0.0) / q2)
    m = np.linspace(setup["m_g"] - d, setup["m_g"] + d, n_points)
    return m, np.sqrt(np.maximum(q2 * m**2 + 2 * q1 * m + q0, 0.0))


def mean_variance_frontiers(mu, Sigma, s, s_bar, rf=0.0, sigma_max=None, n_points=201):
   mu, s = np.asarray(mu, float), np.asarray(s, float)
    ones = np.ones(len(mu))
    c = _c_terms(mu, Sigma, s)

    # --- tangency portfolios (fully invested: weights sum to 1)
    if c["1m"] <= 0:
        warnings.warn(
            "The standard tangency portfolio is net SHORT (1'Sigma^-1 mu <= 0); "
            "the average excess return in the data is probably negative."
        )
    x_all = c["Si_mu"] / c["1m"]
    tan_all = {
        "ret": rf + float(x_all @ mu),
        "std": float(np.sqrt(x_all @ Sigma @ x_all)),
        "esg": float(x_all @ s),
        "weights": x_all,
    }
    tan_all["sharpe"] = (tan_all["ret"] - rf) / tan_all["std"]

    o = esg_sr_closed_form(mu, Sigma, s, s_bar, c=c)
    tan_s = {
        "ret": rf + o["ret"],
        "std": o["vol"],
        "sharpe": o["sharpe_from_weights"],
        "esg": o["esg"],
        "weights": o["weights"],
    }

    # --- the two frontiers
    st_a = _mv_setup(mu, Sigma, [ones], [1.0])
    st_s = _mv_setup(mu, Sigma, [ones, s], [1.0, s_bar])
    if st_s["degenerate"]:
        warnings.warn(
            "mu is an exact linear combination of 1 and s (e.g. a market + ESG factor model "
            "without further factors): all portfolios with ESG score s_bar have the same "
            "expected return, so the s_bar frontier is a horizontal half-line, not a "
            "hyperbola. Add another return factor (e.g. value/size via `extra_chars`)."
        )
    if sigma_max is None:
        sigma_max = max(3 * tan_all["std"], 2 * st_s["sd_min"])

    m_a, sd_a = _mv_points(st_a, sigma_max, n_points)
    m_s, sd_s = _mv_points(st_s, sigma_max, n_points)

    touch, esg_a = None, np.full(n_points, np.nan)
    if not st_a["degenerate"]:
        u, v = st_a["u"], st_a["v"]
        esg_a = s @ u + m_a * (s @ v)  # ESG score of each all-asset frontier portfolio
        if abs(s @ v) > 1e-12:
            m_t = (s_bar - s @ u) / (
                s @ v
            )  # the one all-asset frontier portfolio with ESG = s_bar
            q2, q1, q0 = st_a["q"]
            touch = {
                "ret": rf + float(m_t),
                "std": float(np.sqrt(q2 * m_t**2 + 2 * q1 * m_t + q0)),
                "esg": float(s_bar),
            }

    gmv = lambda st: {
        "ret": rf + (st["m_const"] if st["degenerate"] else st["m_g"]),
        "std": st["sd_min"],
    }
    return {
        "all_assets": pd.DataFrame({"std": sd_a, "ret": rf + m_a, "esg": esg_a}),
        "esg_s_bar": pd.DataFrame({"std": sd_s, "ret": rf + m_s}),
        "tangency_all": tan_all,
        "tangency_s_bar": tan_s,
        "gmv_all": gmv(st_a),
        "gmv_s_bar": gmv(st_s),
        "touch": touch,
        "degenerate_all": st_a["degenerate"],
        "degenerate_s_bar": st_s["degenerate"],
        "rf": rf,
        "s_bar": s_bar,
    }


def plot_mv_frontiers(res, ax=None):
    """Reproduce Fig. 1, Panel B from the output of `mean_variance_frontiers`."""
    import matplotlib.pyplot as plt

    ax = ax or plt.subplots(figsize=(7.5, 5.5))[1]
    rf, sb = res["rf"], res["s_bar"]
    A, S = res["all_assets"], res["esg_s_bar"]
    ta, ts = res["tangency_all"], res["tangency_s_bar"]
    xmax = max(A["std"].max(), S["std"].max())

    ax.plot(
        A["std"],
        A["ret"],
        color="gray",
        lw=2,
        label="Mean-variance frontier (all assets)",
    )
    ax.plot(
        S["std"],
        S["ret"],
        color="seagreen",
        lw=2,
        label=f"Mean-variance frontier (ESG score = {sb:g})",
    )
    for t, col, ls in ((ta, "gray", ":"), (ts, "seagreen", "--")):
        ax.plot([0, xmax], [rf, rf + t["sharpe"] * xmax], color=col, ls=ls, lw=1.8)
    ax.scatter(
        [ta["std"]],
        [ta["ret"]],
        color="navy",
        zorder=5,
        label="Tangency portfolio (all assets)",
    )
    ax.scatter(
        [ts["std"]],
        [ts["ret"]],
        color="seagreen",
        edgecolor="k",
        zorder=5,
        label=f"Tangency portfolio (ESG score = {sb:g})",
    )
    ax.scatter([0], [rf], color="k", zorder=5)
    r_ex = ta["ret"] - rf
    ax.set_xlim(0, xmax)
    if r_ex > 0:
        ax.set_ylim(rf - 1.0 * r_ex, rf + 3.0 * r_ex)
    ax.set_xlabel("Standard deviation")
    ax.set_ylabel("Expected return" if rf else "Expected excess return")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("Mean-variance frontiers (cf. Fig. 1, Panel B)")
    return ax


# ----------------------------------------------------------------------------
# Self-test on synthetic data
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    n, T = 30, 1500
    tick = [f"S{i:02d}" for i in range(n)]
    mkt = rng.normal(0.0004, 0.01, T)
    esg_raw = rng.normal(5, 2, n)
    rets = (
        mkt[:, None] * rng.uniform(0.6, 1.4, n)
        + rng.normal(0, 0.015, (T, n))
        + 0.0002
        + 0.00005 * (esg_raw - esg_raw.mean())
    )
    prices = pd.DataFrame(
        100 * np.cumprod(1 + rets, axis=0),
        index=pd.bdate_range("2018-01-01", periods=T),
        columns=tick,
    )
    info = pd.DataFrame({"esg": esg_raw}, index=tick)

    mu, Sigma, s, names = prepare_inputs(prices, info, esg_col="esg", rf_annual=0.02)
    o = esg_sr_closed_form(mu, Sigma, s, s_bar=1.0)
    print(f"SR (Eq. 9)           : {o['sharpe']:.6f}")
    print(f"SR from weights      : {o['sharpe_from_weights']:.6f}")
    print(f"sum(w)               : {o['weights'].sum():.6f}   (should be 1)")
    print(f"w's                  : {o['esg']:.6f}   (should be 1.0)")
    print(f"excess return / vol  : {o['ret']:.2%} / {o['vol']:.2%}")
    print(f"s* (tangency ESG)    : {o['s_star']:.3f}")
