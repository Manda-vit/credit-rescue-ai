# Credit Rescue AI & Multi-Agent Engine

An intelligent system that automates credit recovery and banking relationship management, transforming denied credit applications into win-win business opportunities through a layered data architecture and multi-agent orchestration.

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technical Dependencies](#technical-dependencies)
- [Business Rules](#business-rules)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Credit Rescue AI is a sophisticated multi-agent system designed to help financial institutions recover denied credit applications by:

1. **Analyzing** rejection reasons and client profiles
2. **Orchestrating** intelligent agent workflows
3. **Generating** personalized recovery strategies
4. **Optimizing** relationship management and customer retention

The system operates through a layered data architecture (Bronze, Silver, Gold) and uses AI-driven agents to identify recovery opportunities and propose tailored solutions.

---

## Key Features

✅ **Automated Credit Triage** - Classify applications and identify rescue-eligible denials  
✅ **Multi-Agent Intelligence** - Coordinated AI agents for underwriting and strategy generation  
✅ **Personalized Recovery Strategies** - Tailored recommendations based on rejection typology  
✅ **Interactive Dashboard** - Real-time visualizations for branch managers  
✅ **Open Finance Integration** - Connect with Brazilian Open Finance ecosystem  
✅ **Scalable Python Stack** - Lightweight, high-performance libraries  

---

## Technical Dependencies

The project is built entirely in **Python 3.10+**, leveraging lightweight, high-performance libraries:

| Dependency | Purpose |
|-----------|---------|
| **Python 3.10+** | Core programming language |
| **Pandas** | Tabular data manipulation, joins, and transformations |
| **NumPy** | Numerical vectorization and synthetic data generation |
| **Streamlit** | Interactive web dashboard for branch managers |

---

## Business Rules

The project's decision engine simulates real financial market and credit underwriting criteria:

### 1. Classification & Ingestion (Bronze & Silver Layers)

- **Global Initial Approval Rate:** ~55% of credit applications are approved automatically
- **Rejection Typology:** Denied applications are categorized based on client profile:

| Client Type | Common Rejection Reasons |
|-------------|------------------------|
| **Gig-workers / Self-employed** | Income proof friction (lack of consistent bank statements, missing tax returns) |
| **Salaried workers** | Registry errors, expired documents (ID/driver's license), micro-debts, excessive DTI (>30%) |
| **Hard Declines** | Historical defaults on Central Bank SCR (permanently blocked, non-rescuable) |

### 2. Multi-Agent Orchestration (The Rescue Intelligence)

#### **Agent 1: Intake & Gatekeeper**
- Acts as an automated underwriter
- Validates documentation and makes primary approval/denial decisions
- Filters out severe risks (hard declines, non-rescuable cases)
- Determines eligibility for rescue workflow

#### **Agent 2: LTV & Relationship Strategist**
- Triggered automatically for rescuable denials
- Generates institution-specific recovery strategies based on failure mode
- Proposes tailored recovery pathways:

| Failure Mode | Recommended Strategy |
|-------------|---------------------|
| **Low Credit Score** | Direct to BACEN Financial Education Journey; propose secured card (CDB-backed) to reactivate Positive Credit Registry |
| **Inconsistent Cash Flow** | Propose Open Finance connection for 90-day cash flow analysis instead of rigid pay stubs |
| **High DTI (>30%)** | Suggest loan term restructuring (extended installments) or co-signer option |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Bronze Layer (Raw Data)                    │
│              (Credit applications, client profiles)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Silver Layer (Cleaned)                      │
│            (Standardized formats, categorized reasons)        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Agent 1: Intake & Gatekeeper                    │
│          (Validation, Approval/Denial, Risk Filter)          │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
    ┌───▼────┐              ┌────────▼───┐
    │  Hard  │              │ Rescuable  │
    │Decline │              │  Denials   │
    └────────┘              └────────┬───┘
                                     │
                        ┌────────────▼───────────┐
                        │ Agent 2: LTV &         │
                        │ Relationship Strategist│
                        │ (Recovery strategies)  │
                        └────────────┬───────────┘
                                     │
┌──────────────────────────────────▼─────────────────────────┐
│                   Gold Layer (Insights)                     │
│            (Recovery strategies, recommendations)            │
└──────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼────────┐
                    │ Streamlit        │
                    │ Dashboard        │
                    │ (Branch Manager) │
                    └──────────────────┘
```

---

## Installation

### Prerequisites
- Python 3.10 or higher
- pip or conda package manager

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Manda-vit/credit-rescue-ai.git
   cd credit-rescue-ai
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pandas numpy streamlit
   ```

---

## Usage

### Running the Dashboard

Start the Streamlit web application:

```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

### Basic Workflow

1. **Upload credit application data** (CSV/Excel)
2. **Run intake processing** - Agent 1 validates and categorizes applications
3. **Review recovery strategies** - Agent 2 generates tailored recommendations
4. **Export insights** - Download recovery action plans for branch managers

---

## Project Structure

```
credit-rescue-ai/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── app.py                    # Streamlit main application
├── src/
│   ├── agents/              # Multi-agent orchestration
│   │   ├── intake_agent.py  # Agent 1: Gatekeeper logic
│   │   └── strategist_agent.py  # Agent 2: Recovery strategist
│   ├── data/                # Data processing layers
│   │   ├── bronze.py        # Raw data ingestion
│   │   ├── silver.py        # Data cleaning & standardization
│   │   └── gold.py          # Insights & transformations
│   └── utils/               # Helper functions
│       ├── config.py        # Configuration settings
│       └── validators.py    # Data validation
├── data/
│   ├── sample_applications.csv
│   └── rejection_rules.json
└── tests/                   # Unit and integration tests
    └── test_agents.py
```

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code includes tests and follows PEP 8 style guidelines.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support & Contact

For questions, issues, or feedback:
- Open an [Issue](https://github.com/Manda-vit/credit-rescue-ai/issues)
- Contact: [Your Contact Info]

---

**Last Updated:** September 2026  
**Status:** Active Development
