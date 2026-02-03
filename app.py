import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Bronchiolitis Gold Guide 2026", layout="wide")

st.title("📑 Bronchiolitis Management Pathway (Final Clinical Version)")
st.caption("Integrated Protocol: Global Evidence-Based Standards with Practical Safety Checks")

# --- 1. RISK ASSESSMENT ---
st.header("1. Risk Assessment")
col_age, col_risks = st.columns([1, 2])
with col_age:
    is_under_6_weeks = st.checkbox("Infant age < 6 weeks (Apnoea High Risk)") [cite: 32]

with col_risks:
    risk_factors = st.multiselect(
        "Risk Factors for Severe Illness:",
        ["Preterm birth (< 37 weeks)", "Chronic Lung Disease (CLD)", "Congenital Heart Disease (CHD)", 
         "Neurological/Neuromuscular conditions", "Immunodeficiency", "Tobacco smoke exposure"] [cite: 33, 35, 36, 37, 38]
    )

# ضبط عتبة الأكسجين: 92% للحالات عالية الخطورة [cite: 32]، و90% للحالات المستقرة عالمياً.
current_threshold = 92 if (is_under_6_weeks or risk_factors) else 90

st.divider()

# --- 2. CLINICAL ASSESSMENT ---
st.header("2. Clinical Assessment")
c1, c2, c3 = st.columns(3)

with c1:
    effort = st.radio("Work of Breathing (WOB):", ["Normal", "Mild", "Moderate", "Severe / Grunting"]) [cite: 4, 28]
    behavior = st.radio("Behavioral State:", ["Normal / Alert", "Irritable", "Lethargic / Altered Mental State"]) [cite: 3, 25]
with c2:
    feeding_status = st.radio("Current Intake:", ["Adequate", "50-75% Intake", "< 50% / Dehydration"]) [cite: 7, 21]
    apnoea = st.selectbox("Apnoea Events:", ["None", "Reported by parents", "Observed clinically"]) [cite: 26]
with c3:
    rr = st.number_input("Respiratory Rate (bpm):", 10, 150, 40) [cite: 9, 17, 25]
    spo2 = st.slider("Oxygen Saturation (SpO2 %):", 70, 100, 96) [cite: 6, 11, 29]
    st.info(f"💡 Target SpO2: ≥ {current_threshold}%")

# --- 3. SAFETY & SEVERITY LOGIC ---
# تصنيف الشدة التنفسية
resp_severity = "Mild"
if (effort == "Severe / Grunting" or spo2 < 87 or apnoea == "Observed clinically" or 
    behavior == "Lethargic / Altered Mental State" or rr > 70):
    resp_severity = "Severe" [cite: 24, 25, 28, 29]
elif (effort == "Moderate" or (87 <= spo2 < current_threshold) or (50 <= rr <= 70) or apnoea == "Reported by parents"):
    resp_severity = "Moderate" [cite: 16, 19, 20]

# حماية المجرى التنفسي: منع التغذية الفموية في الحالات الحرجة [cite: 78, 82]
is_unsafe_to_feed = (behavior == "Lethargic / Altered Mental State" or apnoea == "Observed clinically" or effort == "Severe / Grunting")

# --- 4. DETAILED MANAGEMENT PILLARS ---
st.divider()
st.header(f"Management Plan | Resp: {resp_severity} | Feeding Status: {'⚠️ NBM REQUIRED' if is_unsafe_to_feed else 'Stable'}")
st.error("🚫 **DO NOT ROUTINELY USE:** Salbutamol, Adrenaline, Steroids, Antibiotics, or Chest X-rays.") [cite: 51, 71]

col_resp, col_hydra = st.columns(2)

with col_resp:
    st.subheader("🫁 Pillar 1: Respiratory Support")
    if resp_severity == "Severe":
        st.error("**🚨 High Flow (HFNC) & Escalation Protocol:**")
        st.markdown(f"""
        - **HFNC Flow:** Start at **2 L/kg/min** (Min 8L, Max 25L). [cite: 86, 88]
        - **FiO2:** Start at **40%**; titrate to keep SpO2 ≥ {current_threshold}%. [cite: 89, 122]
        - **Monitoring:** Continuous HR, RR, and SpO2. [cite: 64, 125]
        - **Gastric Safety:** Insert a **venting NGT** to avoid gastric distension. 
        - **Escalation (CPAP):** Consider if FiO2 > 50% or persistent apnoea. [cite: 104, 106, 131]
        - **CPAP Settings:** Pressure **5-7 cmH2O** | Flow **7-10 L/min**. 
        """)
    elif resp_severity == "Moderate":
        st.warning("**⚠️ Low Flow Oxygen (LFNP):**")
        st.write(f"- Use nasal prongs at 0.5 - 2 L/min to maintain SpO2 ≥ {current_threshold}%.") [cite: 60]
    else:
        st.success("**✅ Action: Clinical Monitoring**")

with col_hydra:
    st.subheader("🍼 Pillar 2: Hydration (Safety Standards)")
    if is_unsafe_to_feed:
        st.error("**🚨 Action: NBM (Nil By Mouth)**")
        st.write("- **Method:** NGT (preferred) or IV hydration.") [cite: 78, 83]
        st.write("- **Rate:** **66-75% of maintenance** (prevents SIADH/fluid overload).") [cite: 60, 78]
    elif feeding_status == "< 50% / Dehydration":
        st.error("**Action: Active Hydration**")
        st.write("- NGT at 66-75% maintenance rate.") [cite: 83]
    else:
        st.success("**Action: Oral Feeding**")
        st.write("- Continue breastfeeding or formula as tolerated.") [cite: 49, 13]

# --- 5. DETAILED WEANING & DISCHARGE ---
st.divider()
st.subheader("🏥 Weaning & Discharge Protocol")

if spo2 >= 95 and effort == "Normal" and behavior == "Normal / Alert" and feeding_status == "Adequate":
    st.balloons()
    st.success("**🚀 Fast Track Discharge Enabled:** SpO2 ≥ 95% on air and stable. Safe for home.")
else:
    c_wean, c_dis = st.columns(2)
    with c_wean:
        st.info("**📉 Weaning (Every 4-6 hours):**") [cite: 121]
        st.markdown(f"""
        1. Reduce FiO2 to **21% (Room Air)** first. [cite: 122]
        2. If stable for 2h on 21% FiO2, stop HFNC flow. [cite: 126]
        3. **Failure Signs:** If HR increases by >20 or RR by >10, restart support. 
        """)
    with c_dis:
        st.info("**🏠 Standard Discharge Criteria:**") [cite: 102]
        st.markdown(f"""
        - **Oxygen:** SpO2 ≥ {current_threshold}% on air for 4-12h (including sleep). [cite: 66, 91]
        - **Feeding:** Oral intake > 50-75% of normal volumes. [cite: 12, 112]
        - **Effort:** No grunting or severe recessions. [cite: 111]
        - **Safety:** Parents educated on red flags. [cite: 53, 55]
        """)



if st.button("New Assessment"):
    st.rerun()
