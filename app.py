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
    rr = st.number_input("Respiratory Rate (breaths/min):", min_value=10, max_value=150, value=40)
    hr = st.number_input("Heart Rate (bpm):", min_value=30, max_value=250, value=120)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 80, 100, 96)

# --- SECTION 3: SEVERITY LOGIC ---
severity = "Mild"
if (effort == "Severe Recession / Grunting" or spo2 < 90 or rr > 70 or 
    behavior == "Lethargic / Reduced response" or feeding == "< 50% of normal" or apnoea == "Observed"):
    severity = "Severe"
elif (effort == "Moderate Recession" or (90 <= spo2 < 92) or (50 <= rr <= 70) or
      behavior == "Irritable / Difficult to soothe" or feeding == "50-75% of normal" or apnoea == "Reported"):
    severity = "Moderate"

# --- SECTION 4: INTEGRATED INTERVENTIONS ---
st.divider()
st.header(f"Result: {severity} Bronchiolitis")

# General Clinical Notes (The "Don'ts")
st.error("🚫 **DO NOT ROUTINELY USE:** Salbutamol, Steroids, Antibiotics, Chest X-rays, or Viral Swabs.")

if severity == "Mild":
    st.success("### ✅ Intervention: Home Care (Discharge)")
    st.markdown("""
    * **Feeding:** Ensure oral intake > 75%. Encourage small frequent feeds.
    * **Suction:** Nasal suction only if nose is blocked.
    * **Discharge Criteria:** SpO2 > 92% on air and stable clinical state.
    * **Safety Net:** Advise parents to return if effort increases or feeding drops.
    """)

elif severity == "Moderate":
    st.warning("### ⚠️ Intervention: Hospital Observation")
    st.markdown("""
    * **Oxygen:** Titrate to maintain SpO2 > 92%.
    * **Feeding:** Consider Nasogastric Tube (NGT) if intake is 50-75%.
    * **Monitoring:** Regular clinical assessment and minimal handling.
    * **Support:** Ensure parental confidence and provide teaching on suction.
    """)

else:
    st.error("### 🚨 Intervention: URGENT ADMISSION / HDU")
    st.markdown("""
    * **Respiratory:** Start CPAP or High Flow Nasal Cannula (HFNC).
    * **Fluids:** IV fluids (consider 1/2 or 2/3 maintenance) or NGT feeding.
    * **Consultation:** Immediate Senior Clinician / Pediatric ICU review.
    * **Observation:** Constant monitoring for apnoea and exhaustion.
    """)



if st.button("New Assessment"):
    st.rerun()
