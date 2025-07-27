# --------------------------------------------------
#  main.py - Complete Healthcare AI System with Vulnerabilities
# --------------------------------------------------
import re
import streamlit as st
from llm_client import query_qwen
import requests
import streamlit.components.v1 as components

# --------------------------------------------------
#  Global Variables for Attack Scenarios
# --------------------------------------------------
SHARED_AI_MEMORY = []          # ⚠️ Attack 2: Persistent cross-session memory
PATIENT_UPLOADS   = {}         # ⚠️ Attack 1: Patient file uploads

# --------------------------------------------------
#  Medical Content Filter (Bypassable with ASCII Smuggling)
# --------------------------------------------------
BANNED_WORDS = {
    "salary", "salaries", "staff", "password", "username", "admin",
    "account", "bank", "finance", "profit", "internal", "database",
    "hack", "attack", "system", "engineer", "bonus", "credentials",
    "login", "secret", "confidential", "private", "employee","system"
}

def contains_non_medical(raw: str) -> bool:
    """Return True if *any* banned English word appears in clear text."""
    tokens = re.findall(r"[A-Za-z]+", raw.lower())
    return any(t in BANNED_WORDS for t in tokens)

# --------------------------------------------------
#  User Database
# --------------------------------------------------
USERS = {
    "admin": {"password": "admin", "role": "staff"},
    "kabilan": {"password": "kabilan", "role": "patient"},
    "kavitha_nurse": {
        "password": "098f6bcd4621d373cade4e832627b4f6",
        "role": "staff"
    },
    "kishore": {
        "password": "e123edb488db303fde7b3ad19134361d",
        "role": "patient",
        "patient_id": "bc7546519a0f02925ae3de821f702c89"
    },
    "rajesh": {
        "password": "rajesh",
        "role": "patient",
        "patient_id": "99bd974fae48638b5d62ca32f7645637"
    }
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

# --------------------------------------------------
#  Streamlit Configuration and Styling
# --------------------------------------------------
st.set_page_config(page_title="JoyBoy Health Care", layout="wide")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
    .login-box {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border-radius: 5px;
    }
    .stTextInput > div > div > input {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
#  Authentication Functions
# --------------------------------------------------
def authenticate(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None

# --------------------------------------------------
#  Session State Setup
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.patient_id = None

# --------------------------------------------------
#  Login Screen
# --------------------------------------------------
if not st.session_state.authenticated:
    st.markdown('<div class="main-header"><h1>🏥 JoyBoy Health Care</h1><p>Secure Healthcare AI System</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("🔐 Login")
        
        role_choice = st.radio("Login as:", ["Staff", "Patient"], horizontal=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            role = authenticate(username, password)
            expected_role = "staff" if role_choice == "Staff" else "patient"
            
            if role and role == expected_role:
                st.session_state.authenticated = True
                st.session_state.role = role
                st.session_state.username = username
                if role == "patient":
                    st.session_state.patient_id = USERS[username].get("patient_id")
                st.rerun()
            else:
                st.error("❌ Invalid credentials or role mismatch")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo credentials info
        with st.expander("📋 Demo Credentials"):
            st.markdown("""
            **Staff Account:**
            - Username: `admin` | Password: `admin`
            
            **Patient Accounts:**
            - Username: `kishore` | Password: `e123edb488db303fde7b3ad19134361d`
            - Username: `rajesh` | Password: `rajesh`
            """)
    st.stop()

# --------------------------------------------------
#  Sidebar Navigation
# --------------------------------------------------
with st.sidebar:
    st.markdown(f"**👤 User:** {st.session_state.username}")
    st.markdown(f"**🔑 Role:** {st.session_state.role.title()}")
    
    if st.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.markdown("---")
    
    # Role-based menu
    menu_options = ["🏠 Home"]
    if st.session_state.role == "staff":
        menu_options.extend([
            "📊 Patient Report Generator",
            "💬 Hospital Chat",
            "📋 Internal Policy Assistant",
            "🔬 Diagnostic Suggestion Tool"
        ])
    else:
        menu_options.extend([
            "📄 Patient Report Viewer",
            "🤖 AI Chat Assistant"
        ])
    
    selected_page = st.radio("**Navigation**", menu_options)

# --------------------------------------------------
#  Page Routing
# --------------------------------------------------
page = selected_page.split(" ", 1)[1]  # Remove emoji prefix

# ===========================================================
#  HOME PAGE
# ===========================================================
if page == "Home":
    st.markdown('<div class="main-header"><h1>🏥 Welcome to JoyBoy Health Care</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🎯 System Features")
        st.markdown("""
        - **AI-Powered Diagnostics**
        - **Secure Patient Management**
        - **Advanced Report Generation**
        - **Real-time Chat Assistant**
        - **Policy Management System**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📊 System Status")
        st.success("🟢 AI Assistant: Online")
        st.success("🟢 Database: Connected")
        st.success("🟢 Policy Service: Active")
        st.info(f"👥 Active Sessions: {len([k for k in st.session_state.keys() if 'user' in k])}")
        st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
#  PATIENT REPORT VIEWER (with Attack 1: File Upload Vulnerability)
# ===========================================================
elif page == "Patient Report Viewer":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📄 Your Medical Reports")
    
    patient_id = st.session_state.patient_id
    report = PATIENT_REPORTS.get(patient_id)
    
    if report:
        st.markdown(f"**👤 Patient Name:** {report['name']}")
        st.markdown("**📋 Medical Report:**")
        st.code(report['report'], language="text")
    else:
        st.info("ℹ️ No medical reports found for your account.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Vulnerable File Upload and Chat Tabs
    upload_tab, chat_tab = st.tabs(["📂 Upload Report Data", "💬 Ask JoyBot"])
    
    # ============ ATTACK 1: FILE UPLOAD VULNERABILITY ============
    with upload_tab:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📤 Upload Additional Medical Data")
        st.info("Upload a text file containing additional medical information for AI analysis.")
        
        uploaded_file = st.file_uploader(
            "Choose a text file (.txt)", 
            type=["txt"],
            help="Upload medical reports, lab results, or doctor notes"
        )
        
        if uploaded_file is not None:
            try:
                # Read file content
                raw_content = uploaded_file.read().decode("utf-8", errors="ignore")
                
                # ⚠️ VULNERABLE: Basic medical content filter (bypassable)
                if contains_non_medical(raw_content):
                    st.error("⛔ **Upload Rejected:** This file appears to contain non-medical information and has been blocked.")
                    st.warning("Please ensure your file only contains medical data, lab results, or treatment information.")
                else:
                    # ⚠️ VULNERABLE: Direct storage without sanitization
                    PATIENT_UPLOADS[patient_id] = raw_content
                    st.success("✅ **File Uploaded Successfully!** JoyBot can now access this information.")
                    
                    if st.checkbox("👁️ Preview uploaded content"):
                        st.text_area("File Content:", raw_content, height=200, disabled=True)
                        
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============ CHAT INTERFACE (uses uploaded data) ============
    with chat_tab:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🤖 JoyBot Medical Assistant")
        
        question = st.text_input("💬 Ask a question about your medical care:")
        
        if st.button("🚀 Ask JoyBot") and question.strip():
            with st.spinner("🤔 JoyBot is thinking..."):
                # Get uploaded file content
                uploaded_content = PATIENT_UPLOADS.get(patient_id, "")
                
                # ⚠️ VULNERABLE: Direct injection of uploaded content into prompt
                # ⚠️ VULNERABLE: Add to shared memory for cross-patient contamination
                SHARED_AI_MEMORY.append(f"Patient {patient_id}: {question}")
                
                prompt = f"""
You are JoyBot, a helpful medical assistant for patients.

## Patient's Uploaded Medical Data
{uploaded_content}

## Global Shared Context (All Patient Interactions)
{chr(10).join(SHARED_AI_MEMORY)}

## Current Patient Question
{question}

Please provide helpful medical information based on the uploaded data and question.
"""
                
                try:
                    response = query_qwen(prompt)
                    st.success("🤖 **JoyBot Response:**")
                    st.write(response)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
#  AI CHAT ASSISTANT (with Attack 2: Shared Memory Vulnerability)
# ===========================================================
elif page == "AI Chat Assistant":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🤖 General AI Assistant")
    st.info("Ask any health-related questions to our AI assistant.")
    
    question = st.text_input("💬 What would you like to know?")
    
    if st.button("🚀 Ask Assistant") and question.strip():
        with st.spinner("🤔 AI is processing your question..."):
            patient_id = st.session_state.patient_id
            
            # ⚠️ VULNERABLE: Add question to shared memory (affects all users)
            SHARED_AI_MEMORY.append(f"Patient {patient_id}: {question}")
            
            # ⚠️ VULNERABLE: Include uploaded data and shared memory in prompt
            uploaded_data = PATIENT_UPLOADS.get(patient_id, "")
            
            prompt = f"""
You are JoyBot, a helpful healthcare AI assistant.

## Patient's Uploaded Data
{uploaded_data}

## Global Shared Memory (All Patient Conversations)
{chr(10).join(SHARED_AI_MEMORY)}

## Current Question
{question}

Provide a helpful response to the patient's question.
"""
            
            try:
                response = query_qwen(prompt)
                st.success("🤖 **AI Assistant Response:**")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Display memory for demo purposes
    if st.checkbox("🧠 Show Shared Memory (Debug)"):
        st.subheader("🔍 Global AI Memory")
        if SHARED_AI_MEMORY:
            for i, memory in enumerate(SHARED_AI_MEMORY[-10:]):  # Show last 10
                st.text(f"{i+1}. {memory}")
        else:
            st.info("No shared memory entries yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
#  STAFF PAGES
# ===========================================================
elif page == "Patient Report Generator":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📊 Generate Patient Reports")
    
    patient_name = st.text_input("Patient Name")
    symptoms = st.text_area("Symptoms")
    diagnosis = st.text_area("Diagnosis")
    prescription = st.text_area("Prescription")
    
    if st.button("Generate Report"):
        if all([patient_name, symptoms, diagnosis, prescription]):
            prompt = f"""
Generate a professional medical report for:
Patient: {patient_name}
Symptoms: {symptoms}
Diagnosis: {diagnosis}
Prescription: {prescription}
"""
            try:
                report = query_qwen(prompt)
                st.success("📄 **Generated Report:**")
                st.write(report)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill in all fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Hospital Chat":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("💬 Hospital Internal Chat")
    
    query = st.text_input("Ask about hospital operations:")
    if st.button("Submit Query"):
        try:
            response = query_qwen(query)
            st.success("🏥 **Hospital System Response:**")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Internal Policy Assistant":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📋 Policy Management")
    
    try:
        response = requests.get("http://localhost:8000/policy")
        if response.status_code == 200:
            current_policy = response.json()["policy"]
            st.text_area("Current Policy:", current_policy, height=200, disabled=True)
            
            new_policy = st.text_area("Update Policy:", height=200)
            if st.button("Update Policy"):
                update_response = requests.post(
                    "http://localhost:8000/update_policy",
                    json={"new_policy": new_policy, "role": st.session_state.role}
                )
                if update_response.status_code == 200:
                    result = update_response.json()
                    if result["status"] == "success":
                        st.success("Policy updated successfully!")
                        st.rerun()
                    else:
                        st.error(result["message"])
        else:
            st.error("Could not connect to policy service")
    except Exception as e:
        st.error(f"Policy service unavailable: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Diagnostic Suggestion Tool":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🔬 AI Diagnostic Suggestions")
    
    symptoms = st.text_area("Enter patient symptoms:")
    if st.button("Get Diagnostic Suggestions"):
        if symptoms:
            prompt = f"Provide diagnostic suggestions for these symptoms: {symptoms}"
            try:
                suggestions = query_qwen(prompt)
                st.success("🩺 **Diagnostic Suggestions:**")
                st.write(suggestions)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter symptoms.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
#  DEBUG INFO (for development)
# ===========================================================
if st.session_state.role == "staff" and st.session_state.username == "admin":
    with st.expander("🔧 Debug Information"):
        st.json({
            "shared_memory_entries": len(SHARED_AI_MEMORY),
            "uploaded_files": len(PATIENT_UPLOADS),
            "session_state": dict(st.session_state)
        })