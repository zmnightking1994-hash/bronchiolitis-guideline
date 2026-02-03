import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Bronchiolitis Guideline 2025",
    page_icon="👶",
    layout="wide"
)

st.title("📑 Australasian Bronchiolitis Management Pathway (2025 Update)")
st.caption("Final Version: Strict Severity & Risk-Adjusted Criteria")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks")

with col_risks:
    risk_factors = st.multiselect(
        "Pre-existing Risk Factors / Comorbidities:",
        ["Preterm birth (< 37 weeks)", 
         "Chronic Lung Disease (CLD/BPD)", 
         "Hemodynamically significant CHD", 
         "Trisomy 21", 
         "Immunodeficiency", 
         "Tobacco Smoke Exposure"]
    )

# Logic for O2 Threshold: 92% if <6w OR has any risk factor, else 90%
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
    st.info(f"💡 Target SpO2 threshold for this patient: {current_threshold}%")

# --- SECTION 3: REFINED SEVERITY LOGIC (STRICT 2025) ---
severity = "Mild"

# 🚨 Severe Criteria: High priority markers that trigger 'Severe' status
if (effort == "Severe Recession / Grunting" or 
    spo2 < 87 or 
    behavior == "Lethargic / Altered Mental State" or 
    apnoea == "Observed clinically" or # Strong marker
    feeding == "< 50% of normal intake / Dehydration" or # Strong marker
    rr > 70):
    severity = "Severe"

# ⚠️ Moderate Criteria
elif (effort == "Moderate Recession" or 
      (87 <= spo2 < current_threshold) or 
      (50 <= rr <= 70) or 
      feeding == "50-75% of normal intake" or 
      apnoea == "Reported by parents" or 
      behavior == "Irritable / Difficult to soothe"):
    severity = "Moderate"

# --- SECTION 4: INTEGRATED INTERVENTIONS ---
st.divider()
st.header(f"Clinical Classification: {severity}")

# Global Warning for all categories
st.error("🚫 **GUIDELINE RESTRICTIONS:** Do not routinely use Salbutamol, Steroids, Antibiotics, Chest X-rays, or Viral Swabs.")

col_plan, col_caution = st.columns([2, 1])

with col_plan:
    if severity == "Mild":
        st.success("### ✅ Intervention: Home Care (Discharge)")
        st.markdown(f"""
        - **Oxygen:** Not indicated. SpO2 {spo2}% is safe.
        - **Feeding:** Continue oral hydration. Discharge if > 50-75% of normal.
        - **Advice:** Provide clear safety-netting instructions for parents.
        """)
    
    elif severity == "Moderate":
        st.warning("### ⚠️ Intervention: Hospital Observation")
        st.markdown(f"""
        - **Oxygen:** Titrate only if SpO2 is persistently < {current_threshold}%.
        - **Hydration:** NGT is preferred over IV if oral intake is poor.
        - **Monitoring:** Periodic clinical review (avoid unnecessary continuous oximetry).
        """)
    
    else:
        st.error("### 🚨 Intervention: Urgent Admission / HDU")
        st.markdown(f"""
        - **Respiratory Support:** Consider CPAP or High Flow Nasal Cannula (HFNC).
        - **Fluids:** IV or NGT (consider 2/3 maintenance to avoid fluid overload).
        - **Clinical:** Immediate Senior Clinician review is mandatory.
        """)

with col_caution:
    st.info("📌 **Critical Clinical Pearls:**")
    
    # Context-specific warning for SpO2 "Gray Zone"
    if 87 <= spo2 < current_threshold and effort != "Severe Recession / Grunting":
        st.warning(f"**Clinical Note:** SpO2 is {spo2}%. Classified as **Moderate** because SpO2 is ≥ 87%. Ensure overall clinical stability.")
    
    st.markdown(f"""
    - **Apnoea & Feeding:** Because these were flagged as severe/moderate, the status has been adjusted accordingly.
    - **O2 Target:** {current_threshold}% (Adjusted for {'age/risks' if (is_under_6_weeks or has_risks) else 'normal profile'}).
    - **NGT vs IV:** NGT hydration is safer and reduces hospital stay.
    """)



if st.button("Start New Assessment"):
    st.rerun()
