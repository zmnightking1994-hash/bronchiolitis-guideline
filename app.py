import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Bronchiolitis Guideline 2025",
    page_icon="👶",
    layout="wide"
)

st.title("📑 Australasian Bronchiolitis Management Pathway (2025 Update)")
st.caption("Developed based on the PREDICT 2025 Guideline - Strict Severity Criteria")

# --- SECTION 1: RISK FACTORS ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks", help="Oxygen threshold is 92% for this group.")

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
    
    # Visual feedback for O2 threshold
    current_threshold = 92 if is_under_6_weeks else 90
    st.info(f"O2 Threshold for 'Mild' classification: {current_threshold}%")

# --- SECTION 3: REFINED SEVERITY LOGIC (PAGE 18) ---
severity = "Mild"

# 🚨 Severe Criteria (SpO2 < 87% is the key marker here)
if (effort == "Severe Recession / Grunting" or 
    spo2 < 87 or 
    behavior == "Lethargic / Altered Mental State" or 
    apnoea == "Observed" or 
    rr > 70):
    severity = "Severe"

# ⚠️ Moderate Criteria (SpO2 between 87% and threshold)
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
st.error("🚫 **DO NOT ROUTINELY USE:** Salbutamol, Steroids, Antibiotics, Chest X-rays, or Viral Swabs.")

col_plan, col_caution = st.columns([2, 1])

with col_plan:
    if severity == "Mild":
        st.success("### ✅ Intervention: Discharge & Home Care")
        st.markdown(f"""
        - **Oxygen:** Not indicated. Current SpO2 ({spo2}%) is acceptable.
        - **Hydration:** Oral fluids; encourage small frequent feeds.
        - **Criteria:** SpO2 > {current_threshold}% and adequate feeding.
        """)
    
    elif severity == "Moderate":
        st.warning("### ⚠️ Intervention: Hospital Observation")
        st.markdown(f"""
        - **Oxygen:** Target SpO2 ≥ {current_threshold}%. Start only if persistently below.
        - **Hydration:** NGT is preferred over IV if intake is < 50-75%.
        - **Note:** Avoid continuous monitoring if stable and not on oxygen.
        """)
    
    else:
        st.error("### 🚨 Intervention: Urgent / HDU Admission")
        st.markdown("""
        - **Support:** Consider CPAP or High Flow Oxygen.
        - **Fluids:** IV or NGT (consider 2/3 maintenance).
        - **Review:** Immediate Senior Clinician review required.
        """)

with col_caution:
    st.info("📌 **Clinical Pearls (2025 Guide):**")
    
    # Specific logic for the 87-90% trap
    if 87 <= spo2 < current_threshold and effort != "Severe Recession / Grunting":
        st.warning(f"**Note:** SpO2 is {spo2}%. This is **Moderate** as per guidelines. Do not escalate to 'Severe' treatment unless work of breathing worsens.")

    st.markdown("""
    - **Work of Breathing** is more important than the SpO2 number.
    - **NGT** is the preferred route for hydration.
    - **SARS-CoV-2:** Consider Dexamethasone only if positive AND hypoxaemic.
    """)



if st.button("New Patient Assessment"):
    st.rerun()
