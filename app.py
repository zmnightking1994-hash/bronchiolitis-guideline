import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Gold Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")
st.caption("Integrated Protocol: Syrian Board of Medical Specialties (SBOMS) Clinical Standards")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    # SBOMS Risk Factor: Infants under 2 months [cite: 32]
    is_high_risk_age = st.checkbox("Infant age < 2 months")

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness[cite: 31]:",
        ["Preterm birth [cite: 33]", "Chronic Lung Disease/Cystic Fibrosis [cite: 36]", 
         "Congenital Heart Disease (Complex/Cyanotic) [cite: 37]", "Neuromuscular conditions [cite: 38]", 
         "Immunodeficiency [cite: 35]", "Parental Smoking [cite: 34]"]
    )

# Target SpO2: 90% for standard cases [cite: 11], 92% for high-risk [cite: 60]
current_threshold = 92 if (is_high_risk_age or risk_factors) else 90

st.divider()

# --- 2. CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment [cite: 2]")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB) [cite: 4]:", ["Normal", "Mild", "Moderate", "Severe / Grunting [cite: 28]"])
    behavior = st.radio("Behavioral State [cite: 3]:", ["Normal / Alert", "Irritable", "Lethargic / Altered Mental State "])
with c2:
    feeding_status = st.radio("Current Intake [cite: 7]:", ["Adequate", "50-75% Intake", "< 50% / Dehydration [cite: 21]"])
    apnoea = st.selectbox("Apnoea Events [cite: 26]:", ["None", "Reported by parents", "Observed clinically [cite: 74]"])
with c3:
    rr = st.number_input("Respiratory Rate (bpm)[cite: 4]:", 10, 150, 40)
    spo2 = st.slider("Oxygen Saturation (SpO2 %)[cite: 6]:", 70, 100, 96)
    st.info(f"💡 Clinical Target: SpO2 ≥ {current_threshold}% [cite: 11, 60]")

# --- 3. SBOMS SEVERITY LOGIC ---
severity = "Mild" # [cite: 8]

# Moderate Criteria [cite: 16]
if (effort == "Moderate" or feeding_status == "50-75% Intake" or (50 <= rr <= 80) or (88 <= spo2 < 90) or risk_factors or is_high_risk_age):
    severity = "Moderate" # [cite: 16, 17, 18, 19, 21]

# Severe Criteria [cite: 24]
if (effort == "Severe / Grunting" or behavior == "Lethargic / Altered Mental State" or 
    feeding_status == "< 50% / Dehydration" or apnoea == "Observed clinically" or 
    spo2 < 88 or rr > 80): # [cite: 25, 27, 28, 29]
    severity = "Severe"

# Safety Rule: NPO (Nil By Mouth) [cite: 78, 82]
is_npo = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting")

# --- 4. MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {severity} | Status: {'⚠️ NPO REQUIRED' if is_npo else 'Stable'}")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if severity == "Severe":
        st.error("**🚨 High Flow (HFNC) / CPAP Protocol:**")
        st.markdown(f"""
        - **HFNC Flow [cite: 86]**: Start at **1.5 L/kg/min** (Min 8 L/min). Escalate to **2 L/kg/min** if needed[cite: 88].
        - **CPAP Escalation [cite: 104]**: If HFNC fails after 30 mins (Needs FiO2 > 60% or worsening WOB)[cite: 105, 106, 107].
        - **CPAP Settings **: PEEP **7 cmH2O (Awake) / 10 cmH2O (Sleep)** | Flow **7 L/min**.
        - **Safety [cite: 82]**: Mandatory **Venting NGT** and nasal suctioning[cite: 59].
        """)
    elif severity == "Moderate" or spo2 < current_threshold:
        st.warning("**⚠️ Low Flow Oxygen / Monitoring:**")
        st.write(f"- Use Nasal Prongs/Mask to maintain SpO2 ≥ {current_threshold}%[cite: 60].")
        st.write("- Clinical assessment every 4 hours (4HRCCP)[cite: 62].")
    else:
        st.success("**✅ Home Management:**")
        st.write("- Nasal hygiene [cite: 48] and parental education[cite: 53].")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration [cite: 7]")
    if is_npo:
        st.error("**🚨 Action: Restricted IV Fluids:**")
        st.write("- **Initial Rate [cite: 78]**: **100 ml/kg** D5 (if Na is normal).")
        st.write("- **Restricted Rate **: Reduce to **70 ml/kg** (Restricted Maintenance).")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration:**")
        st.write("- IV/NGT Fluids at **70 ml/kg**[cite: 60].")
    else:
        st.success("**Action: Oral Feeding:**")
        st.write("- Continue breastfeeding/formula; monitor urine output[cite: 7].")

# --- 5. WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge (SBOMS Standards)")

c_wean, c_dis = st.columns(2)
with c_wean:
    st.info("**📉 HFNC Weaning Protocol[cite: 119]:**")
    st.markdown("""
    - **Stability**: Must be stable for **4 consecutive assessments** (every 4h)[cite: 121].
    - **Step 1 **: Reduce FiO2 to **40%**, then decrease by **4% every 4h** until 24%.
    - **Step 2 [cite: 123]**: Reduce flow to **1.5 L/kg/min**.
    - **Trial Off [cite: 126]**: Room air for **5 mins**.
    - **Failure Criteria [cite: 127, 128]**: HR increase **> 20**, RR increase **> 10**, or SpO2 **< 90% (Awake) / 88% (Sleep)**.
    """)
with c_dis:
    st.info("**🏠 Discharge Criteria:**")
    st.markdown(f"""
    - **Oxygen [cite: 93]**: Trial room air for **30 mins (2L flow)** then **90 mins (1L flow)**.
    - **Final Check **: Stable on Room Air for **12 hours**.
    - **Feeding [cite: 12]**: Oral intake is adequate.
    - **Effort [cite: 96]**: RR < 60 (Infant) / < 50 (Child) with no grunting.
    """)

if st.button("New Patient Assessment"):
    st.rerun()
