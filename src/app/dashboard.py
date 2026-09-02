import streamlit as st
import pandas as pd
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Credit Recovery Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED INSTITUTIONAL CSS ---
st.markdown("""
    <style>
        /* Global Background - Institutional Soft Gray */
        .stApp {
            background-color: #f1f5f9;
        }
        
        /* Hide default Streamlit top margin to make room for our custom header */
        .block-container {
            padding-top: 1rem !important;
        }
        
        /* Custom Institutional Top Bar */
        .corporate-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .corporate-header h1 {
            color: white;
            margin: 0;
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        .corporate-header p {
            color: #94a3b8;
            margin: 0;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        /* Metric Cards - Premium Gradient & Shadow */
        div[data-testid="metric-container"] {
            background: linear-gradient(145deg, #ffffff, #f8fafc);
            padding: 24px;
            border-radius: 10px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
            border: 1px solid #e2e8f0;
            border-left: 5px solid #1e3a8a; /* Corporate Blue Marker */
            transition: transform 0.2s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px);
        }
        
        /* Metric Labels */
        div[data-testid="metric-container"] label {
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Metric Values */
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #0f172a;
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -1px;
        }

        /* Selectbox Enclosure - Solid Control Panel Look */
        div[data-testid="stSelectbox"] {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 10px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #cbd5e1;
            margin-bottom: 24px;
        }
        
        /* Expander (Client Data) - Clean Tabular Look */
        div[data-testid="stExpander"] {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #cbd5e1;
        }
        
        div[data-testid="stExpander"] summary {
            background-color: #f8fafc;
            padding: 15px 20px;
            font-weight: 700;
            color: #334155;
            border-bottom: 1px solid #e2e8f0;
        }
        
        /* Agent Report Containers - Document Style */
        .report-container {
            background-color: #ffffff;
            padding: 35px;
            border: 1px solid #cbd5e1;
            border-top: 6px solid #1e3a8a;
            border-radius: 8px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
            margin-top: 30px;
        }
        
        .fast-update-container {
            background-color: #ffffff;
            padding: 35px;
            border: 1px solid #cbd5e1;
            border-top: 6px solid #d97706; /* Amber Warning */
            border-radius: 8px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
            margin-top: 30px;
        }
        
        /* Button Styling - Corporate Action */
        div[data-testid="stButton"] button {
            background-color: #1e3a8a !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 20px !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 6px rgba(30, 58, 138, 0.3) !important;
            transition: all 0.2s ease !important;
        }
        
        div[data-testid="stButton"] button:hover {
            background-color: #152c6b !important;
            box-shadow: 0 6px 12px rgba(30, 58, 138, 0.4) !important;
        }
    </style>
""", unsafe_allow_html=True)

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

# --- SIDEBAR - CONTROL PANEL ---
st.sidebar.markdown("### Workstation Settings")
st.sidebar.markdown("---")

if kpis_df is not None and not kpis_df.empty:
    selected_branch = st.sidebar.selectbox("Active Branch Environment", kpis_df['branch_id'].unique())
    branch_kpi = kpis_df[kpis_df['branch_id'] == selected_branch].iloc[0]
else:
    selected_branch = None

st.sidebar.markdown("---")
st.sidebar.caption("System Status: Online | Connected to Unity Catalog")

# --- CUSTOM CORPORATE HEADER ---
st.markdown("""
    <div class="corporate-header">
        <div>
            <h1>Credit Rescue Intelligence</h1>
            <p>Underwriting & Portfolio Recovery Platform</p>
        </div>
        <div style="text-align: right;">
            <p style="color: #cbd5e1; font-size: 0.75rem;">SECURE SESSION</p>
            <p style="color: white; font-weight: 700;">USER: BRANCH MANAGER</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if kpis_df is None or context_df is None:
    st.error("System Error: Gold layer databases not found. Please execute the data pipeline scripts.")
else:
    # --- EXECUTIVE METRICS ROW ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Denied Applications", f"{int(branch_kpi['total_denied_applications'])}")
    col2.metric("Capital at Risk", f"$ {branch_kpi['total_lost_value']:,.2f}")
    col3.metric("Actionable Leads", f"{int(branch_kpi['rescuable_applications'])}")
    col4.metric("Recoverable Capital", f"$ {branch_kpi['potential_rescue_value']:,.2f}")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- QUEUE & AGENT EXECUTION SECTION ---
    st.markdown(f"<h3 style='color: #0f172a; margin-bottom: 20px;'>Operational Queue - {selected_branch}</h3>", unsafe_allow_html=True)
    
    branch_clients = context_df[context_df['branch_id'] == selected_branch]
    
    if branch_clients.empty:
        st.info("System Notice: No eligible clients for recovery in this branch at this time.")
    else:
        branch_clients['dropdown_label'] = branch_clients['application_id'] + " | " + branch_clients['rejection_reason']
        
        selected_label = st.selectbox(
            "Target Application ID:", 
            branch_clients['dropdown_label'].tolist()
        )
        
        selected_app_id = selected_label.split(" | ")[0]
        client_row = branch_clients[branch_clients['application_id'] == selected_app_id].iloc[0]
        
        # Client Profile Details
        with st.expander("Underwriting Metadata & Compliance Flag", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Client ID:** {client_row['client_id']}")
            c1.markdown(f"**Age:** {client_row['age']} years")
            c2.markdown(f"**Segment:** {client_row['segment']}")
            c2.markdown(f"**Employment:** {client_row['employment_type']}")
            c3.markdown(f"**Relationship Tenure:** {client_row['account_age_months']} months")
            c3.markdown(f"**Requested Principal:** $ {client_row['requested_amount']:,.2f}")
            
            st.markdown(f"**Automated Decision Flag:** `{client_row['rejection_reason']}`")

        # --- RUN MULTI-AGENT PIPELINE ---
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Initialize Multi-Agent Workflow", type="primary", use_container_width=True):
            
            with st.status("Executing screening protocol...", expanded=True) as status:
                st.write("Process 1: Gatekeeper Agent validating regulatory parameters...")
                
                reason = client_row['rejection_reason']
                
                # ROUTE 1: HARD DECLINE
                if "SCR" in reason or "Fraud" in reason:
                    status.update(label="Protocol Terminated: Policy Violation", state="error", expanded=True)
                    st.error("Final Decision: Severe restriction identified (SCR or Fraud). Capital release blocked.")
                
                # ROUTE 2: FAST UPDATE (No Agent 2 needed)
                elif "Document" in reason or "Registry" in reason:
                    status.update(label="Protocol Suspended: Administrative Hold", state="complete", expanded=False)
                    st.write("Process 2: Administrative block identified. Bypassing Strategy Agent.")
                    
                    st.markdown(f"""
                        <div class="fast-update-container">
                            <h4 style="margin-top:0; color:#d97706; font-size: 1.2rem;">Tier 1 Resolution Required</h4>
                            <p style="color: #475569; font-weight: 600;">Directive: KYC / Document Correction</p>
                            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 15px 0;">
                            <ul style="color: #334155; line-height: 1.6;">
                                <li><b>Audit Finding:</b> Application halted due to expired documentation or federal registry mismatch.</li>
                                <li><b>Manager Action:</b> Secure updated identification records from the client.</li>
                                <li><b>System Route:</b> Upon portal upload, the Gatekeeper Agent will automatically authorize the <b>$ {client_row['requested_amount']:,.2f}</b> principal.</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)

                # ROUTE 3: STRATEGIC RESCUE (Agent 2 handles financial restructuring)
                else:
                    st.write("Process 2: Friction validated. Engaging LTV Strategy Agent...")
                    st.write("Process 3: Synthesizing structural alternatives...")
                    status.update(label="Workflow Executed: Strategy Ready", state="complete", expanded=False)
                    
                    amount = client_row['requested_amount']
                    tenure = client_row['account_age_months']
                    employment = client_row['employment_type']
                    segment = client_row['segment']
                    
                    if "Score" in reason or "Positive Credit" in reason:
                        strategy_title = "Structural Alternative: Thin File Segment"
                        strategy_content = f"""
                        <ul style="color: #334155; line-height: 1.7;">
                            <li><b>Portfolio Context:</b> Segment `{segment}` with {tenure} months history. Projected cross-sell LTV: <b>$ {amount * 0.12:,.2f}</b>.</li>
                            <li><b>Credit Architecture:</b> Authorize a secured credit facility (collateralized via CDB investment) to neutralize default probability.</li>
                            <li><b>Regulatory Alignment:</b> Register client in the Central Bank Financial Education Journey to restore Positive Credit standing.</li>
                            <li><b>Client Communication Script:</b><br><i>"We reviewed your application for $ {amount:,.2f}. Because we value your {tenure}-month history with us, we have structured an oriented credit line that releases your funds while building your market score."</i></li>
                        </ul>
                        """
                    elif "Income" in reason or "Cash Flow" in reason:
                        strategy_title = "Structural Alternative: Dynamic Cash Flow"
                        strategy_content = f"""
                        <ul style="color: #334155; line-height: 1.7;">
                            <li><b>Portfolio Context:</b> Occupation `{employment}`. High attrition probability due to rigid payroll requirements.</li>
                            <li><b>Credit Architecture:</b> Override formal payroll checks. Execute liquidity analysis via Open Finance API (90-day ledger).</li>
                            <li><b>Client Communication Script:</b><br><i>"We recognize your income structure as `{employment}` is dynamic. By integrating your data via Open Finance, we can securely authorize your $ {amount:,.2f} request based on actual cash flow."</i></li>
                        </ul>
                        """
                    else:
                        strategy_title = "Structural Alternative: DTI Restructuring"
                        strategy_content = f"""
                        <ul style="color: #334155; line-height: 1.7;">
                            <li><b>Portfolio Context:</b> Segment `{segment}`. Debt-to-income (DTI) ratio breached the internal 30% prudential limit.</li>
                            <li><b>Credit Architecture:</b> Recalculate amortization schedule. Extend term length to dilute monthly obligations, or mandate a co-signer execution.</li>
                            <li><b>Client Communication Script:</b><br><i>"To ensure this $ {amount:,.2f} facility aligns with your financial planning, we have adjusted the amortization term. This ensures the installments fit perfectly within your monthly operating budget."</i></li>
                        </ul>
                        """
                    
                    st.markdown(f"""
                        <div class="report-container">
                            <h4 style="margin-top:0; color:#1e3a8a; font-size: 1.3rem;">Institutional Strategy Report</h4>
                            <p style="color: #475569; font-weight: 600;">Directive: {strategy_title}</p>
                            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
                            {strategy_content}
                        </div>
                    """, unsafe_allow_html=True)