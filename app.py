import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Gold Protocol 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Gold Version)")
st.caption("Integrated Protocol: RCH Melbourne, PREDICT & 2026 Safety Guidelines")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk Assessment")
is_under_6_weeks = st.checkbox("Infant age < 6 weeks")
risk_factors = st.multiselect("Risk Factors for Severe Illness:", ["Preterm birth", "CLD", "CHD", "Immunodeficiency"])

current_threshold = 92 if (is_under_6_weeks or risk_factors) else 90

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB):", ["Normal", "Mild", "Moderate", "Severe / Grunting"])
    behavior = st.radio("Behavioral State:", ["Normal / Alert", "Irritable", "Lethargic / Altered Mental State"])
with c2:
    feeding_status = st.radio("Current Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"])
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported", "Observed clinically"])
with c3:
    rr = st.number_input("RR (bpm):", 10, 150, 40)
    spo2 = st.slider("SpO2 %:", 70, 100, 96)
    st.info(f"💡 Target: ≥ {current_threshold}%")

# --- SECTION 3: SEPARATED LOGIC (التعديل الجديد هنا) ---

# تصنيف الشدة التنفسية
resp_severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or behavior == "Lethargic / Altered Mental State" or rr > 70):
    resp_severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or apnoea == "Reported"):
    resp_severity = "Moderate"

# تصنيف الشدة الغذائية مع حماية المسار الهوائي
# الطفل المثبط أو المصاب بانقطاع نفس ممنوع من الأكل فموياً
feeding_danger = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically")

# --- SECTION 4: MANAGEMENT PILLARS ---
st.divider()
st.header(f"Plan | Resp: {resp_severity} | Feeding Status: {'DANGER' if feeding_danger else 'Stable'}")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 Action: High Flow (HFNC) / CPAP**")
        st.markdown(f"""
        - **HFNC:** 2 L/kg/min | FiO2 40% (titrate to SpO2 ≥ {current_threshold}%).
        - **CPAP:** 5-7 cmH2O if HFNC fails or FiO2 > 50%.
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Action: Low Flow Oxygen (LFNP)**")
        st.write("- 0.5 - 2 L/min via nasal prongs.")
    else:
        st.success("**✅ Action: Monitoring Only**")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    if feeding_danger:
        st.error("**🚨 Action: NBM (Nil By Mouth) - SAFETY ALERT**")
        st.write("- **Reason:** High risk of aspiration due to Lethargy/Apnoea.")
        st.write("- **Hydration:** Start **NGT** at 66% maintenance.")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration**")
        st.write("- NGT preferred over IV at 66-75% maintenance.")
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- Breast/Formula feeding as tolerated.")

# --- SECTION 5: FAST TRACK & WEANING ---
st.divider()
if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled (SpO2 ≥ 95%)**")
else:
    with st.expander("📉 Weaning & Discharge Details"):
        st.markdown(f"""
        - **Wean O2:** Every 6h if SpO2 > {current_threshold}% for 2h.
        - **Standard Discharge:** SpO2 ≥ {current_threshold}% on air for 4-12h.
        """)
