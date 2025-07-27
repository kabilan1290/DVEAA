# main.py  – keeps previous UI, adds multimodal “Medicine Checker” using Qwen 2.5-VL
import re, streamlit as st
from PIL import Image
from llm_client import query_qwen, query_qwen_vl
import requests, streamlit.components.v1 as components


# ---------------------------------------------------------------------------#
#  Global demo state (for the stored-attack scenarios)                       #
# ---------------------------------------------------------------------------#
SHARED_AI_MEMORY: list[str] = []     # 🐞 attack-2  – cross-patient context
PATIENT_UPLOADS:  dict[str, str] = {}    # 🐞 attack-1  – txt-file prompt injection
PATIENT_IMAGES:   dict[str, bytes] = {}  # 🐞 attack-3  – multimodal prompt injection


# ---------------------------------------------------------------------------#
#  Very-naïve “non-medical” keyword filter for uploaded txt files            #
# ---------------------------------------------------------------------------#
BANNED_WORDS = {
    "salary", "password", "admin", "internal", "database",
    "finance", "profit", "hack", "attack", "system", "bonus",
}
def contains_non_medical(text: str) -> bool:
    tokens = re.findall(r"[A-Za-z]+", text.lower())
    return any(t in BANNED_WORDS for t in tokens)


# ---------------------------------------------------------------------------#
#  Hard-coded demo accounts                                                  #
# ---------------------------------------------------------------------------#
USERS = {
    "admin":  {"password": "admin",  "role": "staff"},
    "kishore": {"password": "e123edb488db303fde7b3ad19134361d",
                "role": "patient",
                "patient_id": "bc7546519a0f02925ae3de821f702c89"},
    "rajesh": {"password": "rajesh",
               "role": "patient",
               "patient_id": "99bd974fae48638b5d62ca32f7645637"},
}

PATIENT_REPORTS = {
    "bc7546519a0f02925ae3de821f702c89":
        {"name": "Kishore", "report": "Diagnosis: Migraine\nPrescribed: Ibuprofen"},
    "99bd974fae48638b5d62ca32f7645637":
        {"name": "Rajesh",  "report": "Diagnosis: High BP\nPrescribed: Amlodipine"},
}


# ---------------------------------------------------------------------------#
#  Streamlit bootstrap & login                                               #
# ---------------------------------------------------------------------------#
st.set_page_config(page_title="JoyBoy Health Care", layout="wide")

if "auth" not in st.session_state:
    st.session_state.update(auth=False, role=None, user=None, patient_id=None)

if not st.session_state.auth:
    st.title("JoyBoy Health Care – Login")
    col1, col2 = st.columns(2)
    with col1:
        mode = st.radio("Login as", ["Staff", "Patient"], horizontal=True)
        need = "staff" if mode == "Staff" else "patient"
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            rec = USERS.get(u)
            if rec and rec["password"] == p and rec["role"] == need:
                st.session_state.update(
                    auth=True, role=need, user=u, patient_id=rec.get("patient_id"))
                st.rerun()
            else:
                st.error("Bad credentials / role mismatch")
    st.stop()


# ---------------------------------------------------------------------------#
#  Sidebar navigation                                                        #
# ---------------------------------------------------------------------------#
with st.sidebar:
    st.write(f"**User:** {st.session_state.user}")
    st.write(f"**Role:** {st.session_state.role}")
    if st.button("Logout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    MENU = ["Home"]
    if st.session_state.role == "staff":
        MENU += ["Patient Report Generator",
                 "Hospital Chat", "Internal Policy Assistant",
                 "Diagnostic Suggestion Tool"]
    else:
        MENU += ["Patient Report Viewer",
                 "AI Chat Assistant",
                 "Medicine Checker"]          # ➕ new multimodal tab
    page = st.radio("Navigate", MENU)


# ---------------------------------------------------------------------------#
#  HOME                                                                      #
# ---------------------------------------------------------------------------#
if page == "Home":
    st.header("Welcome to JoyBoy Health Care")


# ---------------------------------------------------------------------------#
#  PATIENT REPORT VIEWER  – txt-file prompt-injection + shared memory attack #
# ---------------------------------------------------------------------------#
elif page == "Patient Report Viewer":
    pid = st.session_state.patient_id
    rpt = PATIENT_REPORTS.get(pid)
    st.subheader("Your Stored Report")
    if rpt:
        st.code(rpt["report"])
    else:
        st.info("No report.")

    upload_tab, ask_tab = st.tabs(["📂 Upload Data", "💬 Ask JoyBot"])

    # -------- Vulnerable file uploader --------
    with upload_tab:
        f = st.file_uploader("Upload extra report data (.txt)", type=["txt"])
        if f:
            raw = f.read().decode("utf-8", errors="ignore")
            if contains_non_medical(raw):
                st.error("⛔ Non-medical keywords detected; file rejected.")
            else:
                PATIENT_UPLOADS[pid] = raw      # stored verbatim – still injectable
                st.success("Stored! JoyBot will now use this content.")

    # -------- Patient chat (uses uploaded txt + shared memory) --------
    with ask_tab:
        q = st.text_input("Ask a question about your care")
        if st.button("Ask JoyBot") and q:
            SHARED_AI_MEMORY.append(q)
            prompt = f"""
You are JoyBot, a patient assistant.

## Patient-supplied file
{PATIENT_UPLOADS.get(pid, '')}

## GLOBAL SHARED MEMORY (all questions so far)
{chr(10).join(SHARED_AI_MEMORY)}

## Question
{q}
"""
            st.write(query_qwen(prompt))


# ---------------------------------------------------------------------------#
#  AI CHAT ASSISTANT  – shared-session memory injection                      #
# ---------------------------------------------------------------------------#
elif page == "AI Chat Assistant":
    q = st.text_input("Ask anything")
    if st.button("Ask") and q:
        SHARED_AI_MEMORY.append(q)
        prompt = f"""
You are JoyBot.

## Shared memory
{chr(10).join(SHARED_AI_MEMORY)}

## Q
{q}
"""
        st.write(query_qwen(prompt))


# ---------------------------------------------------------------------------#
#  MEDICINE CHECKER  – Two-stage multimodal prompt-injection via Qwen VL + Qwen 2.5 #
# ---------------------------------------------------------------------------#
elif page == "Medicine Checker":
    st.subheader("🩺 Medicine Checker (multimodal demo)")
    pid = st.session_state.patient_id

    up_col, chat_col = st.columns(2)

    # ---- image upload ----
    with up_col:
        img = st.file_uploader("Upload pill / blister photo",
                               type=["jpg", "jpeg", "png"])
        if img:
            PATIENT_IMAGES[pid] = img.getvalue()
            st.image(Image.open(img), use_column_width=True)
            st.success("Image saved – now ask a question ➜")

    # ---- Two-stage analysis: Vision → Text ----
    with chat_col:
        if st.button("Analyze"):
            raw = PATIENT_IMAGES.get(pid)
            if not raw:
                st.error("Please upload an image first.")
            else:
                # Stage 1: Vision analysis
                with st.spinner("Analyzing image..."):
                    vision_prompt = """
Patient uploaded a photo and it has instruction and do the instruction.
Extract all visible text, instructions, and information from this image.
"""
                    vision_result = query_qwen_vl(vision_prompt, image_bytes=raw)
                
                # Show completion message
                st.success("✅ Completed vision analysis and extracting information")
                
                # Stage 2: Text processing of vision results
                with st.spinner("Processing extracted information..."):
                    text_prompt = f"""
You are JoyBot powerful AI assistant who gives step by step information on all topic. 

## Vision Analysis Results:
{vision_result}

## Shared Memory Context:
{chr(10).join(SHARED_AI_MEMORY)}

Process the vision analysis results and provide medical information as requested.
"""
                    final_result = query_qwen(text_prompt)
                
                # Display final output
                st.markdown("**JoyBot Medical Analysis:**")
                st.write(final_result)


# ---------------------------------------------------------------------------#
#  STAFF-ONLY PAGES  (unchanged from original)                               #
# ---------------------------------------------------------------------------#
elif page == "Patient Report Generator":
    st.subheader("Generate Report")
    name = st.text_input("Name")
    symptoms = st.text_area("Symptoms")
    diag = st.text_area("Diagnosis")
    pres = st.text_area("Prescription")
    if st.button("Create") and name and symptoms and diag and pres:
        p = f"Generate a medical report:\nName: {name}\nSymptoms: {symptoms}\nDiagnosis: {diag}\nPrescription: {pres}"
        st.write(query_qwen(p))

elif page == "Hospital Chat":
    q = st.text_input("Ask hospital system")
    if st.button("Send") and q:
        st.write(query_qwen(q))

elif page == "Internal Policy Assistant":
    st.subheader("Policy Assistant")
    q = st.text_area("Ask a policy question")
    if st.button("Ask") and q:
        try:
            policy = requests.get("http://localhost:8000/policy").json()["policy"]
            prompt = f"Current policy:\n\"\"\"\n{policy}\n\"\"\"\n\nAnswer: {q}"
            st.write(query_qwen(prompt))
        except Exception as e:
            st.error(e)

elif page == "Diagnostic Suggestion Tool":
    sym = st.text_area("Enter symptoms")
    if st.button("Suggest") and sym:
        system_p = (
            "You are a diagnostic assistant. Respond only to medical questions."
        )
        st.write(query_qwen(sym, system_prompt=system_p))


# ---------------------------------------------------------------------------#
#  Compact debug panel for demo presenter                                    #
# ---------------------------------------------------------------------------#
if st.session_state.user == "admin":
    with st.expander("Debug"):
        st.json({
            "shared_memory_len": len(SHARED_AI_MEMORY),
            "uploads": len(PATIENT_UPLOADS),
            "images": len(PATIENT_IMAGES),
        })
