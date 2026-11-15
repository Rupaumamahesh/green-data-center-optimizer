import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Green AI Cloud Scheduler", page_icon="🌿", layout="wide")

# Session state for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}
if "username" not in st.session_state:
    st.session_state.username = ""

# --- LOGIN / SIGNUP PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌿 Green AI Cloud Scheduler</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Carbon-Aware Workload Optimization & Sustainability Portal</p>", unsafe_allow_html=True)
    st.write("---")

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

        with tab1:
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True, type="primary"):
                if login_user in st.session_state.users and st.session_state.users[login_user] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.rerun()
                else:
                    st.error("Invalid username or password. (Hint: use admin / admin123)")

        with tab2:
            new_user = st.text_input("Choose Username", key="new_user")
            new_pass = st.text_input("Choose Password", type="password", key="new_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
            if st.button("Create Account", use_container_width=True):
                if not new_user or not new_pass:
                    st.warning("Please fill in all fields.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif new_user in st.session_state.users:
                    st.error("Username already exists.")
                else:
                    st.session_state.users[new_user] = new_pass
                    st.success("Account created! Switch to the Login tab to sign in.")

# --- MAIN DASHBOARD ---
else:
    # Load Data Safely
    if not os.path.exists("decisions.csv") or not os.path.exists("results_summary.csv"):
        st.error("⚠️ Missing `decisions.csv` or `results_summary.csv` in `C:\\Users\\dkpha\\green_optimizer`.")
        st.stop()

    d = pd.read_csv("decisions.csv")
    summary = pd.read_csv("results_summary.csv")

    # Left Sidebar Navigation
    with st.sidebar:
        st.success(f"👤 Logged in as **{st.session_state.username}**")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        st.write("---")

        st.header("📂 Data Navigation")
        view_option = st.radio(
            "Select Data Section:",
            [
                "📊 Optimization Impact Summary",
                "📈 Emissions & Cost Chart",
                "⏱️ Step-by-Step Routing Decisions",
                "📋 Full Decision Log",
                "🗂️ Side-by-Side Columns (All)"
            ]
        )

    st.title("🌿 Carbon-Aware Cloud Workload Dashboard")
    st.markdown("Real-time optimization tracking for AI compute jobs across global data centers.")
    st.write("---")

    # --- SEPARATE VIEWS BASED ON SIDEBAR SELECTION ---
    if view_option == "📊 Optimization Impact Summary":
        st.subheader("📊 Optimization Impact Summary")
        if "scenario" in summary.columns:
            scenarios = summary["scenario"].unique()
            cols = st.columns(len(scenarios))
            for idx, sc in enumerate(scenarios):
                with cols[idx]:
                    st.markdown(f"### Scenario {sc}")
                    st.dataframe(summary[summary["scenario"] == sc].drop(columns=["scenario"]), use_container_width=True)
        else:
            st.dataframe(summary, use_container_width=True)

    elif view_option == "📈 Emissions & Cost Chart":
        st.subheader("📈 Emissions & Cost Comparison")
        if os.path.exists("comparison_chart.png"):
            st.image("comparison_chart.png", use_container_width=True)
        else:
            st.warning("`comparison_chart.png` not found in the project folder.")

    elif view_option == "⏱️ Step-by-Step Routing Decisions":
        st.subheader("⏱️ Step-by-Step Routing Decisions")
        step_col = "Step" if "Step" in d.columns else ("step" if "step" in d.columns else d.columns[0])
        min_step, max_step = int(d[step_col].min()), int(d[step_col].max())

        if min_step < max_step:
            step = st.slider("Select Time Step", min_step, max_step, min_step)
            filtered_df = d[d[step_col] == step]
        else:
            st.info(f"Showing data for Step {min_step}")
            filtered_df = d

        st.dataframe(filtered_df, use_container_width=True)

    elif view_option == "📋 Full Decision Log":
        st.subheader("📋 Full Decision Log")
        st.dataframe(d, use_container_width=True)

    elif view_option == "🗂️ Side-by-Side Columns (All)":
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Optimization Impact Summary")
            st.dataframe(summary, use_container_width=True)
            if os.path.exists("comparison_chart.png"):
                st.subheader("📈 Comparison Chart")
                st.image("comparison_chart.png", use_container_width=True)

        with col2:
            st.subheader("⏱️ Routing Decisions")
            st.dataframe(d, use_container_width=True)