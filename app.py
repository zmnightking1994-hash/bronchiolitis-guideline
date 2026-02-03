import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Bronchiolitis Guideline 2025",
    page_icon="👶",
    layout="wide"
)

st.title("📑 Bronchiolitis Clinical Pathway (2025 Update)")
st.caption("Based on the Australasian Bronchiolitis Guideline: 2025 Update")

# --- SECTION 1: RISK FACTORS & AGE ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks", help="Threshold for oxygen is higher (92%) for this group.")

with col_risks:
    risk_factors = st.multiselect(
        "Pre-existing Risk Factors:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease", "Congenital Heart Disease", 
         "Trisomy 21", "Immunodeficiency", "Tobacco Smoke Exposure"]
    )

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio(
        "Respiratory Effort (Work of Breathing):",
        ["Normal", "Mild Recession", "Moderate Recession", "Severe Recession / Grunting"],
        help="The primary pillar of severity assessment."
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
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 80, 100, 96)
    st.info(f"O2 Threshold for this patient: {'92%' if is_under_6_weeks else '90%'}")

# --- SECTION 3: REFINED SEVERITY LOGIC (2025) ---
severity = "Mild"
o2_threshold = 92 if is_under_6_weeks else 90

# Severe Logic
if (effort == "Severe Recession / Grunting" or 
    behavior == "Lethargic / Altered Mental State" or 
    apnoea == "Observed" or 
    rr > 70 or 
    spo2 < 88): # Very low SpO2 is always a concern
    severity = "Severe"

# Moderate Logic
elif (effort == "Moderate Recession" or 
      spo2 < o2_threshold or 
      (50 <= rr <= 70) or 
      feeding != "Normal / Adequate" or 
      apnoea == "Reported by parents" or 
      behavior == "Irritable / Difficult to soothe"):
    severity = "Moderate"

# --- SECTION 4: INTEGRATED INTERVENTIONS & NOTES ---
st.divider()
st.header(f"Clinical Classification: {severity}")

# High-priority warnings (The "Don'ts" from the 2025 Guide)
st.error("🚫 **AVOID ROUTINE:** Salbutamol, Steroids, Antibiotics, Chest X-rays, and Viral Swabs.")

col_plan, col_caution = st.columns([2, 1])

with col_plan:
    if severity == "Mild":
        st.success("### ✅ Management: Home Care")
        st.markdown(f"""
        - **Oxygen:** Not indicated. SpO2 of {spo2}% is acceptable.
        - **Fluids:** Encourage frequent small oral feeds.
        - **Suction:** Superficial nasal suction only if needed for feeding.
        - **Discharge Criteria:** Maintain SpO2 > {o2_threshold}% and feeding > 50-75%.
        """)
    
    elif severity == "Moderate":
        st.warning("### ⚠️ Management: Hospital Observation")
        st.markdown(f"""
        - **Oxygen:** Only if SpO2 is persistently < {o2_threshold}%. Aim for {o2_threshold}%.
        - **Fluids:** NGT is preferred over IV if oral intake < 50-75%. 
        - **Monitoring:** Avoid continuous oximetry if the infant is stable and not on oxygen.
        - **Escalation:** Do not use High Flow (HF) as first-line therapy.
        """)
    
    else:
        st.error("### 🚨 Management: Urgent / HDU Admission")
        st.markdown("""
        - **Respiratory Support:** Consider CPAP or High Flow Oxygen.
        - **Fluids:** IV or NGT (Restrict to 2/3 maintenance to prevent SIADH/Fluid overload).
        - **Clinical:** Immediate Senior Review Required.
        """)

with col_caution:
    st.info("💡 **Clinical Pearls:**")
    # Smart Oxygen Note
    if spo2 < o2_threshold and effort == "Normal":
        st.warning(f"**O2 Caution:** SpO2 is <{o2_threshold}% but effort is normal. 2025 guidelines advise against escalation for 'isolated hypoxaemia' if the child is clinically well.")
    
    st.markdown("""
    - **Work of Breathing** is a more reliable indicator than SpO2.
    - **Nasogastric (NGT)** hydration is safer and preferred over IV fluids.
    - **SARS-CoV-2:** If positive AND hypoxaemic, consider Dexamethasone.
    """)

# Reset Button
if st.button("New Assessment"):
    st.rerun()
