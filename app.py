import streamlit as st

# Page setup
st.set_page_config(page_title="Bronchiolitis Guideline", layout="wide")

st.title("📑 Bronchiolitis Management Pathway")

# --- SECTION 1: RISK FACTORS ---
st.subheader("1. Pre-existing Risk Factors")
with st.expander("Click to select risk factors", expanded=True):
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        age_risk = st.checkbox("Age < 6 weeks")
        preterm = st.checkbox("Preterm birth (< 37 weeks)")
    with col_r2:
        cardiac = st.checkbox("Hemodynamically significant CHD")
        chronic_lung = st.checkbox("Chronic Lung Disease / Immunodeficiency")

if any([age_risk, preterm, cardiac, chronic_lung]):
    st.warning("⚠️ High Risk: Lower threshold for admission and frequent review required.")

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
st.subheader("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio(
        "Respiratory Effort:",
        ["Normal", "Mild Recession", "Moderate Recession", "Severe Recession / Grunting"],
        index=0
    )
    behavior = st.radio(
        "Behavioral State:",
        ["Normal / Alert", "Irritable / Difficult to soothe", "Lethargic / Reduced response"],
        index=0
    )

with c2:
    feeding = st.radio(
        "Feeding Status (Oral intake):",
        ["Normal", "50-75% of normal", "< 50% of normal"],
        index=0
    )
    apnoea = st.selectbox("Apnoea:", ["None", "Reported", "Observed"])

with c3:
    hr = st.number_input("Heart Rate (bpm):", min_value=30, max_value=250, value=120)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 80, 100, 96)

# --- SECTION 3: LOGIC ---
# Using criteria from bronchioritis.xlsx
severity = "Mild"

# Severe Criteria
if (effort == "Severe Recession / Grunting" or 
    spo2 < 90 or 
    behavior == "Lethargic / Reduced response" or 
    feeding == "< 50% of normal" or 
    apnoea == "Observed"):
    severity = "Severe"

# Moderate Criteria
elif (effort == "Moderate Recession" or 
      (90 <= spo2 < 92) or 
      behavior == "Irritable / Difficult to soothe" or 
      feeding == "50-75% of normal" or
      apnoea == "Reported"):
    severity = "Moderate"

# --- SECTION 4: FINAL DISPOSITION ---
st.divider()
st.header(f"Result: {severity} Bronchiolitis")

if severity == "Mild":
    st.success("✅ Management: Home Care")
    st.markdown("""
    **Discharge Criteria:**
    * SpO2 > 92% on air
    * Feeding > 75% of normal
    * Caregivers feel confident at home
    """)

elif severity == "Moderate":
    st.warning("⚠️ Management: Hospital Observation")
    st.markdown("""
    **Interventions:**
    * Oxygen if SpO2 persistently < 92%
    * Consider NGT if feeding is 50-75%
    * Minimal handling
    """)

else:
    st.error("🚨 Management: URGENT / HDU")
    st.markdown("""
    **Immediate Action:**
    * Senior clinical review required
    * Consider CPAP or High Flow Oxygen
    * NG or IV fluids (1/2 to 2/3 maintenance)
    """)

if st.button("New Assessment"):
    st.rerun()
