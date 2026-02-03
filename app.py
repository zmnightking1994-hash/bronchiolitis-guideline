import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="Bronchiolitis Clinical Guide 2025",
    page_icon="👶",
    layout="wide"
)

st.title("📑 Bronchiolitis Management Pathway (Final Gold Version)")
st.caption("Integrated Protocol: RCH Melbourne & PREDICT 2025 Guidelines")

# --- SECTION 1: RISK ASSESSMENT ---
st.header("1. Risk & Threshold Assessment")
col_age, col_risks = st.columns([1, 2])

with col_age:
    age_weeks = st.number_input("Infant Age (Weeks):", min_value=1, max_value=100, value=12)
    is_under_6_weeks = age_weeks < 6 

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Chronic Lung Disease", "Congenital Heart Disease", "Gestational age <37 weeks", 
         "Neurological conditions", "Immunodeficiency", "Tobacco smoke exposure"]
    )

# العتبة (Target SpO2): 92% للحالات تحت 6 أسابيع أو ذوي الخطورة، و90% للبقية
has_risks = (is_under_6_weeks or len(risk_factors) > 0)
current_threshold = 92 if has_risks else 90

st.divider()

# --- SECTION 2: CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB):", ["Normal", "Mild", "Moderate", "Severe / Grunting"])
    behavior = st.radio("Behavior:", ["Normal", "Irritable", "Lethargic / AMS"])
with c2:
    feeding = st.radio("Feeding Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"])
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported by parents", "Observed clinically"])
with c3:
    rr = st.number_input("Respiratory Rate (bpm):", 10, 150, 40)
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96)
    st.info(f"💡 Clinical Target: SpO2 ≥ {current_threshold}%")

# --- Severity Logic ---
severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or behavior == "Lethargic / AMS" or 
    apnoea == "Observed clinically" or feeding == "< 50% / Dehydration" or rr > 70):
    severity = "Severe"
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or 
      feeding == "50-75% Intake" or apnoea == "Reported by parents" or behavior == "Irritable"):
    severity = "Moderate"

# --- SECTION 3: MANAGEMENT PILLARS ---
st.divider()
st.header(f"Management Plan: {severity}")
st.error("🚫 **AVOID:** Salbutamol, Steroids, Antibiotics, X-rays, or Deep Suction.")

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    
    if apnoea == "Observed clinically":
        st.error("**🚨 URGENT: Observed Apnoea Protocol**")
        st.markdown(f"""
        - **Immediate Action:** Continuous Cardiorespiratory Monitoring.
        - **First Line:** Start **HFNC (High Flow)** even if SpO2 is normal to provide PEEP.
        - **Titration:** Flow **2 L/kg/min** | FiO2 to keep SpO2 ≥ {current_threshold}%.
        - **Escalation:** Move to CPAP (**5-7 cmH2O**) if apnoea persists.
        """)
    elif severity == "Mild":
        st.success("**Plan: Standard Care**")
        st.write(f"- SpO2 {spo2}% is adequate. No supplemental O2 needed.")
        st.write("- Intermittent monitoring (every 4h).")
    elif severity == "Moderate":
        st.warning("**Plan: Low Flow Oxygen (LFNP)**")
        st.markdown(f"""
        - **Device:** Nasal prongs at **0.5 - 2 L/min**.
        - **Criteria:** Only if SpO2 persistently < {current_threshold}%.
        - **Note:** If failing LFNP after 2 hours, escalate to HFNC.
        """)
    else: # Severe
        st.error("**Plan: High Flow (HFNC) Escalation**")
        st.markdown(f"""
        - **HFNC Setup:** **2 L/kg/min** (Max 25L) | FiO2 starting at **40%**.
        - **Monitoring:** Continuous HR, RR, and SpO2.
        - **Failure Criteria:** FiO2 > 50% or worsening effort -> Switch to **CPAP**.
        """)

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration & Nutrition")
    
    if apnoea == "Observed clinically":
        st.error("**🚨 URGENT: NBM Status**")
        st.markdown("""
        - **Feeding:** **NBM (Nil By Mouth)** temporarily due to aspiration risk.
        - **Action:** Start **NGT (Nasogastric Tube)** hydration.
        - **Fluid Rate:** **66% of maintenance** (Restricted).
        """)
    elif feeding == "< 50% / Dehydration":
        st.error("**Plan: Active Hydration**")
        st.markdown("- **Route:** NGT preferred over IV.\n- **Rate:** 66-75% of maintenance.")
    elif feeding == "50-75% Intake":
        st.warning("**Plan: NGT Support**")
        st.write("- Provide 100% maintenance via NGT boluses.")
    else:
        st.success("**Plan: Oral Feeding**")
        st.write("- Encourage small, frequent breast/formula feeds.")

# --- SECTION 4: WEANING & DISCHARGE ---
st.divider()
st.subheader("📉 Detailed Weaning & Discharge Protocol")
cw1, cw2 = st.columns(2)

with cw1:
    st.info("**How to Wean Oxygen?**")
    st.markdown(f"""
    1. **HFNC:** Reduce FiO2 to 21% (Room Air). If stable for 2h, stop HFNC.
    2. **Low Flow:** Trial off O2 if SpO2 > {current_threshold}% consistently for 2h.
    3. **Trial Timing:** Attempt to wean every 6 hours (especially during awake periods).
    """)

with cw2:
    st.info("**Discharge Readiness Checklist:**")
    st.markdown(f"""
    - [ ] SpO2 ≥ {current_threshold}% on air for **4-12 hours** (including sleep).
    - [ ] Feeding > 50-75% of normal volumes orally.
    - [ ] No observed apnoea for at least 24 hours.
    - [ ] Family educated on 'Safety Netting' and when to return.
    """)



if st.button("Clear & New Patient Assessment"):
    st.rerun()
