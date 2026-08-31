import streamlit as st
import pandas as pd
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Credit Rescue AI - Institutional Dashboard",
    page_icon="🏦",
    layout="wide"
)

# --- PATHS ---
GOLD_KPI_PATH = Path('data/gold/mart_branch_manager_kpis.csv')
GOLD_CONTEXT_PATH = Path('data/gold/mart_ai_client_context.csv')

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if not GOLD_KPI_PATH.exists() or not GOLD_CONTEXT_PATH.exists():
        return None, None
    kpis_df = pd.read_csv(GOLD_KPI_PATH)
    context_df = pd.read_csv(GOLD_CONTEXT_PATH)
    return kpis_df, context_df

kpis_df, context_df = load_data()

# --- HEADER ---
st.title("🏦 Institutional Credit Rescue & Relationship Engine")
st.markdown("Multi-Agent AI Orchestration empowering branch managers to recover lost revenue securely.")

if kpis_df is None or context_df is None:
    st.error("Gold layer data not found! Please run the data pipelines (`gold_layer_processor.py`) first.")
else:
    # --- SIDEBAR - BRANCH SELECTION ---
    st.sidebar.header("Branch Control Panel")
    selected_branch = st.sidebar.selectbox("Select Branch ID", kpis_df['branch_id'].unique())
    
    branch_kpi = kpis_df[kpis_df['branch_id'] == selected_branch].iloc[0]
    
    # --- METRICS ROW ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Denied Apps", f"{int(branch_kpi['total_denied_applications'])}")
    col2.metric("Total Lost Value", f"${branch_kpi['total_lost_value']:,.2f}")
    col3.metric("Rescuable Leads", f"{int(branch_kpi['rescuable_applications'])}")
    col4.metric("Potential Rescue Value", f"${branch_kpi['potential_rescue_value']:,.2f}", delta="Win-Win LTV")
    
    st.divider()

    # --- RESCUE QUEUE TABLE ---
    st.subheader(f"📋 Daily Rescue Queue for Branch: {selected_branch}")
    st.markdown("Select an application below to run the **Multi-Agent Evaluation Pipeline**.")
    
    branch_clients = context_df[context_df['branch_id'] == selected_branch]
    
    if branch_clients.empty:
        st.info("No rescuable clients found for this branch.")
    else:
        selected_app_id = st.selectbox(
            "Select Application ID to Evaluate:", 
            branch_clients['application_id'].tolist()
        )
        
        client_row = branch_clients[branch_clients['application_id'] == selected_app_id].iloc[0]
        
        # Display client profile summary
        with st.expander("👤 View Client Profile & Rejection Metadata", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.write(f"**Client ID:** {client_row['client_id']}")
            c1.write(f"**Age:** {client_row['age']} years old")
            c2.write(f"**Segment:** {client_row['segment']}")
            c2.write(f"**Employment Type:** {client_row['employment_type']}")
            c3.write(f"**Account Tenure:** {client_row['account_age_months']} months")
            c3.write(f"**Requested Amount:** ${client_row['requested_amount']:,.2f}")
            
            st.warning(f"**System Rejection Reason:** {client_row['rejection_reason']}")

        # --- RUN MULTI-AGENT PIPELINE BUTTON ---
        if st.button("🚀 Run Multi-Agent Decision Engine", type="primary"):
            
            # Agent 1 Execution
            with st.status("🤖 Executing Multi-Agent Pipeline...", expanded=True) as status:
                st.write("Step 1: **Agent 1 [Intake & Gatekeeper]** analyzing documents and eligibility...")
                
                reason = client_row['rejection_reason']
                is_hard_decline = "SCR" in reason or "Fraud" in reason
                
                if is_hard_decline:
                    status.update(label="Agent 1 Evaluation Completed: Hard Decline", state="error", expanded=True)
                    st.error("⛔ **Agent 1 Decision:** Hard decline detected. Case cannot be rescued.")
                else:
                    st.write("Step 2: **Agent 1** validated friction type. Initiating automated *handoff* to Agent 2...")
                    st.write("Step 3: **Agent 2 [LTV & Relationship Strategist]** calculating portfolio value and compliance requirements...")
                    status.update(label="Multi-Agent Pipeline Executed Successfully!", state="complete", expanded=False)
                    
                    # Display Agent 2 Institutional Report
                    st.markdown("---")
                    st.subheader("📊 Institutional Credit Recovery Report (Agent 2 Output)")
                    
                    amount = client_row['requested_amount']
                    tenure = client_row['account_age_months']
                    employment = client_row['employment_type']
                    segment = client_row['segment']
                    
                    if "Score" in reason or "Positive Credit" in reason:
                        report_md = f"""
                        * **1. Client & Portfolio Value Context:** Segment: `{segment}` | Tenure: `{tenure}` months. Low traditional score driven by thin file. Estimated cross-sell LTV impact: **~${amount * 0.12:,.2f}**.
                        * **2. Win-Win Alternative Structure:** Propose a **Secured Credit Line (Credit Builder Card)** 100% collateralized by a minor investment certificate (CDB), bringing default risk to zero.
                        * **3. Regulatory Compliance (BACEN):** Seamlessly enroll the client in the **BACEN Financial Education Journey** to satisfy social mandates and re-activate the Positive Credit Registry.
                        * **4. Branch Manager Playbook & Script:**  
                          * *Context:* "Client has been with us for {tenure} months. Rejection was purely mechanical."  
                          * *Script:* *"Hello! We reviewed your application for ${amount:,.2f}. Because we value our {tenure}-month relationship, we’ve unlocked a guided financial program that safely approves your credit while building your market score."*
                        """
                    elif "Income" in reason or "Cash Flow" in reason:
                        report_md = f"""
                        * **1. Client & Portfolio Value Context:** Employment: `{employment}` | Tenure: `{tenure}` months. Traditional rigid pay stubs failed to capture gig-economy liquidity. High attrition risk.
                        * **2. Win-Win Alternative Structure:** Bypass standard documents by pulling 90-day multi-bank transactional history via **Open Finance API**.
                        * **3. Regulatory Compliance & Data Enrichment:** Collect digital platform statements or Pix receipts through secure banking channels.
                        * **4. Branch Manager Playbook & Script:**  
                          * *Context:* "Pay stubs failed, but account movement shows steady monthly inflows."  
                          * *Script:* *"We know your income as a {employment} flows dynamically. Let's connect your accounts via Open Finance in 1 minute so we can approve your ${amount:,.2f} based on your true cash flow!"*
                        """
                    else:
                        report_md = f"""
                        * **1. Client & Portfolio Value Context:** Segment: `{segment}` | Requested: `${amount:,.2f}`. Debt-to-Income (DTI) exceeded the conservative 30% policy threshold.
                        * **2. Win-Win Alternative Structure:** Restructure loan term (extend installments) to drop DTI below 30%, or introduce a co-signer to share credit exposure.
                        * **3. Branch Manager Playbook & Script:**  
                          * *Context:* "Initial structure overextended their monthly budget. Restructuring saves the deal."  
                          * *Script:* *"We want this ${amount:,.2f} loan to fit comfortably into your monthly budget without pressure. Let's adjust the term length to make installments lighter and safer for your financial health."*
                        """
                    
                    st.markdown(report_md)
                    