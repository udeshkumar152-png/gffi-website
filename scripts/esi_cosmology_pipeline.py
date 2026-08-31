#!/usr/bin/env python3
"""Full cosmology testing pipeline for the ESI model.

Model:
    H^2(z) = H0^2 * (1 + alpha * ln(1 + z))

Pipeline tasks:
1) Fit H(z) data
2) Fit SN Ia data
3) Run MCMC for alpha
4) Compare with LambdaCDM
5) Generate plots
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

# km/s
C_LIGHT = 299_792.458


@dataclass
class FitResult:
    model: str
    params: Dict[str, float]
    chi2: float
    ndof: int
    aic: float
    bic: float


def hz_esi(z: np.ndarray, h0: float, alpha: float) -> np.ndarray:
    inside = 1.0 + alpha * np.log1p(z)
    if np.any(inside <= 0):
        return np.full_like(z, np.inf, dtype=float)
    return h0 * np.sqrt(inside)


def hz_lcdm(z: np.ndarray, h0: float, omega_m: float) -> np.ndarray:
    if omega_m <= 0 or omega_m >= 1:
        return np.full_like(z, np.inf, dtype=float)
    return h0 * np.sqrt(omega_m * (1 + z) ** 3 + (1 - omega_m))


def mu_from_hubble(z: np.ndarray, h_vals: np.ndarray, m_offset: float = 0.0) -> np.ndarray:
    if np.any(~np.isfinite(h_vals)):
        return np.full_like(z, np.inf, dtype=float)
    z_grid = np.linspace(0.0, np.max(z) * 1.01 + 1e-4, 3000)
    h_grid = np.interp(z_grid, z, np.interp(z, z, h_vals, left=h_vals[0], right=h_vals[-1]))
    # Stable recomputation directly from model is preferred; this utility receives h(z) on z.
    inv_h = 1.0 / np.clip(h_grid, 1e-9, None)
    dc = C_LIGHT * cumulative_trapezoid(inv_h, z_grid, initial=0.0)
    dl = (1 + z_grid) * dc
    mu_grid = 5 * np.log10(np.clip(dl, 1e-9, None)) + 25 + m_offset
    return np.interp(z, z_grid, mu_grid)


def mu_esi(z: np.ndarray, h0: float, alpha: float, m_offset: float = 0.0) -> np.ndarray:
    z_grid = np.linspace(0.0, np.max(z) * 1.01 + 1e-4, 3000)
    h_grid = hz_esi(z_grid, h0, alpha)
    if np.any(~np.isfinite(h_grid)):
        return np.full_like(z, np.inf, dtype=float)
    inv_h = 1.0 / h_grid
    dc = C_LIGHT * cumulative_trapezoid(inv_h, z_grid, initial=0.0)
    dl = (1 + z_grid) * dc
    mu_grid = 5 * np.log10(np.clip(dl, 1e-9, None)) + 25 + m_offset
    return np.interp(z, z_grid, mu_grid)


def mu_lcdm(z: np.ndarray, h0: float, omega_m: float, m_offset: float = 0.0) -> np.ndarray:
    z_grid = np.linspace(0.0, np.max(z) * 1.01 + 1e-4, 3000)
    h_grid = hz_lcdm(z_grid, h0, omega_m)
    if np.any(~np.isfinite(h_grid)):
        return np.full_like(z, np.inf, dtype=float)
    inv_h = 1.0 / h_grid
    dc = C_LIGHT * cumulative_trapezoid(inv_h, z_grid, initial=0.0)
    dl = (1 + z_grid) * dc
    mu_grid = 5 * np.log10(np.clip(dl, 1e-9, None)) + 25 + m_offset
    return np.interp(z, z_grid, mu_grid)


def chi2(data: np.ndarray, model: np.ndarray, sigma: np.ndarray) -> float:
    if np.any(~np.isfinite(model)):
        return np.inf
    return float(np.sum(((data - model) / sigma) ** 2))


def fit_hz_esi(df_hz: pd.DataFrame) -> FitResult:
    z, h_obs, h_err = df_hz["z"].values, df_hz["H"].values, df_hz["sigma_H"].values

    def objective(x: np.ndarray) -> float:
        h0, alpha = x
        if h0 <= 0:
            return np.inf
        return chi2(h_obs, hz_esi(z, h0, alpha), h_err)

    res = minimize(objective, x0=[70.0, 0.1], bounds=[(40, 100), (-2.5, 5.0)])
    k = 2
    n = len(df_hz)
    chi2_min = float(res.fun)
    return FitResult(
        model="ESI",
        params={"H0": float(res.x[0]), "alpha": float(res.x[1])},
        chi2=chi2_min,
        ndof=n - k,
        aic=chi2_min + 2 * k,
        bic=chi2_min + k * np.log(n),
    )


def fit_hz_lcdm(df_hz: pd.DataFrame) -> FitResult:
    z, h_obs, h_err = df_hz["z"].values, df_hz["H"].values, df_hz["sigma_H"].values

    def objective(x: np.ndarray) -> float:
        h0, omega_m = x
        if h0 <= 0:
            return np.inf
        return chi2(h_obs, hz_lcdm(z, h0, omega_m), h_err)

    res = minimize(objective, x0=[70.0, 0.3], bounds=[(40, 100), (0.01, 0.99)])
    k = 2
    n = len(df_hz)
    chi2_min = float(res.fun)
    return FitResult(
        model="LambdaCDM",
        params={"H0": float(res.x[0]), "omega_m": float(res.x[1])},
        chi2=chi2_min,
        ndof=n - k,
        aic=chi2_min + 2 * k,
        bic=chi2_min + k * np.log(n),
    )


def fit_sn_esi(df_sn: pd.DataFrame, h0_fixed: float) -> FitResult:
    z, mu_obs, mu_err = df_sn["z"].values, df_sn["mu"].values, df_sn["sigma_mu"].values

    def objective(x: np.ndarray) -> float:
        alpha, m_offset = x
        mu_model = mu_esi(z, h0_fixed, alpha, m_offset)
        return chi2(mu_obs, mu_model, mu_err)

    res = minimize(objective, x0=[0.1, -19.3], bounds=[(-2.5, 5.0), (-21.0, -17.0)])
    k = 2
    n = len(df_sn)
    chi2_min = float(res.fun)
    return FitResult(
        model="ESI",
        params={"H0": h0_fixed, "alpha": float(res.x[0]), "M": float(res.x[1])},
        chi2=chi2_min,
        ndof=n - k,
        aic=chi2_min + 2 * k,
        bic=chi2_min + k * np.log(n),
    )


def fit_sn_lcdm(df_sn: pd.DataFrame, h0_fixed: float) -> FitResult:
    z, mu_obs, mu_err = df_sn["z"].values, df_sn["mu"].values, df_sn["sigma_mu"].values

    def objective(x: np.ndarray) -> float:
        omega_m, m_offset = x
        mu_model = mu_lcdm(z, h0_fixed, omega_m, m_offset)
        return chi2(mu_obs, mu_model, mu_err)

    res = minimize(objective, x0=[0.3, -19.3], bounds=[(0.01, 0.99), (-21.0, -17.0)])
    k = 2
    n = len(df_sn)
    chi2_min = float(res.fun)
    return FitResult(
        model="LambdaCDM",
        params={"H0": h0_fixed, "omega_m": float(res.x[0]), "M": float(res.x[1])},
        chi2=chi2_min,
        ndof=n - k,
        aic=chi2_min + 2 * k,
        bic=chi2_min + k * np.log(n),
    )


def run_alpha_mcmc(
    df_hz: pd.DataFrame,
    df_sn: pd.DataFrame,
    h0_init: float,
    alpha_init: float,
    m_init: float,
    n_steps: int = 12000,
    burn_in: int = 2000,
    proposal: Tuple[float, float, float] = (0.25, 0.03, 0.05),
) -> np.ndarray:
    z_h, h_obs, h_err = df_hz["z"].values, df_hz["H"].values, df_hz["sigma_H"].values
    z_sn, mu_obs, mu_err = df_sn["z"].values, df_sn["mu"].values, df_sn["sigma_mu"].values

    def log_like(theta: np.ndarray) -> float:
        h0, alpha, m_offset = theta
        if h0 <= 0 or alpha <= -2.5 or alpha >= 5.0 or m_offset <= -21 or m_offset >= -17:
            return -np.inf
        hz_model = hz_esi(z_h, h0, alpha)
        mu_model = mu_esi(z_sn, h0, alpha, m_offset)
        if np.any(~np.isfinite(hz_model)) or np.any(~np.isfinite(mu_model)):
            return -np.inf
        ll_h = -0.5 * np.sum(((h_obs - hz_model) / h_err) ** 2)
        ll_sn = -0.5 * np.sum(((mu_obs - mu_model) / mu_err) ** 2)
        return float(ll_h + ll_sn)

    chain = np.zeros((n_steps, 3), dtype=float)
    theta = np.array([h0_init, alpha_init, m_init], dtype=float)
    cur_ll = log_like(theta)

    for i in range(n_steps):
        trial = theta + np.random.normal(scale=np.array(proposal), size=3)
        trial_ll = log_like(trial)
        if np.log(np.random.rand()) < (trial_ll - cur_ll):
            theta, cur_ll = trial, trial_ll
        chain[i] = theta

    return chain[burn_in:]


def generate_mock_data(hz_path: Path, sn_path: Path, seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    true_h0, true_alpha, true_m = 69.8, 0.35, -19.3

    z_h = np.linspace(0.05, 2.0, 30)
    sigma_h = rng.uniform(3.0, 7.0, size=z_h.size)
    h_true = hz_esi(z_h, true_h0, true_alpha)
    h_obs = h_true + rng.normal(0, sigma_h)
    df_h = pd.DataFrame({"z": z_h, "H": h_obs, "sigma_H": sigma_h})

    z_sn = np.sort(rng.uniform(0.01, 1.7, size=120))
    sigma_mu = rng.uniform(0.08, 0.2, size=z_sn.size)
    mu_true = mu_esi(z_sn, true_h0, true_alpha, true_m)
    mu_obs = mu_true + rng.normal(0, sigma_mu)
    df_sn = pd.DataFrame({"z": z_sn, "mu": mu_obs, "sigma_mu": sigma_mu})

    hz_path.parent.mkdir(parents=True, exist_ok=True)
    sn_path.parent.mkdir(parents=True, exist_ok=True)
    df_h.to_csv(hz_path, index=False)
    df_sn.to_csv(sn_path, index=False)


def make_plots(
    outdir: Path,
    df_hz: pd.DataFrame,
    df_sn: pd.DataFrame,
    hz_fit_esi: FitResult,
    hz_fit_lcdm: FitResult,
    sn_fit_esi: FitResult,
    sn_fit_lcdm: FitResult,
    alpha_samples: np.ndarray,
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    if plt is None:
        print("[WARN] matplotlib is not installed; skipping PNG plot generation.")
        return

    # H(z) fit
    plt.figure(figsize=(8, 5))
    plt.errorbar(df_hz["z"], df_hz["H"], yerr=df_hz["sigma_H"], fmt="o", label="H(z) data", alpha=0.8)
    z_grid = np.linspace(df_hz["z"].min(), df_hz["z"].max(), 400)
    plt.plot(z_grid, hz_esi(z_grid, hz_fit_esi.params["H0"], hz_fit_esi.params["alpha"]), label="ESI", lw=2)
    plt.plot(z_grid, hz_lcdm(z_grid, hz_fit_lcdm.params["H0"], hz_fit_lcdm.params["omega_m"]), label="LambdaCDM", lw=2)
    plt.xlabel("z")
    plt.ylabel("H(z) [km/s/Mpc]")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "hz_fit_comparison.png", dpi=180)
    plt.close()

    # SN Ia fit
    plt.figure(figsize=(8, 5))
    plt.errorbar(df_sn["z"], df_sn["mu"], yerr=df_sn["sigma_mu"], fmt=".", label="SN Ia", alpha=0.6)
    z_sn_grid = np.linspace(df_sn["z"].min(), df_sn["z"].max(), 400)
    mu_esi_line = mu_esi(
        z_sn_grid,
        sn_fit_esi.params["H0"],
        sn_fit_esi.params["alpha"],
        sn_fit_esi.params["M"],
    )
    mu_lcdm_line = mu_lcdm(
        z_sn_grid,
        sn_fit_lcdm.params["H0"],
        sn_fit_lcdm.params["omega_m"],
        sn_fit_lcdm.params["M"],
    )
    plt.plot(z_sn_grid, mu_esi_line, label="ESI", lw=2)
    plt.plot(z_sn_grid, mu_lcdm_line, label="LambdaCDM", lw=2)
    plt.xlabel("z")
    plt.ylabel("Distance modulus $\\mu$")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "snia_fit_comparison.png", dpi=180)
    plt.close()

    # Alpha posterior
    plt.figure(figsize=(7, 5))
    plt.hist(alpha_samples, bins=50, density=True, alpha=0.85)
    p16, p50, p84 = np.percentile(alpha_samples, [16, 50, 84])
    plt.axvline(p50, color="k", ls="--", label=f"median={p50:.3f}")
    plt.axvspan(p16, p84, color="gray", alpha=0.25, label="68% CI")
    plt.xlabel(r"$\\alpha$")
    plt.ylabel("Posterior density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "alpha_posterior.png", dpi=180)
    plt.close()

    # Model comparison
    labels = ["H(z) AIC", "SN AIC", "H(z) BIC", "SN BIC"]
    esi_vals = [hz_fit_esi.aic, sn_fit_esi.aic, hz_fit_esi.bic, sn_fit_esi.bic]
    lcdm_vals = [hz_fit_lcdm.aic, sn_fit_lcdm.aic, hz_fit_lcdm.bic, sn_fit_lcdm.bic]
    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(9, 5))
    plt.bar(x - width / 2, esi_vals, width, label="ESI")
    plt.bar(x + width / 2, lcdm_vals, width, label="LambdaCDM")
    plt.xticks(x, labels, rotation=15)
    plt.ylabel("Information criterion")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "model_comparison.png", dpi=180)
    plt.close()


def load_or_create_data(hz_data: Path, sn_data: Path, generate_mock: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if generate_mock and (not hz_data.exists() or not sn_data.exists()):
        print("[INFO] Creating mock cosmology datasets.")
        generate_mock_data(hz_data, sn_data)

    if not hz_data.exists() or not sn_data.exists():
        raise FileNotFoundError(
            "Missing datasets. Provide --hz-data/--sn-data files or pass --generate-mock."
        )

    df_hz = pd.read_csv(hz_data)
    df_sn = pd.read_csv(sn_data)

    required_hz = {"z", "H", "sigma_H"}
    required_sn = {"z", "mu", "sigma_mu"}
    if not required_hz.issubset(df_hz.columns):
        raise ValueError(f"H(z) CSV must contain columns: {sorted(required_hz)}")
    if not required_sn.issubset(df_sn.columns):
        raise ValueError(f"SN CSV must contain columns: {sorted(required_sn)}")

    return df_hz.sort_values("z"), df_sn.sort_values("z")


def main() -> None:
    parser = argparse.ArgumentParser(description="ESI cosmology testing pipeline")
    parser.add_argument("--hz-data", type=Path, default=Path("data/hz_data.csv"), help="CSV with z,H,sigma_H")
    parser.add_argument("--sn-data", type=Path, default=Path("data/snia_data.csv"), help="CSV with z,mu,sigma_mu")
    parser.add_argument("--outdir", type=Path, default=Path("results/cosmology"), help="Output directory")
    parser.add_argument("--generate-mock", action="store_true", help="Generate mock input data if not present")
    parser.add_argument("--mcmc-steps", type=int, default=12000, help="Total MCMC steps")
    parser.add_argument("--mcmc-burn", type=int, default=2000, help="Burn-in steps")
    args = parser.parse_args()

    df_hz, df_sn = load_or_create_data(args.hz_data, args.sn_data, args.generate_mock)

    hz_fit_esi = fit_hz_esi(df_hz)
    hz_fit_lcdm = fit_hz_lcdm(df_hz)

    sn_fit_esi = fit_sn_esi(df_sn, hz_fit_esi.params["H0"])
    sn_fit_lcdm = fit_sn_lcdm(df_sn, hz_fit_lcdm.params["H0"])

    chain = run_alpha_mcmc(
        df_hz=df_hz,
        df_sn=df_sn,
        h0_init=hz_fit_esi.params["H0"],
        alpha_init=sn_fit_esi.params["alpha"],
        m_init=sn_fit_esi.params["M"],
        n_steps=args.mcmc_steps,
        burn_in=args.mcmc_burn,
    )
    alpha_samples = chain[:, 1]
    p16, p50, p84 = np.percentile(alpha_samples, [16, 50, 84])

    make_plots(
        outdir=args.outdir,
        df_hz=df_hz,
        df_sn=df_sn,
        hz_fit_esi=hz_fit_esi,
        hz_fit_lcdm=hz_fit_lcdm,
        sn_fit_esi=sn_fit_esi,
        sn_fit_lcdm=sn_fit_lcdm,
        alpha_samples=alpha_samples,
    )

    summary = {
        "hz_fit_esi": hz_fit_esi.__dict__,
        "hz_fit_lcdm": hz_fit_lcdm.__dict__,
        "sn_fit_esi": sn_fit_esi.__dict__,
        "sn_fit_lcdm": sn_fit_lcdm.__dict__,
        "alpha_posterior": {
            "p16": float(p16),
            "p50": float(p50),
            "p84": float(p84),
            "mean": float(np.mean(alpha_samples)),
            "std": float(np.std(alpha_samples)),
            "n_samples": int(alpha_samples.size),
        },
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    with open(args.outdir / "fit_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n=== ESI Cosmology Pipeline Complete ===")
    print(json.dumps(summary["alpha_posterior"], indent=2))
    print(f"Saved outputs in: {args.outdir}")


if __name__ == "__main__":
    main()
