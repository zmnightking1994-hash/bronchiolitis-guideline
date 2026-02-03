import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Guide 2025", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")
st.caption("Simplified Risk Entry | Separated Resp & Feeding Logic")

# --- SECTION 1: RISK ASSESSMENT (العودة للبساطة) ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    # العودة لنمط الاختيار البسيط
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks")

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors / Comorbidities:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "CHD", "Trisomy 21", "Tobacco Smoke"]
    )

# ضبط العتبة بناءً على العمر أو وجود مخاطر
has_risks = (is_under_6_weeks or len(risk_factors) > 0)
current_threshold = 92 if has_risks else 90

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing:", ["Normal", "Mild", "Moderate", "Severe / Grunting"])
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported by parents", "Observed clinically"])
with c2:
    feeding = st.radio("Feeding Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"])
    behavior = st.radio("Behavior:", ["Normal", "Irritable", "Lethargic / AMS"])
with c3:
    rr = st.number_input("Respiratory Rate (bpm):", 10, 150, 40)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96)
    st.info(f"💡 Target SpO2: {current_threshold}%")

# --- SECTION 3: SEPARATED LOGIC (تصنيف منفصل تماماً) ---

# 1. التصنيف التنفسي (Respiratory Severity)
# يعتمد على: الجهد، الأكسجين، انقطاع النفس، والوعي
resp_severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or rr > 70 or behavior == "Lethargic / AMS"):
    resp_severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or apnoea == "Reported by parents"):
    resp_severity = "Moderate"

# 2. التصنيف الغذائي (Feeding Severity)
# يعتمد فقط على كمية الرضاعة والجفاف
feed_severity = "Mild"
if feeding == "< 50% / Dehydration":
    feed_severity = "Severe"
elif feeding == "50-75% Intake":
    feed_severity = "Moderate"

# --- SECTION 4: MANAGEMENT PILLARS ---
st.divider()
st.header(f"Management Status | Resp: {resp_severity} | Feeding: {feed_severity}")

col_resp, col_hydra = st.columns(2)

# ركيزة الدعم التنفسي (مستقلة)
with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 Action: High Flow (HFNC) Escalation**")
        st.markdown(f"""
        - **Start HFNC:** 2 L/kg/min | FiO2 to keep SpO2 ≥ {current_threshold}%.
        - **Monitor:** Continuous HR, RR, and SpO2.
        - **Next:** Consider CPAP if FiO2 > 50% or apnoea persists.
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Action: Low Flow O2 (LFNP)**")
        st.write(f"- Standard Nasal Prongs if SpO2 < {current_threshold}%.")
    else:
        st.success("**✅ Action: Monitoring Only**")
        st.write(f"- SpO2 {spo2}% is acceptable on Room Air.")

# ركيزة الترطيب والتغذية (مستقلة)
with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    if apnoea == "Observed clinically":
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Safety:** High aspiration risk due to observed apnoea.")
        st.write("- Start **NGT** hydration at 66% maintenance.")
    elif feed_severity == "Severe":
        st.error("**🚨 Action: Active Hydration**")
        st.write("- Start **NGT** (preferred) or IV fluids at 66-75% maintenance.")
    elif feed_severity == "Moderate":
        st.warning("**⚠️ Action: NGT Support**")
        st.write("- Provide supplemental bolus feeds via NGT.")
    else:
        st.success("**✅ Action: Oral Feeding**")
        st.write("- Continue breastfeeding or formula as usual.")



# --- SECTION 5: WEANING & DISCHARGE ---
st.divider()
with st.expander("📝 Weaning & Discharge Checklist (RCH & PREDICT)"):
    st.markdown(f"""
    - **Weaning:** Trial off O2 every 6h if SpO2 > {current_threshold}% for 2h.
    - **Discharge:** SpO2 ≥ {current_threshold}% on air for 4-12h, and feeding > 50%.
    - **Note:** If feeding is poor but breathing is normal, focus on Pillar 2 only.
    """)

if st.button("Clear & New Patient"):
    st.rerun()
