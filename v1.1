# Create a Streamlit app that computes Longevity Score v1.1 without exposing equations.
# It supports single-patient input and CSV bulk mode, CAC method switch, REM% and MVPA helpers.
# Then zip it for download alongside a README and requirements.

import os, json, math, zipfile, textwrap
from pathlib import Path

base = Path("/mnt/data/lq_widget_streamlit")
base.mkdir(parents=True, exist_ok=True)

app_py = r'''
import math
import pandas as pd
import streamlit as st

APP_TITLE = "Longevity Quotient (LQ) v1.1 — Calculator"
APP_DESC = """
A simple, shareable calculator for the Longevity Quotient (LQ) v1.1.
- **Equal weights** across 20 variables
- **CAC** choice: *ln-based* (default) or *piecewise (0–400)*
- Optional helpers to compute **MVPA** from Oura High/Medium minutes and **REM%** from minutes + TST
- Batch mode: upload a CSV and download results
"""

# Reference parameters (means, SDs, and directions for z->percentile normalization)
REF = {
    "ogtt_2h":      {"M":120.0, "S":35.0, "D":-1},
    "apob":         {"M": 90.0, "S":25.0, "D":-1},
    "vo2max":       {"M": 36.0, "S": 8.0, "D": 1},
    "crp":          {"M":  1.5, "S": 0.8, "D":-1},
    "bmi":          {"M": 26.0, "S": 5.0, "D":-1},
    "packyrs":      {"M":  2.0, "S": 5.0, "D":-1},
    "moca":         {"M": 27.0, "S": 2.0, "D": 1},
    "mvpa":         {"M":150.0, "S":75.0, "D": 1},
    "hrv":          {"M": 35.0, "S":15.0, "D": 1},
    "phq9":         {"M":  4.0, "S": 4.0, "D":-1},
    "alt":          {"M": 25.0, "S":12.0, "D":-1},
    "egfr":         {"M": 95.0, "S":15.0, "D": 1},
    "bmd_t":        {"M": -0.5, "S": 1.0, "D": 1},
    "truage_delta": {"M":  2.0, "S": 5.0, "D":-1},
    "small_hdl":    {"M": 25.0, "S": 5.0, "D": 1},
    "rem_pct":      {"M": 20.0, "S": 5.0, "D": 1},
    "grip":         {"M": 38.0, "S":10.0, "D": 1},
    "swls":         {"M": 24.0, "S": 6.0, "D": 1},
    # rpdqs handled separately
}

VAR_ORDER = [
    "ogtt_2h","apob","vo2max","crp","bmi","packyrs","moca","mvpa","cac",
    "hrv","phq9","alt","egfr","bmd_t","truage_delta","small_hdl","rem_pct",
    "grip","swls","rpdqs"
]

HELP_TEXT = {
    "ogtt_2h": "2-hour Oral Glucose Tolerance Test (mg/dL)",
    "apob": "ApoB (mg/dL)",
    "vo2max": "VO₂max (mL/kg/min)",
    "crp": "CRP (mg/L)",
    "bmi": "Body Mass Index",
    "packyrs": "Pack-years of smoking",
    "moca": "MoCA cognitive assessment (0–30)",
    "mvpa": "Moderate-to-Vigorous Physical Activity (min/week)",
    "cac": "Coronary Artery Calcium score (Agatston)",
    "hrv": "Heart Rate Variability (ms)",
    "phq9": "PHQ-9 (0–27)",
    "alt": "ALT (U/L)",
    "egfr": "eGFR (mL/min/1.73m²)",
    "bmd_t": "Bone Mineral Density T-score",
    "truage_delta": "Epigenetic age delta (years; positive = older than chronological)",
    "small_hdl": "Small HDL particles (μmol/L)",
    "rem_pct": "REM sleep (% of TST)",
    "grip": "Grip strength (kg)",
    "swls": "Satisfaction With Life Scale (5–35)",
    "rpdqs": "Rapid Prime Diet Quality Screener (0–52)"
}

def normal_cdf(z: float) -> float:
    # Standard normal CDF via erf; avoids SciPy dependency
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

def normalize_z(x, key):
    p = REF[key]
    z = p["D"] * ((x - p["M"]) / p["S"])
    return clamp(100.0 * normal_cdf(z))

def normalize_rpdqs(x):
    return clamp((x / 52.0) * 100.0)

def normalize_cac(value, method="ln"):
    if method == "ln":
        # 100*normal( -(ln(cac+1) - ln(100)) )
        return clamp(100.0 * normal_cdf(-(math.log(value + 1.0) - math.log(100.0))))
    else:
        # piecewise 0-400 as in spec
        if value == 0:
            return 100.0
        if value >= 400:
            return 0.0
        if value <= 100:
            return clamp(100.0 - 0.2 * value)
        # 100 < value < 400
        return clamp(50.0 - 0.1 * (value - 100.0))

def compute_single(inputs: dict, cac_method="ln") -> dict:
    # inputs: raw values for all required fields (some optional helpers may fill mvpa and rem_pct)
    # returns: dict with normalized scores, composite, and LQ
    # Validate presence
    missing = [k for k in VAR_ORDER if k not in inputs or inputs[k] is None]
    if missing:
        raise ValueError(f"Missing inputs: {missing}")

    # Per-component normalized (0–100)
    N = {}
    N["ogtt_2h"]      = normalize_z(inputs["ogtt_2h"], "ogtt_2h")
    N["apob"]         = normalize_z(inputs["apob"], "apob")
    N["vo2max"]       = normalize_z(inputs["vo2max"], "vo2max")
    N["crp"]          = normalize_z(inputs["crp"], "crp")
    N["bmi"]          = normalize_z(inputs["bmi"], "bmi")
    N["packyrs"]      = normalize_z(inputs["packyrs"], "packyrs")
    N["moca"]         = normalize_z(inputs["moca"], "moca")
    N["mvpa"]         = normalize_z(inputs["mvpa"], "mvpa")
    N["cac"]          = normalize_cac(inputs["cac"], cac_method)
    N["hrv"]          = normalize_z(inputs["hrv"], "hrv")
    N["phq9"]         = normalize_z(inputs["phq9"], "phq9")
    N["alt"]          = normalize_z(inputs["alt"], "alt")
    N["egfr"]         = normalize_z(inputs["egfr"], "egfr")
    N["bmd_t"]        = normalize_z(inputs["bmd_t"], "bmd_t")
    N["truage_delta"] = normalize_z(inputs["truage_delta"], "truage_delta")
    N["small_hdl"]    = normalize_z(inputs["small_hdl"], "small_hdl")
    N["rem_pct"]      = normalize_z(inputs["rem_pct"], "rem_pct")
    N["grip"]         = normalize_z(inputs["grip"], "grip")
    N["swls"]         = normalize_z(inputs["swls"], "swls")
    N["rpdqs"]        = normalize_rpdqs(inputs["rpdqs"])

    # Composite: equal weights (mean)
    comp = sum(N[v] for v in VAR_ORDER) / 20.0
    LQ = 300.0 + 5.5 * comp
    LQ = max(300.0, min(850.0, LQ))

    out = {"composite": comp, "LQ": LQ}
    # add components with a "N_" prefix
    for k, v in N.items():
        out[f"N_{k}"] = v
    return out

def compute_dataframe(df: pd.DataFrame, cac_method="ln") -> pd.DataFrame:
    rows = []
    for idx, row in df.iterrows():
        d = {k: row[k] for k in VAR_ORDER}
        res = compute_single(d, cac_method)
        rows.append(res)
    res_df = pd.DataFrame(rows, index=df.index)
    return pd.concat([df, res_df], axis=1)

def prefill_example(which="typical"):
    if which=="typical":
        return dict(
            ogtt_2h=152, apob=107, vo2max=34, crp=2, bmi=29.6, packyrs=0, moca=25,
            mvpa=112.5, cac=98, hrv=47, phq9=7, alt=42, egfr=82, bmd_t=-1.2,
            truage_delta=2, small_hdl=10.2, rem_pct=(52/420)*100, grip=38, swls=26, rpdqs=35
        )
    else:
        return dict(
            ogtt_2h=85, apob=60, vo2max=55, crp=0.4, bmi=22.5, packyrs=0, moca=29,
            mvpa=300, cac=0, hrv=75, phq9=0, alt=18, egfr=110, bmd_t=1.0,
            truage_delta=-5, small_hdl=40, rem_pct=(120/420)*100, grip=55, swls=33, rpdqs=48
        )

def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.caption("Version 1.1 — equal weights; © Quotient Health")

    with st.expander("About this app", expanded=False):
        st.markdown(APP_DESC)

    st.sidebar.header("Settings")
    cac_method = st.sidebar.selectbox("CAC method", options=["ln","piecewise"], index=0, help="ln-based matches Stata spec; piecewise approximates 0–400 mapping.")

    mode = st.sidebar.radio("Mode", options=["Single patient","Bulk CSV"], index=0)

    if mode == "Single patient":
        st.subheader("Inputs")
        colA, colB, colC, colD = st.columns(4)

        # Helpers
        use_oura = st.checkbox("Compute MVPA from Oura High/Medium", value=False, help="MVPA = High + 0.5 × Medium (capped at 1000)")
        use_rem  = st.checkbox("Compute REM% from minutes + TST", value=False, help="REM% = 100 × REM_minutes / TST_minutes")

        # Prefill buttons
        col0a, col0b = st.columns([1,1])
        if col0a.button("Prefill: Typical Patient"):
            st.session_state["prefill"] = prefill_example("typical")
        if col0b.button("Prefill: High Performer"):
            st.session_state["prefill"] = prefill_example("high")

        defaults = st.session_state.get("prefill", prefill_example("typical"))

        # MVPA helper inputs
        mvpa_val = defaults["mvpa"]
        if use_oura:
            oh = st.number_input("Oura High Activity (min/week)", min_value=0.0, value=100.0, step=1.0)
            om = st.number_input("Oura Medium Activity (min/week)", min_value=0.0, value=100.0, step=1.0)
            mvpa_val = min(1000.0, oh + 0.5*om)
            st.info(f"Computed MVPA = {mvpa_val:.1f} min/week")
        else:
            mvpa_val = st.number_input(HELP_TEXT["mvpa"], min_value=0.0, value=float(mvpa_val), step=1.0)

        # REM helper inputs
        rem_pct_val = defaults["rem_pct"]
        if use_rem:
            rem_minutes = st.number_input("REM minutes (per weeknight average × 7 or total)", min_value=0.0, value=52.0, step=1.0)
            tst_minutes = st.number_input("Total Sleep Time (minutes)", min_value=1.0, value=420.0, step=1.0)
            rem_pct_val = 100.0 * rem_minutes / tst_minutes
            st.info(f"Computed REM% = {rem_pct_val:.1f}%")
        else:
            rem_pct_val = st.number_input(HELP_TEXT["rem_pct"], min_value=0.0, max_value=100.0, value=float(rem_pct_val), step=0.1)

        # Organize other inputs in columns
        with colA:
            ogtt_2h = st.number_input(HELP_TEXT["ogtt_2h"], min_value=0.0, value=float(defaults["ogtt_2h"]), step=1.0)
            apob    = st.number_input(HELP_TEXT["apob"], min_value=0.0, value=float(defaults["apob"]), step=1.0)
            vo2max  = st.number_input(HELP_TEXT["vo2max"], min_value=0.0, value=float(defaults["vo2max"]), step=0.1)
            crp     = st.number_input(HELP_TEXT["crp"], min_value=0.0, value=float(defaults["crp"]), step=0.1)
            bmi     = st.number_input(HELP_TEXT["bmi"], min_value=0.0, value=float(defaults["bmi"]), step=0.1)

        with colB:
            packyrs = st.number_input(HELP_TEXT["packyrs"], min_value=0.0, value=float(defaults["packyrs"]), step=0.1)
            moca    = st.number_input(HELP_TEXT["moca"], min_value=0.0, max_value=30.0, value=float(defaults["moca"]), step=0.5)
            cac     = st.number_input(HELP_TEXT["cac"], min_value=0.0, value=float(defaults["cac"]), step=1.0)
            hrv     = st.number_input(HELP_TEXT["hrv"], min_value=0.0, value=float(defaults["hrv"]), step=1.0)
            phq9    = st.number_input(HELP_TEXT["phq9"], min_value=0.0, max_value=27.0, value=float(defaults["phq9"]), step=1.0)

        with colC:
            alt     = st.number_input(HELP_TEXT["alt"], min_value=0.0, value=float(defaults["alt"]), step=1.0)
            egfr    = st.number_input(HELP_TEXT["egfr"], min_value=0.0, value=float(defaults["egfr"]), step=1.0)
            bmd_t   = st.number_input(HELP_TEXT["bmd_t"], value=float(defaults["bmd_t"]), step=0.1)
            truage_delta = st.number_input(HELP_TEXT["truage_delta"], value=float(defaults["truage_delta"]), step=0.1)
            small_hdl    = st.number_input(HELP_TEXT["small_hdl"], min_value=0.0, value=float(defaults["small_hdl"]), step=0.1)

        with colD:
            grip    = st.number_input(HELP_TEXT["grip"], min_value=0.0, value=float(defaults["grip"]), step=0.1)
            swls    = st.number_input(HELP_TEXT["swls"], min_value=0.0, max_value=35.0, value=float(defaults["swls"]), step=1.0)
            rpdqs   = st.number_input(HELP_TEXT["rpdqs"], min_value=0.0, max_value=52.0, value=float(defaults["rpdqs"]), step=1.0)

        if st.button("Compute LQ"):
            try:
                raw = dict(
                    ogtt_2h=ogtt_2h, apob=apob, vo2max=vo2max, crp=crp, bmi=bmi,
                    packyrs=packyrs, moca=moca, mvpa=mvpa_val, cac=cac, hrv=hrv,
                    phq9=phq9, alt=alt, egfr=egfr, bmd_t=bmd_t, truage_delta=truage_delta,
                    small_hdl=small_hdl, rem_pct=rem_pct_val, grip=grip, swls=swls, rpdqs=rpdqs
                )
                res = compute_single(raw, cac_method=cac_method)

                c1, c2 = st.columns(2)
                c1.metric("Composite (0–100)", f"{res['composite']:.2f}")
                c2.metric("LQ (300–850)", f"{res['LQ']:.1f}")

                # Show normalized components
                norm_items = {k.replace('N_',''): v for k,v in res.items() if k.startswith("N_")}
                df = pd.DataFrame({
                    "Variable": list(norm_items.keys()),
                    "Normalized (0–100)": [norm_items[k] for k in norm_items.keys()],
                    "Description": [HELP_TEXT.get(k,"") for k in norm_items.keys()]
                })
                st.dataframe(df, use_container_width=True)
                # Offer download
                out = {**raw, **res}
                out_df = pd.DataFrame([out])
                st.download_button("Download results (CSV)", data=out_df.to_csv(index=False).encode("utf-8"),
                                   file_name="lq_single_result.csv", mime="text/csv")
            except Exception as e:
                st.error(str(e))

    else:
        st.subheader("Bulk CSV")
        st.markdown("Upload a CSV with columns: " + ", ".join(VAR_ORDER))
        upl = st.file_uploader("Choose CSV file", type=["csv"])
        if upl is not None:
            try:
                df = pd.read_csv(upl)
                missing_cols = [c for c in VAR_ORDER if c not in df.columns]
                if missing_cols:
                    st.error(f"Missing required columns: {missing_cols}")
                else:
                    res_df = compute_dataframe(df, cac_method=cac_method)
                    st.success("Computed successfully.")
                    st.dataframe(res_df, use_container_width=True)
                    st.download_button("Download results (CSV)", data=res_df.to_csv(index=False).encode("utf-8"),
                                       file_name="lq_results.csv", mime="text/csv")
            except Exception as e:
                st.error(str(e))

if __name__ == "__main__":
    main()
'''

readme = r'''
# Longevity Quotient (LQ) v1.1 — Streamlit Widget

This is a lightweight, equation-hidden **web app** for calculating the Longevity Quotient (LQ) v1.1 with **equal weights** across 20 variables.

## Features
- **CAC method** toggle: `ln` (matches Stata) or `piecewise` (0–400 mapping)
- **Helpers**: compute MVPA from Oura High + 0.5×Medium; compute REM% from minutes + TST
- **Single patient** mode with prefill examples
- **Bulk CSV** mode for many patients at once
- **Download** results as CSV
- No SciPy dependency (normal CDF via `erf`)

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
