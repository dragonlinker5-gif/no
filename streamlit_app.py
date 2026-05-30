import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="The Econ Club 2027 Hub", page_icon="🤑", layout="wide")

# --- ANIMATED BACKGROUND & TITLE CSS INJECTION ---
BG_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnwZjOUvmLdeSQGGLKyUHBHwDQvP4relaiQA&s" 

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
    0% {{ background-position: center 0%, center -100%; }}
    100% {{ background-position: center 100%, center 0%; }}
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
st.caption("Transforming chat chaos into economic insights or wtv")

# --- PERSISTENT DATA WAREHOUSE (Session State) ---
if "ideas" not in st.session_state:
    st.session_state.ideas = [
        {"Topic": "Gas price surge mechanics", "Category": "Macroeconomics", "Votes": 3},
        {"Topic": "Gatorade shrinkflation (14oz to 12oz)", "Category": "Consumer Behavior", "Votes": 5}
    ]

if "schedules" not in st.session_state:
    # Set default dummy schedule data based on your Discord text logs!
    st.session_state.schedules = {
        "hotdog": {"Sat": False, "Sun_Early": False, "Sun_Late": False},
        "seer12351": {"Sat": True, "Sun_Early": True, "Sun_Late": True},
        "tthatg": {"Sat": False, "Sun_Early": False, "Sun_Late": True}, # Out of town until late Sunday
        "Goobert": {"Sat": True, "Sun_Early": True, "Sun_Late": True},
        "insidechaosis": {"Sat": True, "Sun_Early": True, "Sun_Late": True}
    }

# 2. Layout Distribution
col1, col2 = st.columns([1.2, 1.0])

# ==========================================
# LEFT COLUMN: BRAINSTORMING & TOPICS
# ==========================================
with col1:
    st.subheader("Submit real world econ Topic")
    
    with st.form("topic_form", clear_on_submit=True):
        new_topic = st.text_area("What real world event do we look at??", 
                                 placeholder="e.g., Why did Gatorade change their bottle size without dropping the price?")
        category = st.selectbox("Economic Category", ["Macroeconomics", "Microeconomics/Pricing", "Global Trade", "Fiscal Policy"])
        submit_button = st.form_submit_button("Queue Topic")
        
        if submit_button and new_topic:
            st.session_state.ideas.append({"Topic": new_topic, "Category": category, "Votes": 1})
            st.rerun()

    st.write("---")
    st.subheader("Topic waiting line")
    if st.session_state.ideas:
        df_ideas = pd.DataFrame(st.session_state.ideas)
        st.dataframe(df_ideas, use_container_width=True)
    else:
        st.info("The waiting line is clear! Type an economic anomaly above to populate.")

# ==========================================
# RIGHT COLUMN: SCHEDULING & AVAILABILITY
# ==========================================
with col2:
    st.subheader("When are u free?")
    st.write("Select the times you are free this coming weekend NOW:")
    
    member_name = st.selectbox("Who ares yous?", ["hotdog", "seer12351", "tthatg", "Goobert", "insidechaosis"])
    
    # Pre-populate checkboxes if the member has already submitted data
    current_mem = st.session_state.schedules.get(member_name, {"Sat": False, "Sun_Early": False, "Sun_Late": False})
    
    sat_free = st.checkbox("Saturday (Anytime)", value=current_mem["Sat"])
    sun_early = st.checkbox("Sunday Morning/Afternoon", value=current_mem["Sun_Early"])
    sun_late = st.checkbox("Sunday Night (Late Sunday)", value=current_mem["Sun_Late"])
    
    if st.button("Save My Schedule", type="primary"):
        st.session_state.schedules[member_name] = {
            "Sat": sat_free,
            "Sun_Early": sun_early,
            "Sun_Late": sun_late
        }
        st.success(f"Schedule recorded for {member_name}!")
        st.rerun()
    
    st.write("---")
    st.subheader("Best time/day to meet")
    
    # --- AUTOMATIC CALCULATION ENGINE ---
    # Total up how free everyone is across slots
    total_members = len(st.session_state.schedules)
    sat_count = sum(1 for m in st.session_state.schedules.values() if m["Sat"])
    sun_e_count = sum(1 for m in st.session_state.schedules.values() if m["Sun_Early"])
    sun_l_count = sum(1 for m in st.session_state.schedules.values() if m["Sun_Late"])
    
    # Check if there is an active crunch/conflict
    out_of_town_mems = [name for name, sched in st.session_state.schedules.items() if not sched["Sat"] and not sched["Sun_Early"]]
    
    if out_of_town_mems:
        st.warning(f"**NOTICE:** {', '.join(out_of_town_mems)} flagged conflict/out-of-town metrics for early weekend windows.")
    
    # Pick the mathematically best slot
    slots = {"Saturday": sat_count, "Sunday Morning/Afternoon": sun_e_count, "Sunday Night": sun_l_count}
    best_slot = max(slots, key=slots.get)
    max_count = slots[best_slot]
    
    if max_count == 0:
        st.info("Awaiting availability inputs. Check blocks above to calculate consensus.")
    else:
        st.success(f"**Recommended Window:** **{best_slot}** ({max_count}/{total_members} members verified free!)")

# ==========================================
# FOOTER: SECRET ADMIN DASHBOARD
# ==========================================
st.write("---")
with st.expander("🔒 Developer Access Portal"):
    password = st.text_input("Enter Admin Override Credential Token:", type="password")
    
    if password == "2.718281828459045":
        st.success("Authorized Operator Access Granted.")
        st.write("### 🛠️ Workspace Clean up Utilities")
        
        if st.session_state.ideas:
            topic_options = [item["Topic"] for item in st.session_state.ideas]
            target_deletion = st.selectbox("Select target topic to erase from database:", topic_options)
            
            if st.button("Execute Targeted Wipeout", type="secondary"):
                st.session_state.ideas = [i for i in st.session_state.ideas if i["Topic"] != target_deletion]
                st.toast(f"Wiped topic: {target_deletion}")
                st.rerun()
        else:
            st.info("No active topics to wipe out.")
    elif password != "":
        st.error("Invalid Credential Token. Access Denied.")
