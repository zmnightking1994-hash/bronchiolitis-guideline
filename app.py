import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Gold Standard 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Clinical Version)")
st.caption("Integrated Protocol: Safety-First Approach with Dynamic Fluid & Resp Logic")

# --- 1. RISK ASSESSMENT (تقييم المخاطر) ---
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

# ضبط عتبة الأكسجين بناءً على الخطورة
current_threshold = 92 if (is_under_6_weeks or risk_factors) else 90

st.divider()

# --- 2. CLINICAL ASSESSMENT (التقييم السريري) ---
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

# --- 3. DYNAMIC SEVERITY LOGIC (منطق الشدة) ---

# تصنيف الحالة الشديدة (Severe)
is_severe = (
    effort == "Severe / Grunting" or 
    behavior == "Lethargic / Altered Mental State" or 
    feeding_status == "< 50% / Dehydration" or 
    apnoea == "Observed clinically" or 
    spo2 < 87 or 
    rr > 70
)

# تصنيف الحالة المتوسطة (Moderate)
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

# منطق الدعم التنفسي المتقدم
needs_advanced_resp = (behavior == "Lethargic / Altered Mental State" or effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically")

# منطق منع التغذية الفموية (NPO)
is_npo = (behavior == "Lethargic / Altered Mental State" or effort == "Severe / Grunting" or apnoea == "Observed clinically")

# --- 4. MANAGEMENT PILLARS (أعمدة التدبير) ---
st.divider()
st.header(f"Management Plan | Severity: {severity}")
st.error("🚫 AVOID: Salbutamol, Steroids, Antibiotics, or Routine Chest X-rays.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if needs_advanced_resp:
        support_type = "HFNC"
        st.error("**🚨 Action: High Flow (HFNC) Protocol Required**")
        st.markdown(f"""
        - **Flow Rate**: Start at **2 L/kg/min**.
        - **FiO2**: Titrate to keep SpO2 ≥ {current_threshold}%.
        - **Escalation**: Move to CPAP (5-8 cmH2O) if FiO2 > 50% or persistent apnoea.
        - **Safety**: Gastric venting via NGT is mandatory.
        """)
    elif severity == "Moderate" or spo2 < current_threshold:
        support_type = "LowFlow"
        st.warning("**⚠️ Action: Low Flow Oxygen (LFNP)**")
        st.write(f"- Administer O2 via nasal prongs at 0.5 - 2 L/min to reach target SpO2.")
    else:
        support_type = "None"
        st.success("**✅ Action: Clinical Monitoring**")
        st.write("- Routine HR, RR, and WOB assessment every 4 hours.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration (Safety Standards)")
    # تم تثبيت نسبة السوائل عند 66-75% لجميع الحالات التي تحتاج تدخل (Restricted Maintenance)
    if is_npo or feeding_status == "< 50% / Dehydration" or severity == "Severe":
        st.error("**🚨 Action: Restricted Fluid Rate (66% - 75%)**")
        st.markdown(f"""
        - **Rate**: **66% to 75%** of calculated daily maintenance.
        - **Rationale**: Prevent **SIADH** and pulmonary edema.
        - **Route**: NGT hydration is the gold standard.
        - **Status**: {'NPO (Nil By Mouth) due to aspiration risk.' if is_npo else 'NGT feeding allowed if breathing stable.'}
        """)
    elif feeding_status == "50-75% Intake":
        st.warning("**⚠️ Action: Supplemental NGT Boluses**")
        st.write("- Supplement oral feeds via NGT to ensure total intake reaches **75%** of maintenance.")
    else:
        st.success("**✅ Action: Oral Feeding Ad Libitum**")
        st.write("- Monitor output and continue frequent small feeds.")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.header("🏥 Weaning & Discharge Protocol")

c_wean, c_dis = st.columns(2)

with c_wean:
    if support_type == "HFNC":
        st.info("**📉 HFNC Weaning Strategy:**")
        st.markdown(f"""
        1. **FiO2 Weaning**: Drop FiO2 to **21%** (Room Air) first.
        2. **Flow Weaning**: Gradually reduce flow (e.g., to 1 L/kg/min).
        3. **Trial Off**: Stop all support for **30-90 minutes**.
        4. **Failure Criteria**: HR increase > 20 bpm, RR > 10 bpm, or SpO2 < {current_threshold}%.
        """)
    elif support_type == "LowFlow":
        st.info("**📉 Low Flow Weaning:**")
        st.markdown("""
        1. **Direct Trial**: Stop oxygen directly and monitor on room air.
        2. **Success**: SpO2 stays above target during awake and sleep states.
        """)
    else:
        st.success("**✅ No Weaning Required**")

with c_dis:
    st.info("**🏠 Discharge Criteria:**")
    st.markdown(f"""
    - **SpO2 Stability**: ≥ {current_threshold}% on room air for **4-12 hours** (including a period of sleep).
    - **Feeding**: Consistent oral intake **> 50-75%** of normal volumes.
    - **Respiratory**: Stable WOB with no grunting or severe recessions.
    """)

if st.button("Start New Assessment"):
    st.rerun()
