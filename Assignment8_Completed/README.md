# Assignment 8 — SOFR OIS Calibration and Hedging Risk

Completed solution to the instructor's five implementation blocks, using the supplied library APIs and market workbook. Open `hw8_sofr_ois_calibration_and_risk.ipynb` for the full calculation, executed tables, derivation, and numerical checks.

## Contents

- `fixedincomelib/yield_curve/valuation_engine.py`: fixed-leg annuity, OIS par rate, and quotient-rule par-rate gradient (2a–2c).
- `fixedincomelib/yield_curve/yield_curve_model.py`: calibration-instrument Jacobian rows (3).
- `fixedincomelib/valuation/utilities.py`: internal-to-market risk transformation via a transposed linear solve (4).
- `hw8_sofr_ois_calibration_and_risk.ipynb`: calibration, repricing, target valuation, all 17 OIS quote risks, hedge notionals, and independent verification.
- `run_assignment.py`: execute and validate the entire notebook in a fresh Python process, then save its real outputs.

## Reproduce

From the repository root, create a virtual environment and install the supplied requirements:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python run_assignment.py
```

Alternatively, run `jupyter notebook` and execute all cells in order. The original template recommends Python 3.11; this submission was executed with Python 3.12. Dependencies used: NumPy 1.26.4, pandas 2.3.1, QuantLib 1.41, SciPy 1.16.1, and openpyxl 3.1.5. Jupyter supplies nbformat and IPython used by the runner.

## Method and units

Quotes are converted from basis points to decimal rates immediately. The valuation date comes from the workbook, not the current date. SOFR uses bootstrap calibration with piecewise-constant left-continuous instantaneous forwards and flat extrapolation. The funding spread stays fixed at zero.

For unsigned fixed and floating PVs F and L, coupon K, and notional N: A = F/(NK), S = L/(NA), and dS = dL/(NA) - (S/F)dF. Each calibration par-rate gradient is a Jacobian row. Solve J.T @ g_market = g_internal; risk display then scales decimal sensitivities by 0.0001.

The target receives 4.5% fixed on USD 1,000,000 for 9Y6M. Each hedge starts as a USD 1,000,000 receive-fixed par OIS. Solve B.T @ weights = -target_risk. Positive signed notionals receive fixed; negative notionals pay fixed. Only the 17 OIS coordinates are hedged, with the funding spread held fixed.

## Results

Valuation date: 2026-10-09. Target PV: **USD -24,829.03**. Maximum repricing error: **5.280e-10 bp**. Maximum analytical-versus-finite-difference risk error: **3.709e-08 USD/bp**. Maximum analytical hedge residual: **5.684e-14 USD/bp**. All assertions passed. `assignment8_results.html` provides a browser-readable copy of the executed notebook.

## Validation

The notebook asserts calibration repricing, near-zero par hedge PVs, the 17-by-17 hedge matrix and 18-by-18 full Jacobian dimensions, pay/receive PV symmetry, analytical hedge cancellation, and agreement with central finite differences. Each of the 17 OIS quotes is bumped by ±0.01 bp and the curve is recalibrated; all trade coupons and hedge weights are held fixed. This also checks the hedged portfolio independently.

This is a first-order hedge. Convexity, changes in funding spread, and changes in curve conventions can leave P&L beyond the hedged OIS first derivatives.

## Upload to GitHub

Unzip the submission and upload the **contents** into your own assignment repository, preserving the folder structure. Replace the matching starter files. Do not upload the ZIP alone: GitHub needs the `.ipynb` and the changed `.py` files to render and run the completed solution. The original workbook, conventions, library, and license are included. The instructor repository requires write permission; use your own fork or course submission repository.
