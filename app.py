import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Gold Standard 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Refined Version)")
st.caption("Evidence-Based Protocol: SBOMS Details Integrated with Global Safety Standards")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    # High-risk age based on global standards
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks (Apnoea High Risk)") [cite: 32]

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth", "Chronic Lung Disease (CLD)", "Congenital Heart Disease (CHD)", 
         "Neuromuscular conditions", "Immunodeficiency", "Tobacco smoke exposure"] [cite: 33, 34, 35, 36, 37, 38]
    )

# Target SpO2 threshold logic
current_threshold = 92 if (is_under_6_weeks or risk_factors) else 90 [cite: 11]

st.divider()

# --- 2. CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB):", ["Normal", "Mild", "Moderate", "Severe / Grunting"]) [cite: 4, 12, 20, 28]
    behavior = st.radio("Behavioral State:", ["Normal / Alert", "Irritable", "Lethargic / Altered Mental State"]) [cite: 3, 12, 25]
with c2:
    feeding_status = st.radio("Current Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"]) [cite: 7, 12, 21, 56]
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported by parents", "Observed clinically"]) [cite: 26, 74, 132]
with c3:
    rr = st.number_input("Respiratory Rate (bpm):", 10, 150, 40) [cite: 9, 10, 17, 18, 25]
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96) [cite: 6, 11, 19, 29]
    st.info(f"💡 Clinical Target: SpO2 ≥ {current_threshold}%")

# --- 3. REFINED SEVERITY LOGIC ---
resp_severity = "Mild"

# Moderate Logic (Intermediate signs)
if (effort == "Moderate" or behavior == "Irritable" or feeding_status == "50-75% Intake" or 
    apnoea == "Reported by parents" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70)): [cite: 16, 17, 18, 19, 20, 21]
    resp_severity = "Moderate"

# Severe Logic (Life-threatening signs)
is_resp_severe = (effort == "Severe / Grunting" or apnoea == "Observed clinically" or spo2 < 87 or rr > 70) [cite: 24, 25, 26, 28, 29]

if is_resp_severe or behavior == "Lethargic / Altered Mental State": [cite: 25]
    resp_severity = "Severe"

# Airway Protection: NPO required if high risk of aspiration
is_unsafe_to_feed = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting") [cite: 78, 82]

# --- 4. MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {resp_severity} | Feeding: {'⚠️ NPO REQUIRED' if is_unsafe_to_feed else 'Stable'}")
st.error("🚫 AVOID ROUTINE: Salbutamol, Steroids, Antibiotics, or X-rays.") [cite: 51, 60, 79, 84]

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if is_resp_severe:
        st.error("**🚨 Advanced Respiratory Support (HFNC/CPAP)**")
        st.markdown(f"""
        - **HFNC Setup**: Start at **1.5 L/kg/min**; escalate to **2 L/kg/min** if needed. [cite: 86, 88]
        - **CPAP Escalation**: If HFNC fails (FiO2 > 50% or persistent distress). [cite: 104, 130, 131]
        - **CPAP Settings**: Pressure **7 cmH2O (Awake) / 10 cmH2O (Sleep)** | Flow **7 L/min**. 
        - **Safety**: Nasal suctioning and **venting NGT** are mandatory. [cite: 59, 78, 82, 118]
        """)
    elif resp_severity == "Moderate" or spo2 < current_threshold:
        st.warning("**⚠️ Low Flow Oxygen (LFNP)**")
        st.write(f"- Administer O2 to maintain SpO2 ≥ {current_threshold}%.") [cite: 60]
    else:
        st.success("**✅ Monitoring Only**")
        st.write("- Frequent clinical assessment every 4 hours.") [cite: 62, 98, 121]

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration (Safety Standards)")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **IV Rate**: **70 ml/kg** (Restricted maintenance to prevent SIADH).") [cite: 60, 78, 83]
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration (NGT/IV)**")
        st.write("- Provide fluids at **70 - 100 ml/kg**.") [cite: 78, 83]
    elif feeding_status == "50-75% Intake":
        st.warning("**Action: NGT Supplementation**")
        st.write("- Supplement oral feeds via NGT to ensure maintenance.") [cite: 78]
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- Continue breast/formula feeding as tolerated.") [cite: 12, 60]

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge (Precise Criteria)")

if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled (Stable & Safe)**") [cite: 47, 93, 114]
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Weaning Protocol (Every 4h):**") [cite: 62, 98, 121]
        st.markdown(f"""
        - **Step 1**: Reduce FiO2 to **21% (Room Air)** gradually. [cite: 122]
        - **Step 2**: Trial off flow if stable for **30-90 mins**. [cite: 93]
        - **Fail Criteria**: HR increase **> 20 bpm** or RR increase **> 10 bpm**. [cite: 127]
        - **Oxygen Fail**: SpO2 < {current_threshold}% during trial. [cite: 128]
        """)
    with c_dis:
        st.info("**🏠 Discharge Criteria:**")
        st.markdown(f"""
        - **Stability**: SpO2 ≥ {current_threshold}% on air for **4-12 hours** (including sleep). 
        - **Feeding**: Oral intake **> 50-75%** of normal volumes. [cite: 12, 56]
        - **Work of Breathing**: No grunting or severe recessions. [cite: 96, 110, 111]
        """)

if st.button("Start New Assessment"):
    st.rerun()
