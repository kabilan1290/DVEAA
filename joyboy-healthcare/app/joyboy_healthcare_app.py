import streamlit as st

# --- Static credentials ---
USERS = {
    "admin": {"password": "admin", "role": "staff"},
    "kishore": {"password": "kishore", "role": "patient"}
}

# --- Streamlit config ---
st.set_page_config(page_title="JoyBoy Health Care", layout="wide")

# --- Styles ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f6fa;
    }
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #2c3e50;
    }
    .subtitle {
        font-size: 16px;
        color: #7f8c8d;
        margin-top: 4px;
        margin-bottom: 30px;
    }
    .section-box {
        background-color: #ffffff;
        padding: 30px 25px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #0052cc;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #003d99;
    }
    .login-box {
        width: 400px;
        margin: auto;
        padding-top: 100px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Auth Functions ---
def authenticate(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None

# --- Session state setup ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None

# --- Login Form with Role Toggle ---
# --- Login Form with Role Toggle ---
if not st.session_state.authenticated:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🔐 JoyBoy Health Care Login")

    role_choice = st.radio("Login As", ["Staff", "Patient"], horizontal=True)
    expected_role = "staff" if role_choice == "Staff" else "patient"

    # Dynamic input label
    username_label = "Username" if expected_role == "staff" else "Patient Name"
    username = st.text_input(username_label)
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password and user["role"] == expected_role:
            st.session_state.authenticated = True
            st.session_state.role = expected_role
            st.session_state.username = username
            st.success(f"Welcome, {username.title()}! Logged in as {expected_role.title()}.")
            st.rerun()
        else:
            st.error(f"Invalid credentials for {expected_role.title()}.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()



# --- Sidebar ---
with st.sidebar:
    st.title("JoyBoy Health Care")
    st.markdown(f"Logged in as: **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()

    if st.session_state.role == "staff":
        page = st.radio("Navigation", [
            "Home",
            "Patient Report Generator",
            "Medical Ticket Triage",
            "Internal Policy Assistant",
            "Diagnostic Suggestion Tool"
        ])
    else:  # patient view
        page = st.radio("Navigation", ["Home", "Patient Report Viewer"])

# --- Header ---
st.markdown(f'<div class="main-title">JoyBoy Health Care</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">Welcome, {st.session_state.username.title()} ({st.session_state.role.title()})</div>', unsafe_allow_html=True)

# --- Pages ---
if page == "Home":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Welcome to JoyBoy Health Care")
    st.write("""
        JoyBoy Health Care is a role-based internal AI system to assist medical professionals and patients.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Patient Report Generator":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Patient Report Generator")
    st.write("Input unstructured doctor notes below and get a structured report.")
    notes = st.text_area("Patient Notes", height=180)
    if st.button("Generate Report"):
        st.info("Generating report... (LLM integration to be added)")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Medical Ticket Triage":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Medical Ticket Triage")
    symptoms = st.text_input("Symptom Description")
    if st.button("Triage"):
        st.warning("Simulated triage... (LLM not yet connected)")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Internal Policy Assistant":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Internal Policy Assistant")
    question = st.text_input("Ask your policy question")
    if st.button("Ask"):
        st.info("Querying policy assistant... (To be implemented)")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Diagnostic Suggestion Tool":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Diagnostic Suggestion Tool")
    age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diag_input = st.text_area("Describe Symptoms", height=150)
    if st.button("Suggest Diagnostics"):
        st.error("AI suggestions may be unreliable — verify with clinicians.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Patient Report Viewer":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Your Reports")
    st.info("This would list reports generated for the logged-in patient.")
    # Placeholder logic
    st.markdown("""
    **Recent Report:**
    - Complaint: Headache and fatigue
    - Diagnosis: Mild dehydration
    - Medications: Oral rehydration salts, paracetamol
    """)
    st.markdown('</div>', unsafe_allow_html=True)
