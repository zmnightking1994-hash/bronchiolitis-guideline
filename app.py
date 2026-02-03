import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Detailed Protocol", layout="wide")

st.title("📑 Detailed Bronchiolitis Management Pathway")
st.caption("Focus: Precise Titration, Monitoring, and Weaning Protocols")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    age_weeks = st.number_input("Infant Age (Weeks):", min_value=1, max_value=100, value=12)
    is_under_6_weeks = age_weeks < 6 # تم التعديل ليكون 6 أسابيع كعامل خطر

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Chronic Lung Disease", "Congenital Heart Disease", "Gestational age <37 weeks", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# العتبة: 92% للحالات تحت 6 أسابيع أو ذوي الخطورة، و90% للبقية
current_threshold = 92 if (is_under_6_weeks or len(risk_factors) > 0) else 90

st.divider()

# --- SECTION 2: CLINICAL STATUS ---
st.header("2. Clinical Status")
c1, c2, c3 = st.columns(3)
with c1:
    effort = st.radio("Work of Breathing:", ["Normal", "Mild", "Moderate", "Severe / Grunting"])
    behavior = st.radio("Behavior:", ["Normal", "Irritable", "Lethargic / AMS"])
with c2:
    feeding = st.radio("Hydration:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"])
    apnoea = st.selectbox("Apnoea:", ["None", "Reported", "Observed clinically"])
with c3:
    rr = st.number_input("RR (bpm):", 10, 150, 40)
    spo2 = st.slider("SpO2 %:", 70, 100, 96)

# Severity Logic
severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or behavior == "Lethargic / AMS" or 
    apnoea == "Observed clinically" or feeding == "< 50% / Dehydration" or rr > 70):
    severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or 
      feeding == "50-75% Intake" or apnoea == "Reported" or behavior == "Irritable"):
    severity = "Moderate"

# --- SECTION 3: DETAILED MANAGEMENT & MONITORING ---
st.divider()
st.header(f"Management & Monitoring Plan: {severity}")

# تقسيم التدبير إلى ركيزتين تفصيليتين
col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Detailed Respiratory Support")
    
    if severity == "Mild":
        st.success("**Standard Care:** No supplemental O2.")
        st.write(f"- Monitoring: Intermittent (every 4 hours). Stop if SpO2 stable > {current_threshold}% for 2h.")
    
    elif severity == "Moderate":
        st.warning("**Low Flow Nasal Prongs (LFNP):**")
        st.markdown(f"""
        * **Flow Rate:** Start at **0.5 - 2 L/min** via nasal prongs.
        * **Goal:** Keep SpO2 ≥ {current_threshold}%.
        * **Monitoring:** Continuous SpO2 until stable for 2h, then move to intermittent.
        * **Trial:** If stable, trial off O2 every 6-12 hours.
        """)
    
    else: # Severe
        st.error("**High Flow (HFNC) & Escalation Protocol:**")
        st.markdown(f"""
        1. **High Flow Nasal Cannula (HFNC):**
           - **Flow Rate:** Start at **2 L/kg/min** (Max 20-25 L/min).
           - **FiO2:** Start at **40%** and titrate to keep SpO2 ≥ {current_threshold}%.
           - **Monitoring:** **Continuous** heart rate, RR, and SpO2.
        
        2. **CPAP (If HFNC Fails):**
           - **Criteria:** Persistent apnoea, FiO2 > 50% on HFNC, or worsening acidosis/effort.
           - **Pressure:** Start at **5 - 7 cmH2O**.
           - **Note:** Transfer to ICU/HDU environment.
        """)

with col_hydra:
    st.subheader("🍼 Detailed Hydration (2025 Standard)")
    if feeding == "Adequate":
        st.success("**Oral Feeding:** Continue breast/formula.")
    else:
        st.error("**Non-oral Fluid Management:**")
        st.markdown(f"""
        * **Route of Choice:** **Nasogastric (NGT)** (Standard bolus feeding).
        * **Rate:** **66% - 75% of maintenance** (Restricted to avoid SIADH/Fluid overload).
        * **Calculation:** (e.g., if 100ml/kg is normal, give **66ml/kg/24h**).
        * **IV Fluids:** Only if NGT is contraindicated. Use Isotonic (0.9% NaCl + 5% Glucose).
        """)

# --- SECTION 4: THE WEANING & DISCHARGE FLOWCHART (بالتفصيل) ---
st.divider()
st.subheader("📉 The Weaning & Stopping Protocol (How to stop O2)")
c_wean1, c_wean2 = st.columns(2)

with c_wean1:
    st.info("**When to Wean O2?**")
    st.markdown(f"""
    - **Step 1:** If SpO2 is consistently > {current_threshold+2}% for 2 hours.
    - **Step 2:** Reduce FiO2 on HFNC to 21% (Room Air) while maintaining flow.
    - **Step 3:** Switch from HFNC to **Room Air** directly if effort is mild.
    - **Step 4:** Trial off LFNP (0.5 L/min) to room air.
    """)

with c_wean2:
    st.info("**Discharge Readiness:**")
    st.markdown(f"""
    - **SpO2:** Consistent ≥ {current_threshold}% on air for **4 - 12 hours** (including during sleep).
    - **Feeding:** Taking > 50-75% of normal volumes orally.
    - **Work of Breathing:** Stable (Mild or Normal) with no grunting or severe recessions.
    """)

if st.button("Clear & New Patient"):
    st.rerun()
