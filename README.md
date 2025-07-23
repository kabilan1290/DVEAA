# DVEAA
DAMN Vulnerable Enterprise AI Application

# JoyBoy Healthcare Platform

**JoyBoy Healthcare** is a role-based AI-augmented healthcare simulation platform that supports doctors, staff, and patients with internal tooling powered by LLMs. It demonstrates real-world workflows while also showcasing common security flaws for educational and red-team training purposes.

---

## 📌 Key Features

###️ Staff Portal
- Patient Report Generator (LLM-assisted)
- Medical Ticket Triage Tool
- Internal Policy Assistant with Update Interface
- Diagnostic Suggestion Tool
- Secure Hospital Chatroom (localStorage-powered)

### Patient Portal
- Personal Report Viewer
- Interactive Chatbot (LLM-backed)

### Language Model Integration
- Uses `Qwen2.5:1.5B` served locally via [Ollama](https://ollama.com)

---


# to run:
streamlit run main.py --browser.gatherUsageStats false
python3 api.py
