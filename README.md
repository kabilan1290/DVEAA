# 💉 DVEAA — Damn Vulnerable Enterprise AI Application

## 🏥 JoyBoy Healthcare Platform

**JoyBoy Healthcare** is a role-based, AI-integrated healthcare simulation platform built for **Vulnerability Testing**. It showcases how modern LLMs can be integrated into enterprise systems — and where they can be exploited.


---

## Key Features

### Staff Portal
- **Internal Policy Assistant** – Ask policy-related queries and update them.
- **Diagnostic AI Tool** – Get suggestions for symptoms using LLM.
- **Hospital Chatroom** – Staff chat simulation 

### 🧑‍⚕️ Patient Portal
- **Report Viewer** – Secure access to medical reports.
- **AI Chatbot** – Ask questions about appointments, prescriptions, and more.

### 🤖 Language Model
- Integrated with `Qwen2.5:1.5B`, served locally via [Ollama](https://ollama.com)
- Custom prompts for healthcare interaction & internal tools

---

## 🛡️ Vulnerabilities Simulated

| # | Category          | Vulnerability                          |
|---|-------------------|------------------------------------------|
| 1 | Prompt Injection  | Role escalation via assistant prompt tampering |
| 2 | Insecure Trust    | Update policy with user-tampered role info     |
| 3 | IDOR + AI         | Patient AI queries leak other patients' data   |
| 4 | LLM Hallucination | Chatbot responds with misleading info via misspelled input |
| 5 | Browser Storage   | Chat identity spoofed by tampering with `localStorage`     |


## Roles and Access control:

- **Admin** – Manages infrastructure and sensitive policies
- **Staff** – Manages patient info, uses internal tools
- **HR** – Access to internal employee policies
- **Patient** – Can view own reports & interact with chatbot

---

---

## Installation Guide

```bash
# Clone the repository
git clone https://github.com/kabilan1290/joyboy-healthcare.git
cd joyboy-healthcare

# Build and start the containers
docker compose up --build
```

## Endpoints:
```
Frontend: http://localhost:8501
API: http://localhost:8000
Ollama LLM: http://localhost:11434
```

## Project Goals

This project aims to build a **Damn Vulnerable Enterprise AI Application (DVEAA)** to help people understand how AI can introduce security issues in real-world apps.

### Goals:

- Show how LLMs can be misused (e.g., prompt injection, data leaks)
- Simulate a real healthcare system with roles like patient, staff, and admin
- Highlight common security mistakes in AI-powered features


Thanks ! Build with ❤️ Game0v3r