import streamlit as st

st.set_page_config(page_title="Bronchiolitis Guideline", layout="centered")

st.title("📑 Bronchiolitis Clinical Pathway")
st.write("Follow the steps to determine the management plan.")

# --- المرحلة الأولى: التقييم السريري ---
st.header("1. Clinical Assessment")

col1, col2 = st.columns(2)

with col1:
    feeding = st.radio("Feeding Status:", ["Normal", "50-75% of normal", "< 50% of normal"])
    effort = st.radio("Respiratory Effort:", ["Normal", "Mild recession", "Moderate/Severe recession"])

with col2:
    oxygen = st.slider("Oxygen Saturation (SpO2 %):", 80, 100, 95)
    apnoea = st.checkbox("History of Apnoea?")

# --- المرحلة الثانية: منطق التصنيف بناءً على الملف ---
# بناءً على معايير ملف bronchioritis.xlsx
severity = "Mild"  # افتراضي

if apnoea or oxygen < 90 or feeding == "< 50% of normal" or effort == "Moderate/Severe recession":
    severity = "Severe"
elif oxygen < 92 or feeding == "50-75% of normal" or effort == "Mild recession":
    severity = "Moderate"
else:
    severity = "Mild"

# --- المرحلة الثالثة: عرض النتيجة والخوارزمية ---
st.divider()
st.subheader(f"Classification: {severity}")

if severity == "Mild":
    st.success("✅ Management: Home Care (Discharge)")
    st.info("Instructions: Saline drops, small frequent feeds, safety net advice.")

elif severity == "Moderate":
    st.warning("⚠️ Management: Hospital Observation")
    st.write("- Consider NGT feeding if oral intake is poor.")
    st.write("- Oxygen therapy if SpO2 stays below 92%.")

else:
    st.error("🚨 Management: Urgent Admission / HDU")
    st.write("- Intravenous fluids or NGT.")
    st.write("- High-flow oxygen or CPAP may be required.")
    st.write("- Senior Review mandatory.")

# زر إعادة البدء
if st.button("New Assessment"):
    st.rerun()
