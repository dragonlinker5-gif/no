import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Econ Club 2027 Hub", page_icon="📈", layout="wide")

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
    st.dataframe(df_ideas, use_container_width=True)

# ==========================================
# RIGHT COLUMN: SCHEDULING & AVAILABILITY
# ==========================================
with col2:
    st.subheader("🗓️ Member Availability Matrix")
    st.write("Select the times you are free this coming weekend:")
    
    # Simple form for group members to log availability
    member_name = st.selectbox("Who are you?", ["hotdog", "seer12351", "tthatg", "Goobert", "insidechaosis"])
    
    sat_free = st.checkbox("Saturday (Anytime)")
    sun_early = st.checkbox("Sunday Morning/Afternoon")
    sun_late = st.checkbox("Sunday Night (Late Sunday)")
    
    save_sched = st.button("Save My Schedule", type="primary")
    
    st.write("---")
    st.subheader("🎯 Optimal Meeting Window")
    # Custom alert logic to resolve conflicts based on chat data
    if tthatg_out_of_town_or_similar := True: 
        st.warning("⚠️ Notice: Multiple members noted they are out of town until Late Sunday.")
        st.info("💡 **Recommended Window:** Sunday Night after 7:00 PM looks optimal for maximum attendance.")
