# scope3-emission-prototype-trail-1
Hackathon MVP for Scope-3 emission estimation using NLP and dashboards
# 🌱 Scope-3 Carbon Tracker (Hackathon MVP)

A hackathon-ready prototype that estimates **Scope-3 supply-chain carbon emissions** from unstructured supplier documents using **OCR-style extraction, deterministic calculations, and full audit traceability**.

This project is designed as a **decision-support tool**, not a compliance or regulatory filing system.

---

## 🚀 Features

- Upload supplier documents (invoices, shipping files, utility records)
- Assign uploads to **custom batches** (e.g., monthly reporting periods)
- Extract activity data using mocked NLP/LLM logic
- Estimate emissions using **standard emission factors**
- Maintain **full upload history**
- **Manually compare batches** to see emission increases or reductions
- View a transparent **audit trail** for every calculation

---

## 🏗️ Architecture Overview

- **Backend:** FastAPI (Python)
  - `/process` → process document + batch
  - `/history` → retrieve all past uploads
- **Frontend:** Streamlit
  - Upload interface
  - Batch comparison
  - Audit history table
- **Computation:** Deterministic Python functions
- **Data Storage:** In-memory history (MVP-level)

---

## 🧰 Tech Stack

- Python 3.10+
- FastAPI
- Streamlit
- Requests
- Pandas

---

## ▶️ How to Run

### 1️⃣ Start Backend

```bash
uvicorn main:app --reload
