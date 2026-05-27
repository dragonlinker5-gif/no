import streamlit as st
import random

st.set_page_config(page_title="DebunkOS", page_icon="🧠", layout="wide")

st.title("🧠 DebunkOS // Logical Fallacy & Fact Analyzer")
st.caption("System Framework v1.0.0 — Deconstruct bad arguments instantly.")

# Layout Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Input Argument Data")
    claim_text = st.text_area(
        "Paste the headline, tweet, or quote you want to dissect:", 
        placeholder="Example: 'Everyone says this new law will ruin the economy, so it must be stopped!'"
    )
    
    bias_level = st.slider("Suspected Sensationalism Level", 0, 100, 50)
    analyze_button = st.button("⚡ Run Dissection Protocol", type="primary")

with col2:
    st.subheader("📊 Analytical Output")
    
    if analyze_button and claim_text:
        # Fun calculation logic using the input data
        length_factor = len(claim_text) % 30
        truth_score = max(5, min(95, 100 - bias_level - length_factor + random.randint(-10, 10)))
        
        # Display the major metric
        st.metric(label="Calculated Truth Probability", value=f"{truth_score}%")
        
        if truth_score < 40:
            st.error("🚨 HIGH LOGICAL INFIDELITY DETECTED")
        elif truth_score < 70:
            st.warning("⚠️ PROBABLE SENSATIONALISM OR BIAS PRESENT")
        else:
            st.success("✅ ARGUMENT PASSES BASELINE LOGICAL CONSISTENCY")
            
        # Fallacy Breakdown System
        st.write("### 🔍 Detected Fallacies & Logical Vulnerabilities")
        
        fallacies = []
        if "Everyone" in claim_text or "always" in claim_text.lower() or "never" in claim_text.lower():
            fallacies.append(("Bandwagon / Hasty Generalization", "Appealing to common belief or making an absolute claim without sufficient statistical samples."))
        if "ruin" in claim_text.lower() or "destroy" in claim_text.lower() or "kill" in claim_text.lower():
            fallacies.append(("Appeal to Emotion (Fear)", "Using highly charged language to manipulate emotional responses instead of presenting valid evidence."))
            
        if not fallacies:
            fallacies.append(("None explicitly triggered via string matches", "Try using words like 'Everyone', 'always', 'never', or 'ruin' to trigger the pattern matching matrix."))

        for name, desc in fallacies:
            with st.expander(f"❌ {name}"):
                st.write(desc)
    else:
        st.info("Awaiting execution protocol. Input data into Column 1 and click 'Run Dissection Protocol'.")
