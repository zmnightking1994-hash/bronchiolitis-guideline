import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")
st.caption("Evidence-Based Protocol | SBOMS & International Standards")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    # High risk age threshold [cite: 32]
    is_under_2_months = st.checkbox("Infant age < 2 months") 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth", "Chronic Lung Disease", "Congenital Heart Disease", 
         "Neuromuscular conditions", "Immunodeficiency", "Tobacco smoke exposure"] # [cite: 33, 34, 35, 36, 37, 38]
    )

# SpO2 Threshold: 92% for high risk, 90% for others 
current_threshold = 92 if (is_under_2_months or risk_factors) else 90

st.divider()

# --- 2. CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB):", ["Normal", "Mild", "Moderate", "Severe / Grunting"]) # [cite: 4, 28]
    behavior = st.radio("Behavioral State:", ["Normal / Alert", "Irritable", "Lethargic / Altered Mental State"]) # [cite: 3, 25]
with c2:
    feeding_status = st.radio("Current Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"]) # [cite: 21]
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported by parents", "Observed clinically"]) # [cite: 26, 74]
with c3:
    rr = st.number_input("Respiratory Rate (bpm):", 10, 150, 40) # [cite: 4, 9, 17, 25]
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96) # [cite: 6, 11, 19, 29]
    st.info(f"💡 Target SpO2: ≥ {current_threshold}%")

# --- 3. REFINED SEVERITY LOGIC ---
resp_severity = "Mild"

# Moderate Logic [cite: 16, 17, 19, 21]
if (effort == "Moderate" or behavior == "Irritable" or feeding_status == "50-75% Intake" or 
    apnoea == "Reported by parents" or (87 <= spo2 < current_threshold)):
    resp_severity = "Moderate"

# Severe Logic (Triggered by high RR, severe WOB, or low SpO2) [cite: 24, 25, 28, 29]
is_resp_severe = (effort == "Severe / Grunting" or apnoea == "Observed clinically" or spo2 < 87 or rr > 70)

if is_resp_severe or behavior == "Lethargic / Altered Mental State":
    resp_severity = "Severe"

# Airway Protection [cite: 78, 82]
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
        - **HFNC Flow**: Start at **1.5 - 2 L/kg/min**[cite: 86, 88].
        - **FiO2**: Titrate to keep SpO2 ≥ {current_threshold}%[cite: 89].
        - **CPAP**: Consider if HFNC fails (FiO2 > 50% needed)[cite: 106].
        - **CPAP Settings**: **7 cmH2O (Awake) / 10 cmH2O (Sleep)**.
        - **Safety**: Insert a **venting NGT**[cite: 78, 82].
        """)
    elif resp_severity == "Moderate" or spo2 < current_threshold or feeding_status == "< 50% / Dehydration":
        st.warning("**⚠️ Low Flow Oxygen / Monitoring**")
        st.write(f"- Use nasal prongs to maintain SpO2 ≥ {current_threshold}%.")
    else:
        st.success("**✅ Action: Clinical Monitoring**")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Rate**: **70 ml/kg** (Restricted Maintenance)[cite: 60, 78].")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: NGT / IV Hydration**")
        st.write("- Start at **70 - 100 ml/kg** based on Na levels[cite: 78, 83].")
    else:
        st.success("**Action: Oral Feeding**")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Checklist")
if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled**")
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Weaning (Every 4h):**")
        st.markdown(f"""
        - Reduce FiO2 to **21%** gradually[cite: 122].
        - **Failure**: HR increase > 20 bpm or RR > 10 bpm.
        - Trial off O2 for 30-90 min[cite: 93].
        """)
    with c_dis:
        st.info("**🏠 Discharge Criteria:**")
        st.write(f"- SpO2 ≥ {current_threshold}% on air for 4-12h[cite: 66, 128].")
        st.write("- Adequate oral intake (> 50-75%)[cite: 56].")

if st.button("New Assessment"):
    st.rerun()
