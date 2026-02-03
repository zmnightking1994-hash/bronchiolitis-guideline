import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Clinical Guide 2025", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Gold Version)")
st.caption("Integrated Protocol: RCH Melbourne & PREDICT 2025 Guidelines")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    # العودة لنمط الاختيار البسيط كما طلبت
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks")

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Chronic Lung Disease", "Congenital Heart Disease", "Gestational age <37 weeks", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# ضبط العتبة (Target SpO2) بناءً على عوامل الخطورة
has_risks = (is_under_6_weeks or len(risk_factors) > 0)
current_threshold = 92 if has_risks else 90

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB):", ["Normal", "Mild", "Moderate", "Severe / Grunting"])
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported by parents", "Observed clinically"])
with c2:
    feeding = st.radio("Feeding Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"])
    behavior = st.radio("Behavior:", ["Normal", "Irritable", "Lethargic / AMS"])
with c3:
    rr = st.number_input("Respiratory Rate (bpm):", 10, 150, 40)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96)
    st.info(f"💡 Clinical Target: SpO2 ≥ {current_threshold}%")

# --- SECTION 3: SEPARATED LOGIC (فصل منطق التنفس عن التغذية) ---

# 1. تصنيف الشدة التنفسية (Respiratory Severity)
resp_severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or rr > 70 or behavior == "Lethargic / AMS"):
    resp_severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or apnoea == "Reported by parents"):
    resp_severity = "Moderate"

# 2. تصنيف الشدة الغذائية (Feeding Severity)
feed_severity = "Mild"
if feeding == "< 50% / Dehydration":
    feed_severity = "Severe"
elif feeding == "50-75% Intake":
    feed_severity = "Moderate"

# --- SECTION 4: MANAGEMENT PILLARS ---
st.divider()
st.header(f"Management Plan | Resp: {resp_severity} | Feeding: {feed_severity}")

col_resp, col_hydra = st.columns(2)

# الركيزة التنفسية: تعتمد فقط على المعايير التنفسية
with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 Action: High Flow (HFNC) / CPAP**")
        st.markdown(f"""
        - **HFNC Setup:** Start at **2 L/kg/min** | FiO2 at **40%** (titrate to SpO2 ≥ {current_threshold}%).
        - **Escalation:** Consider **CPAP (5-7 cmH2O)** if HFNC fails or FiO2 > 50%.
        - **Monitoring:** Continuous cardio-respiratory monitoring mandatory.
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Action: Low Flow Oxygen (LFNP)**")
        st.write(f"- Use nasal prongs at **0.5 - 2 L/min** to maintain SpO2 ≥ {current_threshold}%.")
    else:
        st.success("**✅ Action: Monitoring Only**")
        st.write(f"- SpO2 {spo2}% is stable on Room Air. No O2 needed.")

# الركيزة الغذائية: تعتمد على التغذية وخطر الاستنشاق
with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    if apnoea == "Observed clinically":
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Safety:** High risk of aspiration during apnoea episodes.")
        st.write("- Start **NGT** hydration at **66% maintenance**.")
    elif feed_severity == "Severe":
        st.error("**🚨 Action: Active Hydration**")
        st.write("- Start **NGT** (preferred) or IV fluids at **66-75% maintenance**.")
    elif feed_severity == "Moderate":
        st.warning("**⚠️ Action: NGT Support**")
        st.write("- Supplemental bolus feeds via NGT (100% maintenance).")
    else:
        st.success("**✅ Action: Oral Feeding**")
        st.write("- Continue breast/formula feeding as tolerated.")

# --- SECTION 5: DISCHARGE PROTOCOL (Fast Track included) ---
st.divider()
st.subheader("🏥 Discharge & Weaning Protocol")

if spo2 >= 95 and effort == "Normal" and feeding == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge:** Patient is stable with SpO2 ≥ 95%. Safe for home discharge with primary care follow-up.")
else:
    c_wean1, c_wean2 = st.columns(2)
    with c_wean1:
        st.info("**Weaning Plan**")
        st.markdown(f"""
        - Trial off O2 every 6h if SpO2 > {current_threshold}% for 2h.
        - For HFNC: Reduce FiO2 to 21% before ceasing flow.
        """)
    with c_wean2:
        st.info("**Standard Discharge Criteria**")
        st.markdown(f"""
        - SpO2 ≥ {current_threshold}% on air for 4-12 hours.
        - Oral intake > 50-75% of normal volume.
        - No observed apnoea for > 24 hours.
        """)


if st.button("Clear Assessment"):
    st.rerun()
