import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Longevity Quotient (LQ) v1.1 — Calculator", layout="wide")
st.title("Longevity Quotient (LQ) v1.1 — Calculator")
st.caption("Equal weights across 20 variables; CAC: ln or piecewise; © Quotient Health")

APP_DESC = (
    "A simple calculator for the Longevity Quotient (LQ) v1.1.\n"
    "- Equal weights across 20 variables\n"
    "- CAC choice: ln-based (default) or piecewise (0–400)\n"
    "- Optional helpers: MVPA from Oura High/Medium; REM% from minutes + TST\n"
    "- Bulk mode: upload a CSV and download results\n"
)

with st.expander("About", expanded=False):
    st.markdown(APP_DESC)

# Reference parameters (means, SDs, directions)
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
}
VAR_ORDER = [
    "ogtt_2h","apob","vo2max","crp","bmi","packyrs","moca","mvpa","cac",
    "hrv","phq9","alt","egfr","bmd_t","truage_delta","small_hdl","rem_pct",
    "grip","swls","rpdqs"
]
HELP = {
    "ogtt_2h":"2-hour OGTT (mg/dL)","apob":"ApoB (mg/dL)","vo2max":"VO₂max (mL/kg/min)",
    "crp":"CRP (mg/L)","bmi":"BMI","packyrs":"Pack-years","moca":"MoCA (0–30)",
    "mvpa":"MVPA (min/week)","cac":"CAC (Agatston)","hrv":"HRV (ms)","phq9":"PHQ-9 (0–27)",
    "alt":"ALT (U/L)","egfr":"eGFR (mL/min/1.73m²)","bmd_t":"BMD T-score",
    "truage_delta":"Epigenetic age delta (yrs)","small_hdl":"Small HDL (μmol/L)",
    "rem_pct":"REM sleep (% TST)","grip":"Grip (kg)","swls":"SWLS (5–35)","rpdqs":"rPDQS (0–52)"
}

def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

def normalize_z(x, key):
    p = REF[key]; z = p["D"] * ((x - p["M"]) / p["S"])
    return clamp(100.0 * normal_cdf(z))

def normalize_rpdqs(x): return clamp((x/52.0)*100.0)

def normalize_cac(value, method="ln"):
    if method == "ln":
        return clamp(100.0 * normal_cdf(-(math.log(value + 1.0) - math.log(100.0))))
    # piecewise
    if value == 0: return 100.0
    if value >= 400: return 0.0
    if value <= 100: return clamp(100.0 - 0.2*value)
    return clamp(50.0 - 0.1*(value - 100.0))

def compute_single(inputs: dict, cac_method="ln") -> dict:
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
    comp = sum(N[v] for v in VAR_ORDER) / 20.0
    LQ = max(300.0, min(850.0, 300.0 + 5.5*comp))
    out = {"composite": comp, "LQ": LQ}
    out.update({f"N_{k}": v for k, v in N.items()})
    return out

def prefill(which="typical"):
    if which=="high":
        return dict(ogtt_2h=85,apob=60,vo2max=55,crp=0.4,bmi=22.5,packyrs=0,moca=29,mvpa=300,
                    cac=0,hrv=75,phq9=0,alt=18,egfr=110,bmd_t=1.0,truage_delta=-5,small_hdl=40,
                    rem_pct=(120/420)*100,grip=55,swls=33,rpdqs=48)
    return dict(ogtt_2h=152,apob=107,vo2max=34,crp=2,bmi=29.6,packyrs=0,moca=25,mvpa=112.5,
                cac=98,hrv=47,phq9=7,alt=42,egfr=82,bmd_t=-1.2,truage_delta=2,small_hdl=10.2,
                rem_pct=(52/420)*100,grip=38,swls=26,rpdqs=35)

st.sidebar.header("Settings")
cac_method = st.sidebar.selectbox("CAC method", options=["ln","piecewise"], index=0)
mode = st.sidebar.radio("Mode", ["Single patient","Bulk CSV"], index=0)

if mode == "Single patient":
    st.subheader("Inputs")

    with st.form("lq_form", clear_on_submit=False):
        # Prefill buttons
        col0a, col0b = st.columns(2)
        if col0a.form_submit_button("Prefill: Typical", use_container_width=True):
            st.session_state.pref = prefill("typical")
        if col0b.form_submit_button("Prefill: High Performer", use_container_width=True):
            st.session_state.pref = prefill("high")

        defaults = st.session_state.get("pref", prefill("typical"))

        use_oura = st.checkbox("Compute MVPA from Oura High/Medium", value=False)
        use_rem  = st.checkbox("Compute REM% from minutes + TST", value=False)

        colA, colB, colC, colD = st.columns(4)

        # MVPA helper
        if use_oura:
            oh = st.number_input("Oura High (min/wk)", min_value=0.0, value=100.0, step=1.0, key="oh")
            om = st.number_input("Oura Medium (min/wk)", min_value=0.0, value=100.0, step=1.0, key="om")
            mvpa_val = min(1000.0, oh + 0.5*om)
            st.info(f"Computed MVPA = {mvpa_val:.1f}")
        else:
            mvpa_val = st.number_input(HELP["mvpa"], min_value=0.0, value=float(defaults["mvpa"]), step=1.0, key="mvpa")

        # REM helper
        if use_rem:
            rem_m = st.number_input("REM minutes", min_value=0.0, value=52.0, step=1.0, key="rem_m")
            tst_m = st.number_input("Total Sleep Time (minutes)", min_value=1.0, value=420.0, step=1.0, key="tst_m")
            rem_pct_val = 100.0*rem_m/tst_m
            st.info(f"Computed REM% = {rem_pct_val:.1f}%")
        else:
            rem_pct_val = st.number_input(HELP["rem_pct"], min_value=0.0, max_value=100.0,
                                          value=float(defaults["rem_pct"]), step=0.1, key="rem_pct")

        # Inputs
        with colA:
            ogtt_2h = st.number_input(HELP["ogtt_2h"], min_value=0.0, value=float(defaults["ogtt_2h"]), step=1.0, key="ogtt_2h")
            apob    = st.number_input(HELP["apob"],    min_value=0.0, value=float(defaults["apob"]),    step=1.0, key="apob")
            vo2max  = st.number_input(HELP["vo2max"],  min_value=0.0, value=float(defaults["vo2max"]),  step=0.1, key="vo2max")
            crp     = st.number_input(HEL_
