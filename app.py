import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Bronchiolitis Guideline 2025",
    page_icon="👶",
    layout="wide"
)

st.title("📑 Australasian Bronchiolitis Management Pathway (2025 Update)")
st.caption("Final Version: Specialized Management Pillars (Respiratory & Hydration)")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks")

with col_risks:
    risk_factors = st.multiselect(
        "Pre-existing Risk Factors / Comorbidities:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease (CLD/BPD)", 
         "Hemodynamically significant CHD", "Trisomy 21", 
         "Immunodeficiency", "Tobacco Smoke Exposure"]
    )

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
    st.info(f"💡 Target SpO2 threshold: {current_threshold}%")

# --- SECTION 3: SEVERITY LOGIC ---
severity = "Mild"
if (effort == "Severe Recession / Grunting" or spo2 < 87 or 
    behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or 
    feeding == "< 50% of normal intake / Dehydration" or rr > 70):
    severity = "Severe"
elif (effort == "Moderate Recession" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or 
      feeding == "50-75% of normal intake" or apnoea == "Reported by parents" or 
      behavior == "Irritable / Difficult to soothe"):
    severity = "Moderate"

# --- SECTION 4: MANAGEMENT PILLARS ---
st.divider()
st.header(f"Clinical Classification: {severity}")
st.error("🚫 **DO NOT ROUTINELY USE:** Salbutamol, Steroids, Antibiotics, X-rays, or Viral Swabs.")

col_resp, col_hydra = st.columns(2)

# Pillar 1: Respiratory Support
with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if severity == "Mild":
        st.success("**Plan: No Oxygen Required**")
        st.write(f"- SpO2 is {spo2}% (Acceptable ≥ {current_threshold}%).")
        st.write("- Routine suction is NOT recommended.")
    elif severity == "Moderate":
        st.warning("**Plan: Observation & Low Flow O2**")
        st.write(f"- Start low-flow O2 only if SpO2 persistently < {current_threshold}%.")
        st.write("- Avoid High Flow (HFNC) as first-line therapy.")
    else:
        st.error("**Plan: Urgent Escalation**")
        st.write("- Consider CPAP or High Flow Nasal Cannula (HFNC).")
        st.write("- Immediate senior clinical review for HDU/ICU.")

# Pillar 2: Hydration & Nutrition
with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    if feeding == "Normal / Adequate":
        st.success("**Plan: Oral Feeding**")
        st.write("- Continue breastfeeding or usual formula.")
        st.write("- Encourage small, frequent feeds if effort increases.")
    elif feeding == "50-75% of normal intake":
        st.warning("**Plan: Nutritional Support**")
        st.write("- Nasogastric Tube (NGT) hydration is preferred over IV.")
        st.write("- Provide 100% maintenance fluids.")
    else:
        st.error("**Plan: Active Hydration**")
        st.write("- Start NGT or IV fluids.")
        st.write("- Consider restricting to 2/3 maintenance to avoid fluid overload.")

# Safety Netting and Discharge
st.divider()
with st.expander("📝 Additional Notes & Discharge Criteria"):
    st.markdown(f"""
    - **Discharge if:** SpO2 > {current_threshold}% on air for 4 hours, feeding > 50-75%, and parents are confident.
    - **Note:** Nasal suction only for infants with nasal blockage or before feeding.
    - **COVID-19:** If positive and hypoxaemic, consider Dexamethasone.
    """)

if st.button("New Assessment"):
    st.rerun()
