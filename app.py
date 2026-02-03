import streamlit as st

# Page setup
st.set_page_config(page_title="Bronchiolitis Guideline 2025", layout="wide")

st.title("📑 Australasian Bronchiolitis Management Pathway (2025 Update)")

# --- SECTION 1: RISK FACTORS (As per Guideline p. 9) ---
st.subheader("1. Risk Factors for Severe Illness")
with st.expander("Identify factors that increase risk of deterioration", expanded=True):
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        age_risk = st.checkbox("Young chronological age (especially < 6 weeks)")
        preterm = st.checkbox("Gestational age < 37 weeks")
        tobacco = st.checkbox("Exposure to tobacco smoke (Prenatal/Postnatal)")
    with col_r2:
        comorbidities = st.checkbox("Comorbidities (CHD, CLD, Trisomy 21, etc.)")
        breastfeeding = st.checkbox("Reduced breastfeeding exposure")
        growth = st.checkbox("Faltering growth / Slow weight gain")

if any([age_risk, preterm, tobacco, comorbidities, breastfeeding, growth]):
    st.warning("⚠️ High Risk: These factors are cumulative. Consider a longer observation period or admission even if symptoms are currently mild.")

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT (As per Guideline p. 11-14) ---
st.subheader("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio(
        "Respiratory Effort:",
        ["Normal", "Mild Recession", "Moderate Recession", "Severe Recession / Grunting"],
        help="Check for tachypnoea and retractions."
    )
    behavior = st.radio(
        "Behavioral State:",
        ["Normal / Alert", "Irritable / Difficult to soothe", "Lethargic / Altered Mental State"]
    )

with c2:
    feeding = st.radio(
        "Hydration / Nutrition Status:",
        ["Adequate Intake", "50-75% of normal intake", "< 50% of normal intake / Dehydration"]
    )
    apnoea = st.selectbox("Apnoea:", ["None", "Reported", "Observed"])

with c3:
    rr = st.number_input("Respiratory Rate (breaths/min):", min_value=10, max_value=150, value=40)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 80, 100, 96)
    age_under_6w = age_risk # Linked to the risk factor checkbox

# --- SECTION 3: SEVERITY LOGIC (Pragmatic Definition p. 18) ---
severity = "Mild"

# Severe Criteria
if (effort == "Severe Recession / Grunting" or 
    spo2 < 90 or 
    behavior == "Lethargic / Altered Mental State" or 
    feeding == "< 50% of normal intake / Dehydration" or 
    apnoea == "Observed" or
    rr > 70):
    severity = "Severe"

# Moderate Criteria
elif (effort == "Moderate Recession" or 
      (90 <= spo2 < 92) or 
      (50 <= rr <= 70) or
      behavior == "Irritable / Difficult to soothe" or 
      feeding == "50-75% of normal intake" or
      apnoea == "Reported"):
    severity = "Moderate"

# --- SECTION 4: INTEGRATED INTERVENTIONS (Based on p. 12-14) ---
st.divider()
st.header(f"Clinical Status: {severity}")

# Global Recommendations (The "Don'ts")
st.error("🚫 **GUIDELINE RESTRICTIONS:** Do not routinely use Chest X-rays, Blood tests, Viral swabs, Salbutamol, Steroids, Antibiotics, or Chest Physiotherapy.")

if severity == "Mild":
    st.success("### ✅ Interventions & Discharge Plan")
    st.markdown(f"""
    * **Oxygen:** Not required (SpO2 is {spo2}%).
    * **Hydration:** Encourage oral fluids. No supplemental hydration needed if > 75% intake.
    * **Suction:** Superficial nasal suction only if nose is blocked or before feeding.
    * **Discharge Criteria:** SpO2 > 92% (or > 90% if > 6 weeks old), feeding > 50-75%, and parents feel confident.
    """)

elif severity == "Moderate":
    st.warning("### ⚠️ Interventions & Observation")
    st.markdown(f"""
    * **Oxygen:** Consider supplemental oxygen if SpO2 persistently < 90% (or < 92% if < 6 weeks old).
    * **Hydration:** Provide NG or IV fluids if oral intake is < 50-75% or dehydration present. NG is preferred.
    * **Monitoring:** Use Early Warning Tools (EWT). Do not use continuous pulse oximetry for stable non-hypoxaemic infants.
    * **High Flow (HF):** Do not use HF as first-line. Consider only if failing low-flow oxygen.
    """)

else:
    st.error("### 🚨 Urgent Interventions (HDU/ICU)")
    st.markdown("""
    * **Respiratory Support:** Consider CPAP for severe respiratory failure. HF therapy may be used prior to CPAP.
    * **Hydration:** NG or IV fluids (consider restriction to 50-75% of maintenance to avoid fluid overload).
    * **Consultation:** Immediate Senior Clinician review. 
    * **SARS-CoV-2 Note:** If co-infected and hypoxaemic, consider Dexamethasone.
    """)

if st.button("New Assessment"):
    st.rerun()
