import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Econ Club 2027 Hub", page_icon="📈", layout="wide")

# --- ANIMATED BACKGROUND & TITLE CSS INJECTION ---
# Replace with a direct link to your custom background image if needed.
BG_IMAGE_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe" 

animated_bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{BG_IMAGE_URL}"), url("{BG_IMAGE_URL}");
    background-repeat: repeat-y;
    background-size: 100% 200%; /* Stretches them to be tall */
    
    /* Mixes positions so one starts exactly above the other */
    background-position: center 0px, center -100%; 
    
    /* Calls the animation loop below */
    animation: scrollBackground 20s linear infinite;
}}

/* Ensure the main container content stays readable over an animation */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(14, 17, 23, 0.4); /* Reduced slightly to let your background shine through! */
    z-index: -1;
}}

@keyframes scrollBackground {{
    0% {{
        background-position: center 0%, center -100%;
    }}
    100% {{
        background-position: center 100%, center 0%;
    }}
}}

/* --- MAKING THE TITLE POP --- */
h1 {{
    font-family: 'Inter', 'Helvetica Neue', sans-serif;
    font-weight: 800 !important; /* Extra bold */
    letter-spacing: -0.5px;
    
    /* Create a vibrant text gradient matching your background */
    background: linear-gradient(45deg, #ffffff, #e0f2fe, #bae6fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    
    /* Add drop shadow so it stands out against bright background spots */
    filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.5));
    
    padding-bottom: 5px;
}}

/* Make the caption underneath slightly brighter and sharper */
[data-testid="stCaptionContainer"] {{
    color: #f1f5f9 !important;
    font-weight: 500;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
}}
</style>
"""

# Inject the combined CSS into the app layout securely
st.markdown(animated_bg_css, unsafe_allow_html=True)

# --- APP HEADER ---
st.title("📈 Econ Club 2027 // Workspace")
st.caption("Transforming chat chaos into economic insights.")

# Initialize session state for data persistence if they don't exist
if "ideas" not in st.session_state:
    st.session_state.ideas = [
        {"Topic": "Gas price surge mechanics", "Category": "Macroeconomics", "Votes": 3},
        {"Topic": "Gatorade shrinkflation (14oz to 12oz)", "Category": "Consumer Behavior", "Votes": 5}
    ]

# 2. Layout Distribution
col1, col2 = st.columns([1.2, 1.0])

# ==========================================
# LEFT COLUMN: BRAINSTORMING & TOPICS
# ==========================================
with col1:
    st.subheader("💡 Submit a Real-World Econ Topic")
    
    with st.form("topic_form", clear_on_submit=True):
        new_topic = st.text_area("What real-world event should we analyze?", 
                                 placeholder="e.g., Why did Gatorade change their bottle size without dropping the price?")
        category = st.selectbox("Economic Category", ["Macroeconomics", "Microeconomics/Pricing", "Global Trade", "Fiscal Policy"])
        submit_button = st.form_submit_button("Queue Topic")
        
        if submit_button and new_topic:
            st.session_state.ideas.append({"Topic": new_topic, "Category": category, "Votes": 1})
            st.success("Topic added to the discussion queue!")

    st.write("---")
    st.subheader("📊 Current Topic Queue")
    # Convert session state to DataFrame for clean display
    df_ideas = pd.DataFrame(st.session_state.ideas)
    st.dataframe()
