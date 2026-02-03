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

# --- 3. REFINED SEVERITY LOGIC (UPDATED) ---

# Severe triggers: includes poor feeding < 50% and lethargy
is_severe_trigger = (
    effort == "Severe / Grunting" or 
    behavior == "Lethargic / Altered Mental State" or 
    feeding_status == "< 50% / Dehydration" or # تم التأكد من وجودها هنا لتفعيل الشدة العالية
    apnoea == "Observed clinically" or 
    spo2 < 87 or 
    rr > 70
)

is_moderate_trigger = (
    effort == "Moderate" or 
    behavior == "Irritable" or 
    feeding_status == "50-75% Intake" or 
    apnoea == "Reported by parents" or 
    (87 <= spo2 < current_threshold) or 
    (50 <= rr <= 70)
)

if is_severe_trigger:
    severity = "Severe"
elif is_moderate_trigger:
    severity = "Moderate"
else:
    severity = "Mild"

# Respiratory Support Logic: تفعيل الدعم التنفسي المتقدم في حالتين (الجهد التنفسي أو اضطراب الوعي/الخمول)
needs_advanced_resp = (effort == "Severe / Grunting" or behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or spo2 < 87)

# NPO Logic
is_npo = (behavior == "Lethargic / Altered Mental State" or effort == "Severe / Grunting" or apnoea == "Observed clinically")

# --- 4. MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Severity: {severity} | Status: {'⚠️ NPO REQUIRED' if is_npo else 'Stable'}")
st.error("🚫 AVOID: Salbutamol, Steroids, Antibiotics, or Routine Chest X-rays.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if needs_advanced_resp:
        st.error("**🚨 High Flow (HFNC) / CPAP Protocol:**")
        st.markdown(f"""
        - **Action**: Start HFNC at **2 L/kg/min**.
        - **Note**: Mandatory due to **{behavior if behavior == 'Lethargic / Altered Mental State' else 'Respiratory Distress'}**.
        - **FiO2**: Titrate for SpO2 ≥ {current_threshold}%.
        - **Venting**: Mandatory NGT for decompression.
        """)
    elif severity == "Moderate" or spo2 < current_threshold:
        st.warning("**⚠️ Low Flow Oxygen (LFNP):**")
        st.write(f"- Maintain SpO2 ≥ {current_threshold}% using nasal prongs.")
    else:
        st.success("**✅ Action: Monitoring Only**")
        st.write("- Assessment every 4 hours.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration (Safety Standards)")
    if severity == "Severe" or feeding_status == "< 50% / Dehydration":
        st.error("**🚨 Action: Fluid Restriction (Safety Rate)**")
        st.markdown(f"""
        - **Rate**: **66% - 75% of maintenance** (Strict restriction).
        - **Reason**: Risk of SIADH in **Severe** or **Dehydrated** cases.
        - **Route**: NGT hydration (preferred).
        """)
    elif feeding_status == "50-75% Intake":
        st.warning("**Action: NGT Bolus Support**")
        st.write("- Supplement feeds via NGT to 100% maintenance.")
    else:
        st.success("**Action: Oral Feeding**")

# --- 5. WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

c_wean, c_dis = st.columns(2)
with c_wean:
    st.info("**📉 Weaning:**")
    st.markdown("""
    - Reduce FiO2 to **21%** (Room Air) first.
    - Trial off O2 for 30-90 mins.
    - **Fail if**: HR increases > 20 bpm or RR > 10 bpm.
    """)
with c_dis:
    st.info("**🏠 Discharge Criteria:**")
    st.markdown(f"""
    - SpO2 ≥ {current_threshold}% on air for **4-12 hours**.
    - Oral intake > 50-75% of normal.
    - Stable Work of Breathing.
    """)

if st.button("New Assessment"):
    st.rerun()
