import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="The Econ Club 2027 Hub", page_icon="🤑🤑🤑", layout="wide")

# --- ANIMATED BACKGROUND & TITLE CSS INJECTION ---
# Using the Unsplash abstract gradient backdrop URL
BG_IMAGE_URL = "https://unsplash.com/photos/a-textured-green-background-with-horizontal-lines-WPS6N8uHWeU" 

animated_bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{BG_IMAGE_URL}"), url("{BG_IMAGE_URL}");
    background-repeat: repeat-y;
    background-size: 100% 200%;
    background-position: center 0px, center -100%; 
    animation: scrollBackground 20s linear infinite;
}}

/* Dark overlay mask to keep text sharp and readable */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(14, 17, 23, 0.4); 
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
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    background: linear-gradient(45deg, #ffffff, #e0f2fe, #bae6fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.5));
    padding-bottom: 5px;
}}

/* Subtitle styling */
[data-testid="stCaptionContainer"] {{
    color: #f1f5f9 !important;
    font-weight: 500;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
}}
</style>
"""

# Inject the combined CSS styles securely
st.markdown(animated_bg_css, unsafe_allow_html=True)

# --- APP HEADER ---
st.title("Econ Club 2027 // Workspace")
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
    st.subheader("Submit real world econ Topic")
    
    with st.form("topic_form", clear_on_submit=True):
        new_topic = st.text_area("What real-world event should we analyze?", 
                                 placeholder="e.g., Why did Gatorade change their bottle size without dropping the price?")
        category = st.selectbox("Economic Category", ["Macroeconomics", "Microeconomics/Pricing", "Global Trade", "Fiscal Policy"])
        submit_button = st.form_submit_button("Queue Topic")
        
        if submit_button and new_topic:
            st.session_state.ideas.append({"Topic": new_topic, "Category": category, "Votes": 1})
            st.success("Topic added to the discussion queue!")

    st.write("---")
    st.subheader("Topic waiting line")
    df_ideas = pd.DataFrame(st.session_state.ideas)
    st.dataframe(df_ideas, use_container_width=True)

# ==========================================
# RIGHT COLUMN: SCHEDULING & AVAILABILITY
# ==========================================
with col2:
    st.subheader("When are u free?")
    st.write("Select the times you are free this coming weekend:")
    
    member_name = st.selectbox("Who are you?", ["hotdog", "seer12351", "tthatg", "Goobert", "insidechaosis"])
    
    sat_free = st.checkbox("Saturday (Anytime)")
    sun_early = st.checkbox("Sunday Morning/Afternoon")
    sun_late = st.checkbox("Sunday Night (Late Sunday)")
    
    save_sched = st.button("Save My Schedule", type="primary")
    
    st.write("---")
    st.subheader("Best time/day to meet")
    
    if tthatg_out_of_town_or_similar := True: 
        st.warning("⚠️ Notice: Multiple members noted they are out of town until Late Sunday.")
        st.info("💡 **Recommended Window:** Sunday Night after 7:00 PM looks optimal for maximum attendance.")
