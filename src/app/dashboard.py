import streamlit as st
import pandas as pd
import time
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Credit Recovery Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED INSTITUTIONAL CSS & UI COMPONENTS ---
st.markdown("""
    <style>
        /* Global Background */
        .stApp { background-color: #f1f5f9; }
        .block-container { padding-top: 1.5rem !important; }
        
        /* Corporate Header */
        .corporate-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: white;
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 32px;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .corporate-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px; }
        .corporate-header p { color: #94a3b8; margin: 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; margin-top: 4px; }
        
        /* Metric Cards */
        div[data-testid="metric-container"] {
            background: linear-gradient(145deg, #ffffff, #f8fafc);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            border-left: 5px solid #1e3a8a;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }
        div[data-testid="metric-container"] label { color: #64748b; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #0f172a; font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; }

        /* CRM Tags/Badges */
        .crm-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px; /* Pill shape */
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-blue { background-color: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
        .badge-gray { background-color: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
        .badge-red { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        
        /* Structural Containers */
        div[data-testid="stSelectbox"] { background-color: #ffffff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); border: 1px solid #cbd5e1; margin-bottom: 24px; }
        div[data-testid="stExpander"] { background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); border: 1px solid #cbd5e1; }
        div[data-testid="stExpander"] summary { background-color: #f8fafc; padding: 16px 24px; font-weight: 700; color: #334155; border-bottom: 1px solid #e2e8f0; }
        
        /* Reports */
        .report-container { background-color: #ffffff; padding: 35px; border: 1px solid #cbd5e1; border-top: 6px solid #1e3a8a; border-radius: 12px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05); margin-top: 30px; }
        .fast-update-container { background-color: #ffffff; padding: 35px; border: 1px solid #cbd5e1; border-top: 6px solid #d97706; border-radius: 12px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05); margin-top: 30px; }
        
        /* Button CTA */
        div[data-testid="stButton"] button { background-color: #1e3a8a !important; color: white !important; font-weight: 600 !important; padding: 24px !important; border-radius: 10px !important; border: none !important; box-shadow: 0 4px 6px rgba(30, 58, 138, 0.3) !important; transition: all 0.2s ease !important; width: 100%; font-size: 1.05rem !important;}
        div[data-testid="stButton"] button:hover { background-color: #152c6b !important; box-shadow: 0 8px 15px rgba(30, 58, 138, 0.4) !important; transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

# --- PATHS & DATA LOADING ---
GOLD_KPI_PATH = Path('data/gold/mart_branch_manager_kpis.csv')
GOLD_CONTEXT_PATH = Path('data/gold/mart_ai_client_context.csv')

@st.cache_data
def load_data():
    if not GOLD_KPI_PATH.exists() or not GOLD_CONTEXT_PATH.exists(): return None, None
    return pd.read_csv(GOLD_KPI_PATH), pd.read_csv(GOLD_CONTEXT_PATH)

kpis_df, context_df = load_data()

# --- SIDEBAR ---
st.sidebar.markdown("### Workstation Settings")
st.sidebar.markdown("---")
selected_branch = st.sidebar.selectbox("Active Branch Environment", kpis_df['branch_id'].unique()) if kpis_df is not None else None
branch_kpi = kpis_df[kpis_df['branch_id'] == selected_branch].iloc[0] if selected_branch else None
st.sidebar.markdown("---")
st.sidebar.caption("🟢 System Status: Online\n🔗 Connected to Unity Catalog")

# --- HEADER ---
st.markdown("""
    <div class="corporate-header">
        <div>
            <h1>Credit Rescue Intelligence</h1>
            <p>Underwriting & Portfolio Recovery Platform</p>
        </div>
        <div style="text-align: right;">
            <p style="color: #cbd5e1; font-size: 0.75rem; letter-spacing: 2px;">SECURE SESSION</p>
            <p style="color: white; font-weight: 700; font-size: 0.9rem;">USER: BRANCH MANAGER</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if kpis_df is None or context_df is None:
    st.error("System Error: Gold layer databases not found. Please execute the data pipelines.")
    st.stop()

# --- METRICS & DATA VIZ ROW ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Denied Applications", f"{int(branch_kpi['total_denied_applications'])}")
col2.metric("Capital at Risk", f"$ {branch_kpi['total_lost_value']:,.2f}")
col3.metric("Actionable Leads", f"{int(branch_kpi['rescuable_applications'])}")
col4.metric("Recoverable Capital", f"$ {branch_kpi['potential_rescue_value']:,.2f}")

# Progress Bar Visualization (Recovery Yield)
recovery_yield = (branch_kpi['potential_rescue_value'] / branch_kpi['total_lost_value']) * 100 if branch_kpi['total_lost_value'] > 0 else 0
st.markdown(f"<p style='color: #64748b; font-size: 0.85rem; font-weight: 600; margin-top: 15px; margin-bottom: 5px; text-transform: uppercase;'>Branch Recovery Yield Potential: {recovery_yield:.1f}%</p>", unsafe_allow_html=True)
st.progress(int(recovery_yield))
st.markdown("<br>", unsafe_allow_html=True)

# --- QUEUE SECTION ---
st.markdown(f"<h3 style='color: #0f172a; font-size: 1.5rem; margin-bottom: 20px;'>Operational Queue - {selected_branch}</h3>", unsafe_allow_html=True)
branch_clients = context_df[context_df['branch_id'] == selected_branch]

if branch_clients.empty:
    st.info("System Notice: No eligible clients for recovery in this branch at this time.")
else:
    branch_clients['dropdown_label'] = branch_clients['application_id'] + " | " + branch_clients['rejection_reason']
    selected_label = st.selectbox("Target Application ID:", branch_clients['dropdown_label'].tolist())
    
    selected_app_id = selected_label.split(" | ")[0]
    client_row = branch_clients[branch_clients['application_id'] == selected_app_id].iloc[0]
    
    # CRM Styled Profile Details
    with st.expander("Underwriting Metadata & Compliance Flag", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Client ID:** `{client_row['client_id']}`")
        c1.markdown(f"**Age:** {client_row['age']} years")
        
        # Applying CRM Badges
        c2.markdown(f"**Segment:** <span class='crm-badge badge-blue'>{client_row['segment']}</span>", unsafe_allow_html=True)
        c2.markdown(f"**Employment:** <span class='crm-badge badge-gray'>{client_row['employment_type']}</span>", unsafe_allow_html=True)
        
        c3.markdown(f"**Relationship Tenure:** {client_row['account_age_months']} months")
        c3.markdown(f"**Requested Principal:** **$ {client_row['requested_amount']:,.2f}**")
        
        st.markdown(f"**Automated Decision Flag:** <span class='crm-badge badge-red'>{client_row['rejection_reason']}</span>", unsafe_allow_html=True)

    # --- ACTION BUTTON ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Initialize Multi-Agent Workflow", type="primary", use_container_width=True):
        
        with st.status("Establishing connection to Agent Engine...", expanded=True) as status:
            # Simulated Latency for better UX feedback
            time.sleep(1) 
            st.write("Process 1: Gatekeeper Agent pulling Unity Catalog schemas...")
            time.sleep(1.5)
            st.write("Process 1: Validating KYC parameters and regulatory flags...")
            
            reason = client_row['rejection_reason']
            
            if "SCR" in reason or "Fraud" in reason:
                time.sleep(1)
                status.update(label="Protocol Terminated: Policy Violation", state="error", expanded=True)
                st.error("Final Decision: Severe restriction identified (SCR or Fraud). Capital release blocked.")
            
            elif "Document" in reason or "Registry" in reason:
                time.sleep(1)
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

            else:
                st.write("Process 2: Operational friction validated. Engaging LTV Strategy Agent...")
                time.sleep(2) # Simulating LLM generation time
                st.write("Process 3: Synthesizing structural alternatives based on behavioral data...")
                status.update(label="Workflow Executed: Strategy Ready", state="complete", expanded=False)
                
                amount = client_row['requested_amount']
                tenure = client_row['account_age_months']
                employment = client_row['employment_type']
                segment = client_row['segment']
                
                if "Score" in reason or "Positive Credit" in reason:
                    strategy_title = "Structural Alternative: Thin File Segment"
                    strategy_content = f"""<ul style="color: #334155; line-height: 1.7;"><li><b>Portfolio Context:</b> Segment `{segment}` with {tenure} months history. Projected cross-sell LTV: <b>$ {amount * 0.12:,.2f}</b>.</li><li><b>Credit Architecture:</b> Authorize a secured credit facility (collateralized via CDB investment) to neutralize default probability.</li><li><b>Regulatory Alignment:</b> Register client in the Central Bank Financial Education Journey to restore Positive Credit standing.</li><li><b>Client Communication Script:</b><br><i>"We reviewed your application for $ {amount:,.2f}. Because we value your {tenure}-month history with us, we have structured an oriented credit line that releases your funds while building your market score."</i></li></ul>"""
                elif "Income" in reason or "Cash Flow" in reason:
                    strategy_title = "Structural Alternative: Dynamic Cash Flow"
                    strategy_content = f"""<ul style="color: #334155; line-height: 1.7;"><li><b>Portfolio Context:</b> Occupation `{employment}`. High attrition probability due to rigid payroll requirements.</li><li><b>Credit Architecture:</b> Override formal payroll checks. Execute liquidity analysis via Open Finance API (90-day ledger).</li><li><b>Client Communication Script:</b><br><i>"We recognize your income structure as `{employment}` is dynamic. By integrating your data via Open Finance, we can securely authorize your $ {amount:,.2f} request based on actual cash flow."</i></li></ul>"""
                else:
                    strategy_title = "Structural Alternative: DTI Restructuring"
                    strategy_content = f"""<ul style="color: #334155; line-height: 1.7;"><li><b>Portfolio Context:</b> Segment `{segment}`. Debt-to-income (DTI) ratio breached the internal 30% prudential limit.</li><li><b>Credit Architecture:</b> Recalculate amortization schedule. Extend term length to dilute monthly obligations, or mandate a co-signer execution.</li><li><b>Client Communication Script:</b><br><i>"To ensure this $ {amount:,.2f} facility aligns with your financial planning, we have adjusted the amortization term. This ensures the installments fit perfectly within your monthly operating budget."</i></li></ul>"""
                
                st.markdown(f"""
                    <div class="report-container">
                        <h4 style="margin-top:0; color:#1e3a8a; font-size: 1.3rem;">Institutional Strategy Report</h4>
                        <p style="color: #475569; font-weight: 600;">Directive: {strategy_title}</p>
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
                        {strategy_content}
                    </div>
                """, unsafe_allow_html=True)