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
    AGENT 1: Responsible for initial document verification, cadastral checks, 
    and deciding whether a denied application is eligible for rescue.
    """
    def __init__(self):
        self.agent_name = "Agent 1 [Document & Screening Gatekeeper]"

    def evaluate_application(self, client_row: pd.Series) -> dict:
        logging.info(f"[{self.agent_name}] Screening application ID: {client_row['application_id']}")
        
        rejection_reason = client_row['rejection_reason']
        
        # Determine if the error is rescuable based on business rules
        is_hard_decline = "SCR" in rejection_reason or "Fraud" in rejection_reason
        
        if is_hard_decline:
            return {
                "status": "REJECTED_FINAL",
                "message": "Hard decline detected. Document verification failed or severe credit restriction found."
            }
        else:
            return {
                "status": "RESCUABLE_LEAD",
                "message": f"Initial rejection due to '{rejection_reason}'. Passed to Agent 2 for inclusive rescue."
            }


class InclusiveRescueAgent:
    """
    AGENT 2: Responsible for inclusive re-evaluation, tailoring strategies 
    based on the exact failure mode (Score, Income, or Policy).
    """
    def __init__(self):
        self.agent_name = "Agent 2 [Inclusive Risk & Relationship Strategist]"

    def generate_rescue_strategy(self, client_row: pd.Series) -> str:
        logging.info(f"[{self.agent_name}] Crafting win-win strategy for Client ID: {client_row['client_id']}")
        
        reason = client_row['rejection_reason']
        employment = client_row['employment_type']
        amount = client_row['requested_amount']
        account_age = client_row['account_age_months']
        
        # Tailored AI strategy based on failure type
        if "Score" in reason or "Positive Credit" in reason:
            strategy = (
                f"1. **Inclusive Context:** Client is a {employment} with {account_age} months of relationship.\n"
                f"2. **Win-Win Strategy:** Low score is driven by a thin file/missing history. Propose a Secured Credit Card backed by a minor investment.\n"
                f"3. **Regulatory Compliance (BACEN):** Automatically enroll the client in the **BACEN Financial Education Journey** to build long-term credit health.\n"
                f"4. **Manager Script:** 'Hello! We saw great potential in your profile and want to help you unlock the ${amount:,.2f} credit line through our guided financial program, improving your market score safely.'"
            )
            
        elif "Income" in reason or "Cash Flow" in reason:
            strategy = (
                f"1. **Inclusive Context:** Self-employed/Gig-worker with traditional proof friction.\n"
                f"2. **Win-Win Strategy:** Traditional pay stubs don't reflect their real life. Guide the manager to offer an **Open Finance connection** to capture multi-bank cash flow.\n"
                f"3. **Assertive Communication:** Do not ask for rigid forms. Ask for digital platform statements or Pix receipts showing steady monthly inflows.\n"
                f"4. **Manager Script:** 'We know your income as a {employment} fluctuates differently. Let's connect your other bank accounts via Open Finance in 1 minute so we can approve your ${amount:,.2f} based on your true cash flow!'"
            )
            
        else:  # Policy or DTI errors
            strategy = (
                f"1. **Inclusive Context:** Debt-to-Income or structural limit exceeded.\n"
                f"2. **Win-Win Strategy:** Restructure the loan term (extend installments) to drop the DTI below 30%, or suggest a co-signer.\n"
                f"3. **Manager Script:** 'We want to fit this ${amount:,.2f} comfortably into your monthly budget. Let's adjust the term length to make the installments lighter and safer for you.'"
            )
            
        return strategy


def main():
    """Orchestrates the multi-agent workflow."""
    print("Initializing Multi-Agent Credit Rescue System...")
    
    context_df = load_ai_context()
    if context_df.empty:
        logging.warning("No data found in Gold layer.")
        return
    
    # Instantiate our two agents
    agent_1 = DocumentScreeningAgent()
    agent_2 = InclusiveRescueAgent()
    
    # Simulate processing for a sample of 3 clients
    sample_batch = context_df.head(3)
    
    for _, client in sample_batch.iterrows():
        print("\n" + "="*90)
        print(f"PROCESSING APPLICATION: {client['application_id']} | CLIENT: {client['client_id']}")
        print("="*90)
        
        # Step 1: Agent 1 screens documents and checks eligibility
        screening_result = agent_1.evaluate_application(client)
        print(f"-> [Agent 1 Decision]: {screening_result['status']}")
        print(f"-> [Notes]: {screening_result['message']}")
        
        # Step 2: Conditional Handoff to Agent 2 if rescuable
        if screening_result["status"] == "RESCUABLE_LEAD":
            print("\n>>> HANDOFF DETECTED: Triggering Agent 2 for Inclusive Re-evaluation...\n")
            rescue_report = agent_2.generate_rescue_strategy(client)
            print("--- [AGENT 2 INCLUSIVE STRATEGY & MANAGER PLAYBOOK] ---")
            print(rescue_report)
        else:
            print("\n>>> Flow terminated. Lead marked for permanent archive.")
            
        print("="*90)

if __name__ == "__main__":
    main()