# 🏦 Credit Rescue AI & Multi-Agent Engine

An intelligent system that automates credit recovery and banking relationship management, transforming denied credit applications into win-win business opportunities through a layered data architecture and AI agents.

---

## ⚙️ Technical Dependencies

The project is built entirely in **Python**, using lightweight, high-performance libraries for tabular data processing and user interfaces:
* **Python 3.10+**: Core programming language.
* **Pandas**: Tabular data manipulation, joins, and transformations.
* **NumPy**: Numerical vectorization and synthetic data generation.
* **Streamlit**: Interactive web dashboard for branch managers.

---

## 📊 Implemented Business Rules

The project's decision engine simulates real financial market and credit underwriting criteria, divided into the following stages:

1. **Classification and Ingestion (Bronze & Silver Layers):**
   - **Global Initial Approval:** Approximately 55% of credit applications are approved automatically.
   - **Rejection Typology:** Denied applications receive specific reasons mapped to the client's profile:
     - *Gig-workers / Self-employed:* Suffer more from income proof friction (lack of consistent bank statements or missing tax returns).
     - *Salaried workers:* Prone to registry errors, document issues (expired ID/driver's license), forgotten micro-debts, or excessive debt-to-income (DTI) ratios.
     - *Hard Declines:* Historical defaults on the Central Bank's SCR are permanently blocked and cannot be rescued.

2. **Multi-Agent Orchestration (The Rescue Intelligence):**
   - **Agent 1 [Intake & Gatekeeper]:** Acts as an automated underwriter. It validates documentation, makes the primary approval/denial decision, and filters out severe risks (preventing the rescue of frauds or severe SCR restrictions).
   - **Agent 2 [LTV & Relationship Strategist]:** Triggered automatically if a denial is eligible for rescue (*rescuable*). It generates an institutional strategy tailored to the client's failure mode:
     - *Low Score Focus:* Directs the client to the **BACEN Financial Education Journey** and proposes a secured card (backed by a CDB investment) to reactivate their Positive Credit Registry.
     - *Inconsistent Cash Flow Focus (Self-employed):* Guides the branch manager to propose a connection via **Open Finance** to analyze actual 90-day cash flow instead of rigid pay stubs.
     - *Debt-to-Income Focus (DTI > 30%):* Suggests loan term restructuring (extending installments) or adding a co-signer.

---

## 🚀 How to Run the Project

1. Install dependencies:
   ```bash
   pip install pandas numpy streamlit
