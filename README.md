# GFFI - Global Financial Fragility Index

🌍 Real-time financial fragility index based on entropy.

## 🚀 Live Dashboard
[https://udeshkumar152-png.github.io/gffi-website](https://udeshkumar152-png.github.io/gffi-website)

## 📊 Features
- Live GFFI dashboard with 17 countries
- Real-time market analysis
- Crisis prediction (0.921 AUC)
- 24-month early warning system
- Daily blog updates

## 📈 Key Metrics
- **AUC Score**: 0.921 (Beats VIX 0.71)
- **Lead Time**: 24 months before 2008 crisis
- **Coverage**: 17 countries
- **Validation**: 2008, 2020, 2022, 2023 crises

## 🔬 Published Research
This project is based on published research:
[DOI: 10.5281/zenodo.18859370](https://doi.org/10.5281/zenodo.18859370)

## 🛠️ Tech Stack
- HTML5
- CSS3
- JavaScript
- GitHub Pages

## 📝 Daily Updates
GFFI values are updated daily. Check back for:
- Live market fragility scores
- Country-wise analysis
- Risk alerts
- Investment insights

## 📬 Contact
- **Email**: udeshkumar152@gmail.com
- **Location**: Raipur, India

## 📄 License
© 2026 GFFI Analytics. All rights reserved.

## 🌌 Cosmology Testing Pipeline (ESI)
A full pipeline is included at `scripts/esi_cosmology_pipeline.py` for testing:

\[
H^2(z) = H_0^2\left(1 + \alpha\ln(1+z)\right)
\]

It performs:
1. **H(z) fitting** (ESI and \(\Lambda\)CDM)
2. **SN Ia fitting** (ESI and \(\Lambda\)CDM)
3. **MCMC sampling** for \(\alpha\)
4. **Model comparison** using AIC/BIC
5. **Plot generation**

### Input data format
- H(z) CSV columns: `z,H,sigma_H`
- SN Ia CSV columns: `z,mu,sigma_mu`

### Quick start
```bash
python scripts/esi_cosmology_pipeline.py --generate-mock
```

### With your own data
```bash
python scripts/esi_cosmology_pipeline.py \
  --hz-data data/hz_data.csv \
  --sn-data data/snia_data.csv \
  --outdir results/cosmology \
  --mcmc-steps 20000 \
  --mcmc-burn 4000
```

Outputs are written to `results/cosmology/`:
- `fit_summary.json`
- `hz_fit_comparison.png`
- `snia_fit_comparison.png`
- `alpha_posterior.png`
- `model_comparison.png`
