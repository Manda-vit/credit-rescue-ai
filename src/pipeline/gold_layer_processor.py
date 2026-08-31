import pandas as pd
from pathlib import Path
import logging

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

INPUT_DIR = Path('data/silver')
OUTPUT_DIR = Path('data/gold')

# Ensure output directory exists (THIS LINE FIXES THE ERROR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_silver_data() -> pd.DataFrame:
    """Loads the enriched data from the Silver layer."""
    logging.info("Loading enriched data from Silver layer...")
    return pd.read_csv(INPUT_DIR / 'silver_applications_enriched.csv')

def create_manager_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates data to create KPIs for the Branch Manager Dashboard."""
    logging.info("Generating Branch Manager KPIs...")
    
    # Filter only denied applications to calculate lost value
    denied_df = df[df['status'] == 'Denied']
    
    kpis = denied_df.groupby('branch_id').agg(
        total_denied_applications=('application_id', 'count'),
        total_lost_value=('lost_value', 'sum'),
        rescuable_applications=('is_rescuable', 'sum')
    ).reset_index()
    
    # Calculate how much money can potentially be rescued per branch
    rescuable_df = denied_df[denied_df['is_rescuable'] == True]
    rescuable_value = rescuable_df.groupby('branch_id')['lost_value'].sum().reset_index(name='potential_rescue_value')
    
    kpis = kpis.merge(rescuable_value, on='branch_id', how='left').fillna(0)
    
    return kpis

def create_ai_context_view(df: pd.DataFrame) -> pd.DataFrame:
    """Filters and formats the data for the AI Agent consumption (Rescuable clients only)."""
    logging.info("Generating AI Context View for rescuable clients...")
    
    rescuable_df = df[(df['status'] == 'Denied') & (df['is_rescuable'] == True)].copy()
    
    ai_context_cols = [
        'application_id', 'client_id', 'branch_id', 'age', 'segment', 
        'employment_type', 'account_age_months', 'requested_amount', 
        'status', 'rejection_reason', 'recommended_action'  # <-- Adicionado 'status' aqui
    ]
    
    return rescuable_df[ai_context_cols]

def save_gold_data(kpis_df: pd.DataFrame, ai_context_df: pd.DataFrame):
    """Saves the Gold layer data marts."""
    kpis_path = OUTPUT_DIR / 'mart_branch_manager_kpis.csv'
    ai_context_path = OUTPUT_DIR / 'mart_ai_client_context.csv'
    
    kpis_df.to_csv(kpis_path, index=False)
    ai_context_df.to_csv(ai_context_path, index=False)
    
    logging.info(f"Gold data successfully saved to {OUTPUT_DIR}")

def main():
    """Orchestrates the Gold Layer processing pipeline."""
    silver_df = load_silver_data()
    
    kpis_df = create_manager_kpis(silver_df)
    ai_context_df = create_ai_context_view(silver_df)
    
    save_gold_data(kpis_df, ai_context_df)
    
    logging.info("Gold layer processing completed!")

if __name__ == "__main__":
    main()