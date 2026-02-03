import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Clinical Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")
st.caption("Evidence-Based Guidelines: RCH Melbourne, PREDICT & Global Safety Standards")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks") 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "Congenital Heart Disease", 
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

is_severe = (
    effort == "Severe / Grunting" or 
    behavior == "Lethargic / Altered Mental State" or 
    feeding_status == "< 50% / Dehydration" or 
    apnoea == "Observed clinically" or 
    spo2 < 87 or 
    rr > 70
)

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
needs_hfnc = (behavior == "Lethargic / Altered Mental State" or effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically")
is_npo = (behavior == "Lethargic / Altered Mental State" or effort == "Severe / Grunting" or apnoea == "Observed clinically")

# --- 4. MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {severity}")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if needs_hfnc:
        support_type = "HFNC"
        st.error("**🚨 Action: High Flow (HFNC) Required**")
        st.markdown(f"""
        - **Flow Rate**: Start at **2 L/kg/min**.
        - **FiO2**: Titrate to keep SpO2 ≥ {current_threshold}%.
        - **Note**: Mandatory venting NGT and frequent suctioning.
        """)
    elif severity == "Moderate" or spo2 < current_threshold:
        support_type = "LowFlow"
        st.warning("**⚠️ Action: Low Flow Oxygen (LFNP)**")
        st.write(f"- Nasal prongs at 0.5 - 2 L/min to maintain SpO2 ≥ {current_threshold}%.")
    else:
        support_type = "None"
        st.success("**✅ Action: Clinical Monitoring**")
        st.write("- Routine assessment every 4 hours.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration")
    if is_npo or feeding_status == "< 50% / Dehydration":
        st.error("**🚨 Action: Fluid Restriction (66-75%)**")
        st.write("- Start **NGT** hydration at restricted rates to prevent SIADH.")
    elif feeding_status == "50-75% Intake":
        st.warning("**Action: NGT Supplementation**")
        st.write("- Supplement oral feeds via NGT to 100% maintenance.")
    else:
        st.success("**Action: Oral Feeding**")

# --- 5. DYNAMIC WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

c_wean, c_dis = st.columns(2)

with c_wean:
    if support_type == "HFNC":
        st.info("**📉 HFNC Weaning Steps:**")
        st.markdown(f"""
        1. **FiO2 Weaning**: Reduce FiO2 to **21%** (Room Air) first.
        2. **Flow Weaning**: Gradually reduce flow (e.g., to 1.5 L/kg/min).
        3. **Trial Off**: Stop flow for **30-90 minutes** to check stability.
        4. **Failure**: Fail if HR increases > 20 bpm, RR > 10 bpm, or SpO2 < {current_threshold}%.
        """)
    elif support_type == "LowFlow":
        st.info("**📉 Low Flow Weaning:**")
        st.markdown(f"""
        1. **Direct Trial**: Attempt to stop oxygen directly to room air.
        2. **Monitoring**: Watch SpO2 during both awake and sleep periods.
        3. **Failure**: Fail if SpO2 drops below {current_threshold}% or WOB increases.
        """)
    else:
        st.success("**✅ No Weaning Required**")
        st.write("- Patient is already on room air.")

with c_dis:
    st.info("**🏠 Discharge Criteria:**")
    st.markdown(f"""
    - **O2 Stability**: SpO2 ≥ {current_threshold}% on room air for **4-12 hours** (must include sleep).
    - **Feeding**: Oral intake consistently **> 50-75%** of normal volumes.
    - **Clinical**: Stable Work of Breathing with no grunting.
    """)

if st.button("New Assessment"):
    st.rerun()
