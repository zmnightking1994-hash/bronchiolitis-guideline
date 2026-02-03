import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Gold Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Gold Version)")
st.caption("Integrated Protocol: RCH Melbourne, PREDICT & Evidence-Based Standards")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    # Age threshold for high risk of apnoea [cite: 32]
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks (High Risk)") 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease (CLD)", "Congenital Heart Disease (CHD)", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# Target SpO2: 92% for high-risk, 90% for standard cases [cite: 11, 19]
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

# --- 3. SAFETY & SEVERITY LOGIC ---
resp_severity = "Mild"
# Severe if grunting, low SpO2, observed apnoea, lethargy, or very high RR [cite: 24, 25, 26, 28, 29]
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or 
    behavior == "Lethargic / Altered Mental State" or rr > 70):
    resp_severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or apnoea == "Reported by parents"):
    resp_severity = "Moderate"

# Airway Protection: NBM required for Severe effort, Lethargy, or Apnoea 
is_unsafe_to_feed = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting")

# --- 4. DETAILED MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Resp: {resp_severity} | Feeding Status: {'⚠️ NBM REQUIRED' if is_unsafe_to_feed else 'Stable'}")
st.error("🚫 **AVOID ROUTINE:** Salbutamol, Steroids, Antibiotics, X-rays, or Deep Suction.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 High Flow (HFNC) & Escalation Protocol:**")
        st.markdown(f"""
        - **HFNC Flow:** Start at **2 L/kg/min** (Max 25L/min)[cite: 88].
        - **FiO2:** Start at **40%**; titrate to maintain SpO2 ≥ {current_threshold}%[cite: 89].
        - **Gastric Safety:** Insert a **venting NGT** to relieve gastric distension.
        - **CPAP Escalation:** Consider if HFNC fails (FiO2 > 50%) or persistent apnoea[cite: 104, 130].
        - **CPAP Settings:** Pressure **5-7 cmH2O** (up to 10 during sleep) | Flow **7-10 L/min**[cite: 95, 103].
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Low Flow Oxygen (LFNP):**")
        st.write(f"- Use nasal prongs at 0.5 - 2 L/min to keep SpO2 ≥ {current_threshold}%[cite: 60].")
    else:
        st.success("**✅ Action: Clinical Monitoring**")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Route:** NGT (preferred) or IV[cite: 78, 83].")
        st.write("- **Rate:** Restricted to **66-75% maintenance** to prevent SIADH[cite: 60, 78, 83].")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration**")
        st.write("- NGT at 66-75% maintenance rate[cite: 60, 83].")
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- Continue breastfeeding or formula as tolerated.")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

# Fast Track Logic
if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled:** SpO2 ≥ 95% on air and stable. Safe for home.")
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Weaning Protocol:**")
        st.markdown(f"""
        - **HFNC Weaning:** 1. Reduce FiO2 to **21%**[cite: 122]. 2. Trial off flow if stable for 2h[cite: 93].
        - **Assessment:** Every 4-6 hours[cite: 62, 121].
        - **Failure Criteria:** If HR increases by >20 bpm or RR by >10 bpm.
        """)
    with c_dis:
        st.info("**🏠 Discharge Criteria:**")
        st.markdown(f"""
        - **Oxygen:** SpO2 ≥ {current_threshold}% on room air for 4-12h (must include sleep)[cite: 66, 91].
        - **Feeding:** Oral intake > 50-75% of maintenance[cite: 12].
        - **Stability:** No grunting or severe effort[cite: 96, 111].
        """)



if st.button("Start New Assessment"):
    st.rerun()
