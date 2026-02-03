import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Gold Standard 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Gold Version)")
st.caption("Comprehensive Protocol: RCH Melbourne, PREDICT & 2026 Guidelines")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    # واجهة العمر البسيطة كما فضلت
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks")

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "CHD", "Trisomy 21", "Tobacco smoke exposure"]
    )

# ضبط عتبة الأكسجين بناءً على المخاطر
current_threshold = 92 if (is_under_6_weeks or risk_factors) else 90

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

# --- SECTION 4: MANAGEMENT PILLARS (التدبير التفصيلي) ---
st.divider()
st.header(f"Management Status | Resp: {resp_severity} | Feeding: {feed_severity}")
st.error("🚫 **AVOID ROUTINE:** Salbutamol, Steroids, Antibiotics, X-rays, and Viral Swabs.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 Action: High Flow (HFNC) & Escalation**")
        st.markdown(f"""
        - **HFNC Setup:** Start at **2 L/kg/min** (Max 25L) | FiO2 at **40%** (titrate to keep SpO2 ≥ {current_threshold}%).
        - **Monitoring:** **Continuous** cardio-respiratory monitoring is mandatory.
        - **Escalation to CPAP:** Consider **CPAP (5-7 cmH2O)** if FiO2 > 50%, persistent apnoea, or worsening acidosis.
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Action: Low Flow Oxygen (LFNP)**")
        st.markdown(f"""
        - **Device:** Nasal prongs at **0.5 - 2 L/min**.
        - **Goal:** Keep SpO2 ≥ {current_threshold}%.
        - **Note:** If no improvement after 2h, escalate to HFNC.
        """)
    else:
        st.success("**✅ Action: Monitoring Only**")
        st.write(f"- SpO2 {spo2}% is stable on Room Air. No supplemental O2 required.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    if apnoea == "Observed clinically":
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Safety:** High aspiration risk due to apnoea. Stop oral feeds.")
        st.write("- Start **NGT** hydration at **66% maintenance**.")
    elif feed_severity == "Severe":
        st.error("**🚨 Action: Active Hydration**")
        st.write("- Start **NGT** (preferred) or IV fluids at **66-75% maintenance**.")
    elif feed_severity == "Moderate":
        st.warning("**⚠️ Action: NGT Support**")
        st.write("- Provide 100% maintenance via NGT boluses.")
    else:
        st.success("**✅ Action: Oral Feeding**")
        st.write("- Continue breast/formula feeds as tolerated.")

# --- SECTION 5: DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Discharge & Weaning Protocol (The 'Fast Track' logic)")

# معيار الـ 95% للتخريج الفوري الذي طلبته
if spo2 >= 95 and effort == "Normal" and feeding == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled:** Patient is stable with SpO2 ≥ 95%. Safe for immediate home discharge.")
else:
    c_wean1, c_wean2 = st.columns(2)
    with c_wean1:
        st.info("**📉 How to Wean Oxygen?**")
        st.markdown(f"""
        - **Step 1:** Trial off O2 every 6h if SpO2 > {current_threshold}% for 2 consecutive hours.
        - **Step 2 (HFNC):** Reduce FiO2 to 21% (Room Air) first, then cease flow.
        - **Step 3:** Stop continuous oximetry once off O2 for 2h and stable.
        """)
    with c_wean2:
        st.info("**🏠 Standard Discharge Criteria:**")
        st.markdown(f"""
        - SpO2 ≥ {current_threshold}% on air for 4-12 hours (including sleep).
        - Oral intake > 50-75% of normal volume.
        - No observed apnoea for > 24 hours.
        - Parents confident in home management.
        """)

if st.button("Start New Assessment"):
    st.rerun()
