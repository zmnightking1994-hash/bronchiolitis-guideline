import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Gold Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Gold Version)")
st.caption("Integrated Protocol: RCH Melbourne, PREDICT & Evidence-Based Standards")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks (Apnoea High Risk)") 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease (CLD)", "Congenital Heart Disease (CHD)", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

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

# Default is Mild (Normal)
resp_severity = "Mild"

# Check for Moderate first
if (effort == "Moderate" or 
    behavior == "Irritable" or 
    feeding_status == "50-75% Intake" or 
    apnoea == "Reported by parents" or 
    (87 <= spo2 < current_threshold) or 
    (50 <= rr <= 70)):
    resp_severity = "Moderate"

# Severe overrides everything else
if (effort == "Severe / Grunting" or 
    behavior == "Lethargic / Altered Mental State" or 
    feeding_status == "< 50% / Dehydration" or
    apnoea == "Observed clinically" or 
    spo2 < 87 or 
    rr > 70):
    resp_severity = "Severe"

# Airway Protection Rule
is_unsafe_to_feed = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting")

# --- 4. DETAILED MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {resp_severity} | Feeding Status: {'⚠️ NBM REQUIRED' if is_unsafe_to_feed else 'Stable'}")
st.error("🚫 **AVOID ROUTINE:** Salbutamol, Steroids, Antibiotics, X-rays, or Deep Suction.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 High Flow (HFNC) & Escalation Protocol:**")
        st.markdown(f"""
        - **HFNC Flow**: Start at **2 L/kg/min**[cite: 88].
        - **FiO2**: Start at **40%**; titrate to maintain SpO2 ≥ {current_threshold}%[cite: 89].
        - **Gastric Safety**: Insert a **venting NGT** to prevent gastric distension[cite: 82].
        - **CPAP Escalation**: If HFNC fails (FiO2 > 50%) or persistent apnoea[cite: 105, 131].
        - **CPAP Settings**: Pressure **5-7 cmH2O** (up to 10 during sleep) | Flow **7-10 L/min**[cite: 95].
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Low Flow Oxygen (LFNP):**")
        st.write(f"- Nasal prongs at 0.5 - 2 L/min to keep SpO2 ≥ {current_threshold}%.")
    else:
        st.success("**✅ Action: Clinical Monitoring**")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Method**: NGT (preferred) or IV[cite: 78, 82].")
        st.write("- **Rate**: **66-75% maintenance** to prevent SIADH[cite: 78, 83].")
    elif feeding_status == "50-75% Intake":
        st.warning("**Action: NGT Supplementation**")
        st.write("- Provide bolus feeds via NGT to ensure 100% maintenance.")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration**")
        st.write("- NGT at 66-75% maintenance rate[cite: 83].")
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- Continue breastfeeding or formula as tolerated.")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled:** Stable patient. Safe for home.")
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Weaning Protocol:**")
        st.markdown(f"""
        - **HFNC Weaning**: Reduce FiO2 to **21%** first[cite: 122]. Trial off flow if stable for 2h[cite: 93].
        - **Assessment**: Every 4-6 hours[cite: 121].
        - **Failure Criteria**: If HR increases by >20 bpm or RR by >10 bpm[cite: 127].
        """)
    with c_dis:
        st.info("**🏠 Discharge Criteria:**")
        st.markdown(f"""
        - **Oxygen**: SpO2 ≥ {current_threshold}% on room air for 4-12h (including sleep)[cite: 66].
        - **Feeding**: Oral intake > 50-75% of normal volumes[cite: 21].
        - **Stability**: No grunting or severe effort[cite: 28, 96].
        """)

if st.button("Start New Assessment"):
    st.rerun()
