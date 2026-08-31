import pandas as pd
from pathlib import Path
import logging

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

INPUT_DIR = Path('data/raw')
OUTPUT_DIR = Path('data/silver')

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_bronze_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Loads raw data from the Bronze layer."""
    logging.info("Loading raw data from Bronze layer...")
    
    apps_df = pd.read_csv(INPUT_DIR / 'raw_credit_applications.csv')
    clients_df = pd.read_csv(INPUT_DIR / 'raw_client_demographics.csv')
    
    return apps_df, clients_df

def get_rejection_routing_map() -> dict:
    """
    Business Domain Rule: Maps the raw rejection reason to an actionable 
    resolution strategy and determines if it is rescuable.
    """
    return {
        'None': {'action': 'None', 'is_rescuable': False},
        
        # Fast Updates (Cadastral/Documental)
        'Registry Error - Data Mismatch with Tax Authority': {'action': 'Fast Update - ID Verification', 'is_rescuable': True},
        'Document Error - Expired or Illegible ID': {'action': 'Fast Update - Request New ID', 'is_rescuable': True},
        'Document Error - Divergent Marital Status': {'action': 'Fast Update - Marital Status Docs', 'is_rescuable': True},
        
        # Income Proof
        'Income - Gig Worker with Inconsistent Cash Flow': {'action': 'Income Proof - Open Finance Connect', 'is_rescuable': True},
        'Income - Missing Tax Return': {'action': 'Income Proof - Request Tax Return', 'is_rescuable': True},
        
        # Credit Recovery
        'Score - Forgotten Micro-Debt': {'action': 'Credit Recovery - Micro-settlement', 'is_rescuable': True},
        'Score - Disabled Positive Credit Registry': {'action': 'Credit Recovery - BACEN Education Journey', 'is_rescuable': True},
        
        # Restructuring
        'Policy - Debt-to-Income (DTI) > 30%': {'action': 'Restructuring - Add Co-signer or Increase Term', 'is_rescuable': True},
        'Policy - Asset Value Exceeds Program Limit': {'action': 'Restructuring - Change Property/Loan Type', 'is_rescuable': True},
        
        # Hard Declines (Not Rescuable)
        'Restriction - Historical Default on Central Bank SCR': {'action': 'Hard Decline - SCR Restriction', 'is_rescuable': False}
    }

def process_silver_layer(apps_df: pd.DataFrame, clients_df: pd.DataFrame, routing_map: dict) -> pd.DataFrame:
    """Applies business rules to enrich data and calculate Lost Value."""
    logging.info("Applying business rules and joining datasets...")
    
    # 1. Join Applications with Client Demographics
    enriched_df = apps_df.merge(clients_df, on='client_id', how='left')
    
    # 2. Calculate Financial Lost Value
    enriched_df['lost_value'] = enriched_df.apply(
        lambda row: row['requested_amount'] if row['status'] == 'Denied' else 0.0, axis=1
    )
    
    # 3. Apply Rejection Routing Rules (Mapping)
    routing_df = pd.DataFrame.from_dict(routing_map, orient='index')
    
    enriched_df = enriched_df.merge(
        routing_df, 
        left_on='rejection_reason', 
        right_index=True, 
        how='left'
    )
    
    # Clean up column names to keep consistency
    enriched_df.rename(columns={'action': 'recommended_action'}, inplace=True)
    
    return enriched_df

def save_silver_data(df: pd.DataFrame):
    """Saves the processed data to the Silver layer (Processed)."""
    output_path = OUTPUT_DIR / 'silver_applications_enriched.csv'
    df.to_csv(output_path, index=False)
    logging.info(f"Silver data successfully saved to {output_path}")

def main():
    """Orchestrates the Silver Layer processing pipeline."""
    apps_df, clients_df = load_bronze_data()
    
    routing_map = get_rejection_routing_map()
    
    silver_df = process_silver_layer(apps_df, clients_df, routing_map)
    
    save_silver_data(silver_df)
    
    logging.info("Silver layer processing completed!")

if __name__ == "__main__":
    main()