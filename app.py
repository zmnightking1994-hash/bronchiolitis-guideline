import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Gold Standard 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Comprehensive Version)")
st.caption("Integrated Protocol: RCH Melbourne, PREDICT & 2026 Safety Guidelines")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks") # تم التعديل لـ 6 أسابيع

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "Congenital Heart Disease", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# ضبط عتبة الأكسجين المستهدفة
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

# --- 3. SEPARATED SAFETY LOGIC ---

# تصنيف الشدة التنفسية (Respiratory Severity)
resp_severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or 
    behavior == "Lethargic / Altered Mental State" or rr > 70):
    resp_severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or apnoea == "Reported by parents"):
    resp_severity = "Moderate"

# حماية المجرى التنفسي (Feeding Safety Logic)
# يُمنع الإرضاع الفموي في 3 حالات: جهد شديد، خمول، أو انقطاع نفس ملحوظ
is_unsafe_to_feed = (
    behavior == "Lethargic / Altered Mental State" or 
    apnoea == "Observed clinically" or 
    effort == "Severe / Grunting"
)

# --- 4. DETAILED MANAGEMENT PILLARS ---
st.divider()
st.header(f"Management Plan | Resp: {resp_severity} | Feeding Status: {'⚠️ NBM REQUIRED' if is_unsafe_to_feed else 'Stable'}")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Detailed Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 High Flow (HFNC) & Escalation Protocol:**")
        st.markdown(f"""
        1. **High Flow Nasal Cannula (HFNC):**
           - **Flow Rate:** Start at **2 L/kg/min** (Max 20-25 L/min).
           - **FiO2:** Start at **40%** and titrate to keep SpO2 ≥ {current_threshold}%.
           - **Monitoring:** **Continuous** heart rate, RR, and SpO2.
        
        2. **CPAP (If HFNC Fails):**
           - **Criteria:** Persistent apnoea, FiO2 > 50% on HFNC, or worsening acidosis/effort.
           - **Pressure:** Start at **5 - 7 cmH2O**.
           - **Note:** Transfer to ICU/HDU environment.
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Low Flow Oxygen (LFNP):**")
        st.markdown(f"""
        - **Device:** Nasal prongs at **0.5 - 2 L/min**.
        - **Goal:** Maintain SpO2 ≥ {current_threshold}%.
        - **Trial:** If stable for 2h, attempt trial off O2.
        """)
    else:
        st.success("**✅ Action: Monitoring Only**")
        st.write(f"- SpO2 {spo2}% is adequate on room air.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Detailed Hydration")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.markdown(f"""
        - **Reason:** High aspiration risk due to **{'Severe Effort' if effort == 'Severe / Grunting' else 'Altered Consciousness/Apnoea'}**.
        - **Method:** Start **NGT** (Nasogastric Tube) hydration.
        - **Rate:** Restricted to **66% of maintenance** to avoid fluid overload/SIADH.
        """)
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration**")
        st.write("- Start **NGT** (preferred) at 66-75% maintenance.")
    elif feeding_status == "50-75% Intake":
        st.warning("**Action: NGT Bolus Support**")
        st.write("- Supplemental NGT feeds to ensure 100% maintenance.")
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- Continue breast/formula feeds as tolerated.")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol (Detailed)")

# منطق التخريج السريع (Fast Track)
if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled:** SpO2 ≥ 95% + Stable Clinical State. Safe for home.")
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Oxygen Weaning (How to stop O2):**")
        st.markdown(f"""
        - **When to start:** If SpO2 is consistently > {current_threshold+2}% for 2 hours.
        - **HFNC Weaning:** 1. Reduce FiO2 to **21% (Room Air)**.
            2. If stable for 2h on 21% FiO2, stop HFNC flow.
        - **Low Flow Weaning:** Trial off O2 directly to room air.
        - **Trial Frequency:** Attempt weaning every **6-12 hours** (ideally when awake).
        """)
    with c_dis:
        st.info("**🏠 Standard Discharge Criteria:**")
        st.markdown(f"""
        - **Oxygen:** SpO2 ≥ {current_threshold}% on room air for **4-12 hours** (must include a period of sleep).
        - **Feeding:** Oral intake consistently > 50-75% of normal volumes.
        - **Work of Breathing:** Stable (Normal or Mild) with no grunting.
        - **Social:** Parents confident and have access to follow-up.
        """)



if st.button("Start New Assessment"):
    st.rerun()
