import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="Bronchiolitis Guide 2026",
    page_icon="👶",
    layout="wide"
)

st.title("📑 Bronchiolitis Management Pathway (Final Gold Version)")
st.caption("Integrated Protocol: Based on RCH Melbourne & PREDICT Guidelines")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk & Threshold Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    # عامل العمر المعدل بناءً على طلبك (6 أسابيع)
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks")

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "Congenital Heart Disease", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# تحديد عتبة الأكسجين المستهدفة (Target SpO2)
# 92% للأطفال تحت 6 أسابيع أو ذوي الخطورة، و90% للبقية
has_risks = (is_under_6_weeks or len(risk_factors) > 0)
current_threshold = 92 if has_risks else 90

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
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

# --- SECTION 3: SEPARATED LOGIC (فصل منطق التنفس عن التغذية) ---

# 1. تصنيف الشدة التنفسية (Respiratory Severity)
# الخمول (Lethargic) أو الجهد الشديد أو انخفاض الإكسجين يجعل الحالة Severe
resp_severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or 
    behavior == "Lethargic / Altered Mental State" or rr > 70):
    resp_severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or apnoea == "Reported by parents"):
    resp_severity = "Moderate"

# 2. تصنيف حالة التغذية والأمان (Feeding Danger Logic)
# منع التغذية الفموية في حال الخمول أو انقطاع النفس الملحوظ حماية للمجرى التنفسي
feeding_danger = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically")

# --- SECTION 4: MANAGEMENT PILLARS ---
st.divider()
st.header(f"Management Plan | Resp: {resp_severity} | Feeding Status: {'DANGER' if feeding_danger else 'Stable'}")
st.error("🚫 **AVOID ROUTINE:** Salbutamol, Steroids, Antibiotics, X-rays, or Deep Suction.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 Action: High Flow (HFNC) / CPAP**")
        st.markdown(f"""
        - **HFNC Setup:** Start at **2 L/kg/min** | FiO2 at **40%** (titrate to keep SpO2 ≥ {current_threshold}%).
        - **Monitoring:** Continuous cardio-respiratory monitoring is mandatory.
        - **Escalation:** Consider **CPAP (5-7 cmH2O)** if HFNC fails or FiO2 > 50%.
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Action: Low Flow Oxygen (LFNP)**")
        st.markdown(f"""
        - **Device:** Nasal prongs at **0.5 - 2 L/min**.
        - **Note:** If no improvement after 2 hours, escalate to HFNC.
        """)
    else:
        st.success("**✅ Action: Monitoring Only**")
        st.write(f"- SpO2 {spo2}% is acceptable on Room Air.")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    if feeding_danger:
        st.error("**🚨 Action: NBM (Nil By Mouth) - SAFETY ALERT**")
        st.write("- **Reason:** High risk of aspiration due to Lethargy/Apnoea.")
        st.write("- **Hydration:** Start **NGT** (Nasogastric Tube) at **66% maintenance rate**.")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**🚨 Action: Active Hydration**")
        st.write("- **Route:** NGT is preferred over IV hydration.")
        st.write("- **Rate:** 66-75% of maintenance to avoid fluid overload.")
    elif feeding_status == "50-75% Intake":
        st.warning("**⚠️ Action: NGT Support**")
        st.write("- Supplemental bolus feeds via NGT (100% maintenance).")
    else:
        st.success("**✅ Action: Oral Feeding**")
        st.write("- Continue breast/formula feeds as tolerated.")

# --- SECTION 5: WEANING & DISCHARGE PROTOCOL ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

# منطق التخريج السريع (Fast Track) بناءً على طلبك
if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled:** Patient is stable with SpO2 ≥ 95%. Safe for immediate home discharge.")
else:
    col_wean, col_dis = st.columns(2)
    with col_wean:
        st.info("**📉 How to Wean Oxygen?**")
        st.markdown(f"""
        - **Step 1:** Trial off O2 every 6h if SpO2 > {current_threshold}% for 2 consecutive hours.
        - **Step 2 (HFNC):** Reduce FiO2 to 21% (Room Air) first, then cease flow.
        - **Step 3:** Stop continuous oximetry once off O2 for 2 hours and stable.
        """)
    with col_dis:
        st.info("**🏠 Standard Discharge Criteria:**")
        st.markdown(f"""
        - **SpO2:** Consistent ≥ {current_threshold}% on air for 4-12 hours (including sleep).
        - **Feeding:** Oral intake > 50-75% of normal volume.
        - **Stability:** No observed apnoea for > 24 hours.
        - **Education:** Family educated on 'Safety Netting' and follow-up.
        """)

if st.button("Start New Assessment"):
    st.rerun()
