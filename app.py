import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Clinical Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")
st.caption("Comprehensive Version: Dynamic Escalation & Clinical Safety Logic")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks (Apnoea High Risk)")

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "Congenital Heart Disease", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# Target SpO2 threshold logic
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

# --- 3. DYNAMIC SEVERITY LOGIC (STRICT) ---

# Severe criteria
is_severe = (
    effort == "Severe / Grunting" or 
    behavior == "Lethargic / Altered Mental State" or 
    feeding_status == "< 50% / Dehydration" or 
    apnoea == "Observed clinically" or 
    spo2 < 87 or 
    rr > 70
)

# Moderate criteria
is_moderate = (
    not is_severe and (
        effort == "Moderate" or 
        behavior == "Irritable" or 
        feeding_status == "50-75% Intake" or 
        apnoea == "Reported by parents" or 
        (87 <= spo2 < current_threshold) or 
        (50 <= rr <= 70)
    )
)

severity = "Severe" if is_severe else ("Moderate" if is_moderate else "Mild")

# --- 4. DYNAMIC MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {severity}")
st.error("🚫 AVOID: Salbutamol, Steroids, Antibiotics, or Routine X-rays.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    
    # Advanced Support logic
    if behavior == "Lethargic / Altered Mental State" or effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically":
        st.error("**🚨 Action: Advanced Support (HFNC/CPAP)**")
        st.markdown(f"""
        - **HFNC**: Start at **2 L/kg/min**. Titrate FiO2 to keep SpO2 ≥ {current_threshold}%.
        - **CPAP**: Escalate if FiO2 > 50% or persistent apnoea. Start at **5-8 cmH2O**.
        - **Care**: Frequent nasal suction and **Venting NGT** required.
        """)
    elif severity == "Moderate" or spo2 < current_threshold:
        st.warning("**⚠️ Action: Low Flow Oxygen (LFNP)**")
        st.write(f"- Use nasal prongs (0.5 - 2 L/min) to maintain SpO2 ≥ {current_threshold}%.")
        st.write("- Assessment every 2-4 hours.")
    else:
        st.success("**✅ Action: Clinical Monitoring**")
        st.write("- Routine observations (HR, RR, WOB) every 4 hours.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    
    if behavior == "Lethargic / Altered Mental State" or effort == "Severe / Grunting" or apnoea == "Observed clinically":
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.markdown("""
        - **Risk**: High aspiration risk.
        - **Hydration**: Start **NGT** (preferred) or IV fluids.
        - **Rate**: **66% - 75% of maintenance** (Strict restriction to prevent SIADH).
        """)
    elif feeding_status == "< 50% / Dehydration":
        st.error("**🚨 Action: Active Hydration Required**")
        st.markdown(f"""
        - **Route**: NGT at **75% - 100%** maintenance.
        - **Severity Note**: High severity due to poor intake, but oral/NGT trial is possible if breathing is stable.
        """)
    elif feeding_status == "50-75% Intake":
        st.warning("**⚠️ Action: NGT Supplementation**")
        st.write("- Supplement oral feeds via NGT to ensure 100% daily maintenance.")
    else:
        st.success("**✅ Action: Oral Feeding**")
        st.write("- Continue breast or formula feeds as tolerated.")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

c_wean, c_dis = st.columns(2)
with c_wean:
    st.info("**📉 Weaning Steps:**")
    st.markdown(f"""
    1. **Reduce FiO2**: Drop to **21%** (Room Air) first while on flow.
    2. **Trial Off**: Stop flow/O2 for **30-90 minutes**.
    3. **Failure Check**: Fail if HR increases > 20 bpm, RR increases > 10 bpm, or SpO2 < {current_threshold}%.
    """)
with c_dis:
    st.info("**🏠 Discharge Criteria:**")
    st.markdown(f"""
    - **O2 Stability**: SpO2 ≥ {current_threshold}% on room air for **4-12 hours** (must include sleep).
    - **Feeding**: Intake consistently **> 50-75%** of normal volumes.
    - **Breathing**: Stable WOB, no grunting, and RR within safe limits.
    """)

if st.button("New Assessment"):
    st.rerun()
