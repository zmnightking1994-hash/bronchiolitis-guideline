import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")
st.caption("Evidence-Based Protocol | SBOMS & International Standards (RCH/PREDICT)")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    # International standard: 6 weeks as high risk for apnoea
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks") 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "Congenital Heart Disease", 
         "Neuromuscular conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# SpO2 Threshold: 92% for high risk, 90% for standard cases
current_threshold = 92 if (is_under_6_weeks or risk_factors) else 90

st.divider()

# --- 2. CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB):", ["Normal", "Mild", "Moderate", "Severe / Grunting"])
    behavior = st.radio("Behavioral State:", ["Normal / Alert", "Irritable", "Lethargic / Altered Mental State"])
with c2:
    feeding_status = st.radio("Current Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"])
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported by parents", "Observed clinically"])
with c3:
    rr = st.number_input("Respiratory Rate (bpm):", 10, 150, 40)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96)
    st.info(f"💡 Target SpO2: ≥ {current_threshold}%")

# --- 3. REFINED SEVERITY LOGIC ---
resp_severity = "Mild"

# Moderate Logic
if (effort == "Moderate" or behavior == "Irritable" or feeding_status == "50-75% Intake" or 
    apnoea == "Reported by parents" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70)):
    resp_severity = "Moderate"

# Severe Logic (Respiratory/Neurological triggers)
is_resp_severe = (effort == "Severe / Grunting" or apnoea == "Observed clinically" or spo2 < 87 or rr > 70)

if is_resp_severe or behavior == "Lethargic / Altered Mental State":
    resp_severity = "Severe"

# Airway Protection Safety Rule
is_unsafe_to_feed = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting")

# --- 4. MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {resp_severity} | Feeding: {'⚠️ NPO' if is_unsafe_to_feed else 'Stable'}")
st.error("🚫 AVOID ROUTINE: Salbutamol, Steroids, Antibiotics, or X-rays.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if is_resp_severe:
        st.error("**🚨 High Flow (HFNC) / CPAP**")
        st.markdown(f"""
        - **HFNC Flow**: 2 L/kg/min | FiO2 40%.
        - **CPAP**: If HFNC fails (FiO2 > 50%).
        - **CPAP Pressure**: **7 cmH2O (Awake) / 10 cmH2O (Sleep)**.
        - **Safety**: Insert a **venting NGT**.
        """)
    elif resp_severity == "Moderate" or feeding_status == "< 50% / Dehydration":
        st.warning("**⚠️ Low Flow Oxygen / Monitoring**")
        st.write(f"- Use nasal prongs to maintain SpO2 ≥ {current_threshold}%.")
    else:
        st.success("**✅ Action: Clinical Monitoring**")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration (Safety Standards)")
    if is_unsafe_to_feed or feeding_status == "< 50% / Dehydration":
        st.error("**🚨 Action: Active Hydration (NGT preferred)**")
        # Global Standard: Restricted fluids (66%-75%) to prevent SIADH
        st.write("- **Rate**: **66% - 75% of maintenance** (Fluid restriction is crucial). ")
        if is_unsafe_to_feed:
            st.write("- **Status**: NPO (Nil By Mouth) due to aspiration risk.")
    elif feeding_status == "50-75% Intake":
        st.warning("**Action: NGT Supplementation**")
        st.write("- Provide bolus feeds via NGT to ensure maintenance.")
    else:
        st.success("**Action: Oral Feeding**")

# --- 5. WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge")
if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled**")
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Weaning (Every 4-6h):**")
        st.markdown(f"""
        - Reduce FiO2 to **21%** first. 
        - **Fail Criteria**: HR increases > 20 bpm or RR > 10 bpm. 
        - Trial off O2 for 30-90 min. 
        """)
    with c_dis:
        st.info("**🏠 Discharge Criteria:**")
        st.write(f"- SpO2 ≥ {current_threshold}% on air for 4-12h (including sleep). ")
        st.write("- Oral intake > 50-75% of normal volumes. ")

if st.button("New Assessment"):
    st.rerun()
