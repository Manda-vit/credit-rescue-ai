import pandas as pd
from pathlib import Path
import logging

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GOLD_DATA_PATH = Path('data/gold/mart_ai_client_context.csv')

def load_ai_context() -> pd.DataFrame:
    """Loads the AI-ready context table from the Gold layer."""
    if not GOLD_DATA_PATH.exists():
        raise FileNotFoundError(f"Gold data not found at {GOLD_DATA_PATH}. Run gold_layer_processor.py first.")
    return pd.read_csv(GOLD_DATA_PATH)


class DocumentScreeningAgent:
    """
    AGENT 1 [Intake & Eligibility Gatekeeper]:
    Responsible for simulating document intake, validating raw application parameters, 
    making the final Approve/Deny decision, and assessing whether a denial is rescuable.
    """
    def __init__(self):
        self.name = "Agent 1 [Intake & Gatekeeper]"

    def process_application(self, client_row: pd.Series) -> dict:
        logging.info(f"[{self.name}] Analyzing documents for Application ID: {client_row['application_id']}")
        
        status = client_row['status']
        reason = client_row['rejection_reason']
        
        # If the system originally approved it, Agent 1 validates it successfully
        if status == 'Approved':
            return {
                "decision": "APPROVED",
                "route_to_agent_2": False,
                "notes": "Documents and parameters passed all underwriting compliance rules."
            }
        
        # If denied, check if it's a hard decline vs rescuable error
        is_hard_decline = "SCR" in reason or "Fraud" in reason
        
        if is_hard_decline:
            return {
                "decision": "DENIED_FINAL",
                "route_to_agent_2": False,
                "notes": f"Hard decline triggered due to severe restriction ({reason}). No rescue permitted."
            }
        else:
            return {
                "decision": "DENIED_RESCUABLE",
                "route_to_agent_2": True,
                "notes": f"Denial due to operational/credit friction ({reason}). Eligible for rescue workflow."
            }


class InstitutionalRescueAgent:
    """
    AGENT 2 [Institutional Risk & LTV Strategist]:
    Responsible for deep behavioral re-evaluation, regulatory compliance (BACEN), 
    financial value estimation (LTV protection), and crafting executive manager playbooks.
    """
    def __init__(self):
        self.name = "Agent 2 [LTV & Relationship Strategist]"

    def execute_rescue_strategy(self, client_row: pd.Series) -> str:
        logging.info(f"[{self.name}] Building institutional rescue strategy for Client ID: {client_row['client_id']}")
        
        reason = client_row['rejection_reason']
        employment = client_row['employment_type']
        amount = client_row['requested_amount']
        tenure = client_row['account_age_months']
        segment = client_row['segment']
        
        # Market-grade intelligence formatting based on failure type
        if "Score" in reason or "Positive Credit" in reason:
            strategy = f"""
            ====================================================================================
            📊 INSTITUTIONAL CREDIT RECOVERY REPORT (MARKET-GRADE)
            ====================================================================================
            1. **Client & Portfolio Value Context:**
               - Segment: {segment} | Tenure: {tenure} months with the bank.
               - Core Issue: Thin file / Low traditional score driving a false-positive rejection.
               - LTV Impact: Rescuing this client preserves an estimated lifetime banking value of ~${amount * 0.12:,.2f} in cross-sell potential (investments, insurance).

            2. **Win-Win Alternative Structure:**
               - Product Recommendation: **Secured Credit Line / Credit Builder Card**.
               - Risk Mitigation: 100% collateralized by a micro-investment certificate (CDB Garantia), reducing default risk to near zero while establishing credit history.

            3. **Regulatory Compliance (BACEN Mandate):**
               - Action: Seamlessly enroll the client in the **BACEN Financial Education Journey**. This fulfills regulatory social responsibility requirements and automatically re-activates their Positive Credit Registry (Cadastro Positivo).

            4. **Branch Manager Playbook & Outreach Script:**
               - *Context for Manager:* "This client has been with us for {tenure} months. Their rejection was purely mechanical due to lack of bureau history."
               - *Script:* "Hello! We reviewed your application for ${amount:,.2f}. Because we value our {tenure}-month relationship, we’ve unlocked a guided financial program that safely approves your credit while building your market score."
            ====================================================================================
            """
            
        elif "Income" in reason or "Cash Flow" in reason:
            strategy = f"""
            ====================================================================================
            📊 INSTITUTIONAL CREDIT RECOVERY REPORT (MARKET-GRADE)
            ====================================================================================
            1. **Client & Portfolio Value Context:**
               - Employment: {employment} | Tenure: {tenure} months.
               - Core Issue: Traditional income proof friction (rigid pay stubs do not capture gig-economy or self-employed cash flow).
               - LTV Impact: High attrition risk if turned away; gig-workers represent the fastest-growing segment for transaction fees.

            2. **Win-Win Alternative Structure:**
               - Product Recommendation: **Open Finance Cash Flow Underwriting**.
               - Risk Mitigation: Bypass standard formal income docs by pulling 90-day multi-bank transactional data via Open Finance API to verify real-time liquidity.

            3. **Regulatory Compliance & Data Enrichment:**
               - Action: Request digital platform statements or Pix-based cash-flow history directly via secure banking channel.

            4. **Branch Manager Playbook & Outreach Script:**
               - *Context for Manager:* "Standard pay stubs failed, but their account movement shows consistent inflows."
               - *Script:* "We know your income as a {employment} flows dynamically. Let's connect your accounts via Open Finance in 1 minute so we can approve your ${amount:,.2f} based on your true cash flow!"
            ====================================================================================
            """
            
        else: # Policy / Debt-to-Income
            strategy = f"""
            ====================================================================================
            📊 INSTITUTIONAL CREDIT RECOVERY REPORT (MARKET-GRADE)
            ====================================================================================
            1. **Client & Portfolio Value Context:**
               - Segment: {segment} | Requested Amount: ${amount:,.2f}.
               - Core Issue: Debt-to-Income (DTI) ratio exceeded the conservative 30% policy threshold.

            2. **Win-Win Alternative Structure:**
               - Product Recommendation: **Loan Term Restructuring / Co-signer Inclusion**.
               - Risk Mitigation: Extend installment duration to reduce monthly commitment below 30%, or introduce a co-obligor to share credit exposure.

            3. **Branch Manager Playbook & Outreach Script:**
               - *Context for Manager:* "The initial structure overextended their monthly budget. Restructuring saves the deal."
               - *Script:* "We want this ${amount:,.2f} loan to fit comfortably into your monthly budget without pressure. Let's adjust the term length to make installments lighter and safer for your financial health."
            ====================================================================================
            """
            
        return strategy.strip()


def main():
    """Orchestrates the multi-agent credit pipeline demo."""
    print("Initializing Multi-Agent Credit Engine...")
    
    context_df = load_ai_context()
    if context_df.empty:
        logging.warning("No data found in Gold layer.")
        return
    
    # Instantiate agents
    intake_agent = DocumentScreeningAgent()
    rescue_agent = InstitutionalRescueAgent()
    
    # Process a sample batch of applications
    sample_batch = context_df.head(3)
    
    for _, client in sample_batch.iterrows():
        print("\n" + "#"*90)
        print(f"PROCESSING BATCH ITEM -> App ID: {client['application_id']} | Client: {client['client_id']}")
        print("#"*90)
        
        # Step 1: Agent 1 evaluates documents and application status
        screening_res = intake_agent.process_application(client)
        print(f"👉 [{intake_agent.name}] Decision: {screening_res['decision']}")
        print(f"   [Details]: {screening_res['notes']}")
        
        # Step 2: Conditional routing to Agent 2 if rescuable
        if screening_res['route_to_agent_2']:
            print("\n🔄 [HANDOFF DETECTED] Routing case to Agent 2 for Institutional Rescue Analysis...\n")
            report = rescue_agent.execute_rescue_strategy(client)
            print(report)
        else:
            print("\n⛔ [WORKFLOW TERMINATED] Case closed. No agent handoff required.")
            
        print("#"*90 + "\n")

if __name__ == "__main__":
    main()