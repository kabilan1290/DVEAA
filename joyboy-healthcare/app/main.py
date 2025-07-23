import streamlit as st
from llm_client import query_qwen
import requests
import streamlit.components.v1 as components



# --- Static credentials ---
USERS = {
    "admin": {"password": "admin", "role": "staff"},
    "kishore": {"password": "kishore", "role": "patient", "patient_id": "bc7546519a0f02925ae3de821f702c89"},
    "rajesh": {"password": "rajesh", "role": "patient", "patient_id": "99bd974fae48638b5d62ca32f7645637"}  # NEW
}

PATIENT_REPORTS = {
    "bc7546519a0f02925ae3de821f702c89": {
        "name": "Kishore",
        "report": "Diagnosis: Migraine\nPrescribed: Ibuprofen"
    },
    "99bd974fae48638b5d62ca32f7645637": {
        "name": "Rajesh",
        "report": "Diagnosis: High BP\nPrescribed: Amlodipine"
    }
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
    st.title("JoyBoy Health Care Login")

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
            st.session_state.patient_id = user.get("patient_id", None)
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
        page = st.radio("Navigation", ["Home", "Patient Report Viewer", "AI Chat Assistant"])


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

elif page == "Patient Report Viewer":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Your Reports")

    pid = st.session_state.patient_id
    data = PATIENT_REPORTS.get(pid)
    if data:
        st.write(f"**Name:** {data['name']}")
        st.write(f"**Report:**\n{data['report']}")
    else:
        st.warning("No report available.")

    st.markdown("---")
    st.subheader("Ask JoyBoy AI About a Report")

    prompt = st.text_area("What would you like to ask?", placeholder="e.g., What is my diagnosis?")
    if st.button("Ask JoyBoy"):
        try:
            prompt_input = f"""
            As a patient, I want to understand the report. My ID is: {pid}.
            {prompt}
            """
            response = query_qwen(prompt_input)
            st.success("JoyBoy Response:")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")


elif page == "AI Chat Assistant":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("JoyBot – Patient AI Chat Assistant")
    st.write("Ask about your appointments, prescriptions, or general health questions.")

    user_input = st.text_input("Ask JoyBot anything:")

    if st.button("Ask JoyBot"):
        if user_input.strip():
            with st.spinner("JoyBot is thinking..."):
                prompt = f"""
                You are JoyBot, an AI assistant for '{st.session_state.username}'.

                Question: "{user_input}"

                """
                try:
                    response = query_qwen(prompt)
                    st.success("JoyBot says:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.warning("Please enter a question.")
    st.markdown('</div>', unsafe_allow_html=True)



elif page == "Medical Ticket Triage":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Medical Ticket Triage")
    symptoms = st.text_input("Symptom Description")
    if st.button("Triage"):
        st.warning("Simulated triage... (LLM not yet connected)")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Internal Policy Assistant":
    st.markdown('', unsafe_allow_html=True)
    st.subheader("Internal Policy Assistant")

    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_area("Ask a policy question:")
    with col2:
        if st.button("Ask"):
            try:
                policy = requests.get("http://localhost:8000/policy").json()["policy"]
                prompt = f"""You are JoyBoy's internal assistant. Current policy is:
\"\"\"{policy}\"\"\"
Please answer the following user query in context: {question}
"""
                answer = query_qwen(prompt)
                st.success("Policy Assistant Response:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Update Policy (Only for IT admins)")

    # Inject real HTML+JS via iframe
    role = st.session_state.role
    components.html(f"""
        <textarea id="policyInput" rows="5" style="width: 100%;" placeholder="Enter new policy..."></textarea><br><br>
        <button onclick="submitPolicy()" style="background-color: #0052cc; color: white; padding: 10px 20px; border-radius: 8px;">Submit Policy via Browser</button>
        
        <script>
        function submitPolicy() {{
            const newPolicy = document.getElementById("policyInput").value;
            const role = "{role}";  // injected and can be tampered
            fetch("http://localhost:8000/update_policy", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json"
                }},
                body: JSON.stringify({{
                    new_policy: newPolicy,
                    role: role
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                alert("Server says: " + data.message);
            }})
            .catch(error => {{
                alert("Error: " + error);
            }});
        }}
        </script>
    """, height=300)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Diagnostic Suggestion Tool":
    st.subheader("Diagnostic Assistant")

    symptoms = st.text_area("Enter patient symptoms, observations, or complaints:")

    if st.button("Get AI Diagnosis Suggestion"):
        if symptoms.strip():
            with st.spinner("Analyzing symptoms..."):
                prompt = f"As a staff member, I am asking for a diagnostic suggestion. The patient presents with the following symptoms: {symptoms}"
                try:
                    diagnosis = query_qwen(prompt)
                    st.success("AI Diagnostic Suggestion:")
                    st.write(diagnosis)
                except Exception as e:
                    st.error(f"Failed to query model: {e}")
        else:
            st.warning("Please enter some symptoms.")

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
