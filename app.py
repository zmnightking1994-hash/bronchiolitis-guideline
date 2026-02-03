import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Bronchiolitis Guideline 2025",
    page_icon="👶",
    layout="wide"
)

st.title("📑 Australasian Bronchiolitis Management Pathway (2025 Update)")
st.caption("Incorporating strict 2025 severity criteria & Risk-adjusted O2 thresholds")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks")

with col_risks:
    # قائمة عوامل الخطر بناءً على الدليل
    risk_factors = st.multiselect(
        "Pre-existing Risk Factors / Comorbidities:",
        ["Preterm birth (< 37 weeks)", 
         "Chronic Lung Disease (CLD/BPD)", 
         "Hemodynamically significant CHD", 
         "Trisomy 21", 
         "Immunodeficiency", 
         "Tobacco Smoke Exposure"]
    )

# --- تحديث عتبة الأكسجين بناءً على ملاحظتك ---
# العتبة تكون 92 إذا كان العمر < 6 أسابيع أو وجد أي عامل خطر من القائمة
has_risks = len(risk_factors) > 0
current_threshold = 92 if (is_under_6_weeks or has_risks) else 90

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio(
        "Respiratory Effort (Work of Breathing):",
        ["Normal", "Mild Recession", "Moderate Recession", "Severe Recession / Grunting"]
    )
    behavior = st.radio(
        "Behavioral State:",
        ["Normal / Alert", "Irritable / Difficult to soothe", "Lethargic / Altered Mental State"]
    )

with c2:
    feeding = st.radio(
        "Hydration & Feeding:",
        ["Normal / Adequate", "50-75% of normal intake", "< 50% of normal intake / Dehydration"]
    )
    apnoea = st.selectbox("Apnoea History:", ["None", "Reported by parents", "Observed clinically"])

with c3:
    rr = st.number_input("Respiratory Rate (bpm):", min_value=10, max_value=150, value=40)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96)
    
    # تنبيه يوضح العتبة الحالية بناءً على المعطيات
    st.info(f"💡 Target SpO2 threshold for this patient is: {current_threshold}%")

# --- SECTION 3: REFINED SEVERITY LOGIC (PAGE 18) ---
severity = "Mild"

# 🚨 Severe Criteria (SpO2 < 87% is the absolute threshold for Severe)
if (effort == "Severe Recession / Grunting" or 
    spo2 < 87 or 
    behavior == "Lethargic / Altered Mental State" or 
    apnoea == "Observed" or 
    rr > 70):
    severity = "Severe"

# ⚠️ Moderate Criteria (SpO2 between 87% and the adjusted threshold)
elif (effort == "Moderate Recession" or 
      (87 <= spo2 < current_threshold) or 
      (50 <= rr <= 70) or 
      feeding != "Normal / Adequate" or 
      apnoea == "Reported by parents" or 
      behavior == "Irritable / Difficult to soothe"):
    severity = "Moderate"

# --- SECTION 4: INTEGRATED INTERVENTIONS ---
st.divider()
st.header(f"Final Classification: {severity}")

# Strong Recommendations (The "Don'ts")
st.error("🚫 **GUIDELINE RESTRICTIONS:** Do not routinely use Salbutamol, Steroids, Antibiotics, Chest X-rays, or Viral Swabs.")

col_plan, col_caution = st.columns([2, 1])

with col_plan:
    if severity == "Mild":
        st.success("### ✅ Intervention: Discharge & Home Care")
        st.markdown(f"""
        - **Oxygen:** Not indicated. SpO2 of {spo2}% is acceptable.
        - **Fluids:** Maintain oral hydration.
        - **Criteria:** Patient stable with SpO2 > {current_threshold}%.
        """)
    
    elif severity == "Moderate":
        st.warning("### ⚠️ Intervention: Hospital Observation")
        st.markdown(f"""
        - **Oxygen:** Target SpO2 ≥ {current_threshold}%.
        - **Hydration:** NGT is the preferred route if oral intake is poor (< 50-75%).
        - **Observation:** Clinical assessment using Early Warning Tools.
        """)
    
    else:
        st.error("### 🚨 Intervention: Urgent / HDU Admission")
        st.markdown("""
        - **Support:** Consider CPAP or High Flow Nasal Cannula.
        - **Fluids:** IV or NGT fluids (Restricted maintenance).
        - **Review:** Immediate Senior Clinician review required.
        """)

with col_caution:
    st.info("📌 **Clinical Notes:**")
    
    # توضيح حالة الأكسجين "الخادعة"
    if 87 <= spo2 < current_threshold and effort != "Severe Recession / Grunting":
        st.warning(f"**O2 Caution:** SpO2 is {spo2}%. This is **Moderate** as per the 2025 update. Do not escalate unless respiratory effort increases.")

    st.markdown(f"""
    - **Custom Threshold:** Because of {'risk factors' if has_risks else 'age'}, the O2 target is {current_threshold}%.
    - **Hydration:** NGT is preferred over IV.
    - **SARS-CoV-2:** Consider Dexamethasone only if positive AND hypoxaemic.
    """)

if st.button("New Patient Assessment"):
    st.rerun()
