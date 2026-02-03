import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Bronchiolitis Clinical Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")
st.caption("Evidence-Based Guidelines: RCH Melbourne, PREDICT & Global Standards")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    # High risk for apnoea in infants under 6 weeks
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks") 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "Congenital Heart Disease", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# SpO2 Threshold: 92% for high risk, 90% for standard
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

# --- 3. REFINED SEVERITY & SAFETY LOGIC ---

# a. General Severity (Overall Classification)
severity = "Mild"
if (effort == "Moderate" or behavior == "Irritable" or feeding_status == "50-75% Intake" or 
    apnoea == "Reported by parents" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70)):
    severity = "Moderate"

if (effort == "Severe / Grunting" or behavior == "Lethargic / Altered Mental State" or 
    feeding_status == "< 50% / Dehydration" or apnoea == "Observed clinically" or 
    spo2 < 87 or rr > 70):
    severity = "Severe"

# b. Respiratory Support Logic (Fixed: Poor feeding alone doesn't trigger HFNC)
needs_advanced_resp = (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically")

# c. Feeding Safety (Aspiration Risk)
is_unsafe_to_feed = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting")

# --- 4. MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {severity} | Feeding: {'⚠️ NPO REQUIRED' if is_unsafe_to_feed else 'Stable'}")
st.error("🚫 AVOID: Salbutamol, Steroids, Antibiotics, or Routine Chest X-rays.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if needs_advanced_resp:
        st.error("**🚨 High Flow (HFNC) & Escalation:**")
        st.markdown(f"""
        - **HFNC Flow**: Start at **2 L/kg/min**.
        - **FiO2**: Titrate to maintain SpO2 ≥ {current_threshold}%.
        - **Escalation**: Consider CPAP if FiO2 > 50% or persistent apnoea.
        - **CPAP**: Pressure **5 - 8 cmH2O**.
        - **Support**: Ensure nasal suctioning and gastric venting (Venting NGT).
        """)
    elif severity == "Moderate" or spo2 < current_threshold:
        st.warning("**⚠️ Low Flow Oxygen (LFNP):**")
        st.write(f"- Administer O2 via nasal prongs at 0.5 - 2 L/min.")
        st.write(f"- Aim for SpO2 ≥ {current_threshold}%.")
    else:
        st.success("**✅ Action: Monitoring Only**")
        st.write("- Regular clinical assessment (HR, RR, WOB) every 4 hours.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Method**: NGT hydration (preferred) or IV fluids.")
        st.write("- **Rate**: **66% - 75% of maintenance** (Fluid restriction to prevent SIADH).")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration**")
        st.write("- Start **NGT** (preferred) or IV hydration at **75% - 100%** maintenance.")
        st.info("💡 Respiratory distress is absent; focus on hydration stability.")
    elif feeding_status == "50-75% Intake":
        st.warning("**Action: NGT Supplementation**")
        st.write("- Bolus NGT feeds to supplement oral intake.")
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- Continue breast or formula feeds as tolerated.")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

c_wean, c_dis = st.columns(2)
with c_wean:
    st.info("**📉 Weaning Protocol:**")
    st.markdown(f"""
    - **HFNC**: 1. Reduce FiO2 to **21%**. 2. If stable for 2h, trial off flow.
    - **Low Flow**: Trial off directly to room air.
    - **Success**: Stable HR/RR and SpO2 ≥ {current_threshold}% for 2-4 hours.
    - **Fail**: Increased WOB, HR increases > 20 bpm, or RR > 10 bpm.
    """)
with c_dis:
    st.info("**🏠 Discharge Criteria:**")
    st.markdown(f"""
    - **Oxygen**: SpO2 ≥ {current_threshold}% on room air for **4 - 12 hours** (including sleep).
    - **Feeding**: Oral intake consistently **> 50-75%** of normal volumes.
    - **Clinical**: Stable work of breathing with no grunting.
    - **Social**: Caregivers are confident in home management.
    """)

if st.button("Start New Assessment"):
    st.rerun()
