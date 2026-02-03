import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Gold Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Clinical Version)")
st.caption("Integrated Protocol: Global Evidence-Based Standards with Practical Safety Checks")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    # تم إصلاح الخطأ البرمجي هنا (تأكد من تعريف المتغير بشكل صحيح)
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks (Apnoea High Risk)") 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease (CLD)", "Congenital Heart Disease (CHD)", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# عتبة الأكسجين: 92% للحالات عالية الخطورة [cite: 32]، و90% للحالات المستقرة عالمياً[cite: 11].
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

# --- 3. SAFETY & SEVERITY LOGIC ---
resp_severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or 
    behavior == "Lethargic / Altered Mental State" or rr > 70): # [cite: 25, 28, 29]
    resp_severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or apnoea == "Reported by parents"):
    resp_severity = "Moderate"

# حماية المجرى التنفسي: يُمنع الإرضاع فموياً في الجهد الشديد، الخمول، أو انقطاع النفس[cite: 78, 82].
is_unsafe_to_feed = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting")

# --- 4. DETAILED MANAGEMENT PILLARS ---
st.divider()
st.header(f"Management Plan | Resp: {resp_severity} | Feeding Status: {'⚠️ NBM REQUIRED' if is_unsafe_to_feed else 'Stable'}")
st.error("🚫 **AVOID ROUTINE:** Salbutamol, Steroids, Antibiotics, X-rays, or Deep Suction.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 High Flow (HFNC) & Escalation Protocol:**")
        st.markdown(f"""
        - **HFNC Flow:** نبدأ بـ **2 L/kg/min** (الحد الأقصى 25L)[cite: 86, 88].
        - **FiO2:** نبدأ بـ **40%** وتعديلها للحفاظ على إشباع ≥ {current_threshold}%[cite: 89].
        - **Gastric Safety:** وضع **venting NGT** (تفريغي) لتقليل انتفاخ المعدة.
        - **CPAP Escalation:** يُستعمل في حال فشل HFNC (FiO2 > 50%) أو انقطاع نفس مستمر[cite: 104, 106].
        - **CPAP Settings:** الضغط **5-7 cmH2O** (اليقظة) وقد يصل لـ 10 عند النوم.
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Low Flow Oxygen (LFNP):**")
        st.write(f"- 0.5 - 2 L/min للحفاظ على أكسجة ≥ {current_threshold}%[cite: 60].")
    else:
        st.success("**✅ Action: Monitoring Only**")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Method:** NGT (Nasogastric Tube) أو وريدي[cite: 78, 83].")
        st.write("- **Rate:** تحديد السوائل بـ **66-75% من الصيانة** (للحماية من SIADH)[cite: 78].")
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration**")
        st.write("- NGT بمعدل 66-75% من الصيانة[cite: 83].")
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- متابعة الرضاعة الطبيعية حسب التحمل[cite: 60].")

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

# مسار التخريج السريع (Fast Track) بناءً على طلبك
if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge:** المريض مستقر (SpO2 ≥ 95%). جاهز للتخريج المباشر مع توصيات للمنزل.")
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Weaning (الفطام):**")
        st.markdown(f"""
        - **HFNC:** تقليل FiO2 لـ 21% أولاً، ثم إيقاف الجريان تدريجياً[cite: 122, 123].
        - **التكرار:** التقييم كل 4-6 ساعات[cite: 121].
        - **علامات الفشل:** زيادة النبض > 20 أو التنفس > 10.
        """)
    with c_dis:
        st.info("**🏠 Discharge Criteria (المعايير):**")
        st.markdown(f"""
        - أكسجة ≥ {current_threshold}% على هواء الغرفة لمدة 4-12 ساعة (تشمل النوم)[cite: 66, 91].
        - وارد فموي > 50-75% من المعتاد[cite: 56].
        - عدم وجود طحة أو جهد تنفسي شديد[cite: 96, 111].
        """)

if st.button("Start New Assessment"):
    st.rerun()
