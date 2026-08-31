import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

# --- GLOBAL CONFIGURATIONS ---
np.random.seed(42)
random.seed(42)

NUM_CLIENTS = 5000
NUM_APPLICATIONS = 8000
NUM_BRANCHES = 50
OUTPUT_DIR = Path('data/raw')

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_branches(num_branches: int) -> pd.DataFrame:
    """Generates mock data for bank branches."""
    return pd.DataFrame({
        'branch_id': [f'BR_{str(i).zfill(3)}' for i in range(1, num_branches + 1)],
        'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], num_branches),
        'manager_id': [f'MGR_{np.random.randint(100, 999)}' for _ in range(num_branches)]
    })

def generate_clients(num_clients: int) -> pd.DataFrame:
    """Generates mock demographic data for clients."""
    employment_types = ['Salaried', 'Gig-worker', 'Self-employed', 'Unemployed', 'Business Owner']
    segments = ['Mass', 'Mass-Affluent', 'Premium', 'Private']

    return pd.DataFrame({
        'client_id': [f'CLI_{str(i).zfill(5)}' for i in range(1, num_clients + 1)],
        'age': np.random.randint(18, 75, num_clients),
        'account_age_months': np.random.randint(1, 120, num_clients),
        'employment_type': np.random.choice(employment_types, num_clients, p=[0.4, 0.25, 0.2, 0.1, 0.05]),
        'segment': np.random.choice(segments, num_clients, p=[0.6, 0.25, 0.1, 0.05])
    })

def determine_status_and_reason(employment: str) -> pd.Series:
    """Applies business rules for credit approval based on employment profile."""
    if np.random.rand() > 0.45:  # 55% global approval rate
        return pd.Series(['Approved', 'None'])
    
    if employment in ['Gig-worker', 'Self-employed']:
        reason = np.random.choice([
            'Income - Gig Worker with Inconsistent Cash Flow',
            'Income - Missing Tax Return',
            'Score - Disabled Positive Credit Registry',
            'Policy - Debt-to-Income (DTI) > 30%'
        ], p=[0.4, 0.2, 0.2, 0.2])
    else:
        reason = np.random.choice([
            'Registry Error - Data Mismatch with Tax Authority',
            'Document Error - Expired or Illegible ID',
            'Score - Forgotten Micro-Debt',
            'Restriction - Historical Default on Central Bank SCR',
            'Policy - Debt-to-Income (DTI) > 30%'
        ], p=[0.2, 0.2, 0.2, 0.1, 0.3])
        
    return pd.Series(['Denied', reason])

def generate_applications(num_applications: int, clients_df: pd.DataFrame, branches_df: pd.DataFrame) -> pd.DataFrame:
    """Generates the credit application history based on existing clients and branches."""
    
    # Sample random clients to create applications
    apps_df = clients_df[['client_id', 'employment_type']].sample(n=num_applications, replace=True).reset_index(drop=True)
    
    apps_df['application_id'] = [f'APP_{str(i).zfill(6)}' for i in range(1, num_applications + 1)]
    apps_df['branch_id'] = np.random.choice(branches_df['branch_id'], num_applications)
    apps_df['requested_amount'] = np.round(np.random.uniform(1000, 50000, num_applications), 2)
    
    # Generate random dates in the last 180 days (vectorized approach)
    random_days = np.random.randint(0, 180, num_applications)
    base_date = datetime.now()
    apps_df['application_date'] = [(base_date - timedelta(days=int(d))).strftime('%Y-%m-%d') for d in random_days]

    # Apply approval/rejection rules
    status_reason_df = apps_df['employment_type'].apply(determine_status_and_reason)
    apps_df[['status', 'rejection_reason']] = status_reason_df

    # Clean up and reorder columns
    apps_df = apps_df.drop(columns=['employment_type'])
    return apps_df[['application_id', 'client_id', 'branch_id', 'requested_amount', 'status', 'rejection_reason', 'application_date']]

def main():
    """Main function that orchestrates data generation."""
    print("Building massive mock dataset (Clean Code Architecture)...")
    
    branches = generate_branches(NUM_BRANCHES)
    branches.to_csv(OUTPUT_DIR / 'raw_branch_data.csv', index=False)
    
    clients = generate_clients(NUM_CLIENTS)
    clients.to_csv(OUTPUT_DIR / 'raw_client_demographics.csv', index=False)
    
    applications = generate_applications(NUM_APPLICATIONS, clients, branches)
    applications.to_csv(OUTPUT_DIR / 'raw_credit_applications.csv', index=False)
    
    print(f"Mock data generated successfully in '{OUTPUT_DIR}'!")

if __name__ == "__main__":
    main()