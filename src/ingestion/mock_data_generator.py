import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configurações para reprodutibilidade e volume
np.random.seed(42)
random.seed(42)
NUM_CLIENTS = 5000
NUM_APPLICATIONS = 8000
NUM_BRANCHES = 50

print("Buidling massive mock dataset...")

# 1. Gerar raw_branch_data
branches = pd.DataFrame({
    'branch_id': [f'BR_{str(i).zfill(3)}' for i in range(1, NUM_BRANCHES + 1)],
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], NUM_BRANCHES),
    'manager_id': [f'MGR_{np.random.randint(100, 999)}' for _ in range(NUM_BRANCHES)]
})
branches.to_csv('data/raw/raw_branch_data.csv', index=False)

# 2. Gerar raw_client_demographics
employment_types = ['Salaried', 'Gig-worker', 'Self-employed', 'Unemployed', 'Business Owner']
segments = ['Mass', 'Mass-Affluent', 'Premium', 'Private']

clients = pd.DataFrame({
    'client_id': [f'CLI_{str(i).zfill(5)}' for i in range(1, NUM_CLIENTS + 1)],
    'age': np.random.randint(18, 75, NUM_CLIENTS),
    'account_age_months': np.random.randint(1, 120, NUM_CLIENTS),
    'employment_type': np.random.choice(employment_types, NUM_CLIENTS, p=[0.4, 0.25, 0.2, 0.1, 0.05]),
    'segment': np.random.choice(segments, NUM_CLIENTS, p=[0.6, 0.25, 0.1, 0.05])
})
clients.to_csv('data/raw/raw_client_demographics.csv', index=False)

# 3. Gerar raw_credit_applications
statuses = ['Approved', 'Denied']
rejection_reasons = ['None', 'Low Score', 'Thin File', 'Fraud Suspicion', 'Active Default', 'High DTI']

# Regras de negócio simuladas para dar realismo aos dados
def determine_status_and_reason(employment):
    if np.random.rand() > 0.6:  # 40% de aprovação global
        return 'Approved', 'None'
    else:
        # Ponderação de erro baseada no tipo de emprego
        if employment in ['Gig-worker', 'Self-employed']:
            reason = np.random.choice(['Low Score', 'Thin File', 'High DTI', 'Fraud Suspicion'], p=[0.4, 0.4, 0.15, 0.05])
        else:
            reason = np.random.choice(rejection_reasons[1:], p=[0.3, 0.1, 0.1, 0.3, 0.2])
        return 'Denied', reason

applications = []
for i in range(1, NUM_APPLICATIONS + 1):
    client_id = f'CLI_{str(np.random.randint(1, NUM_CLIENTS + 1)).zfill(5)}'
    client_emp = clients.loc[clients['client_id'] == client_id, 'employment_type'].values[0]
    
    status, reason = determine_status_and_reason(client_emp)
    
    # Data de aplicação aleatória nos últimos 6 meses
    days_ago = np.random.randint(0, 180)
    app_date = datetime.now() - timedelta(days=days_ago)
    
    applications.append({
        'application_id': f'APP_{str(i).zfill(6)}',
        'client_id': client_id,
        'branch_id': np.random.choice(branches['branch_id']),
        'requested_amount': round(np.random.uniform(1000, 50000), 2),
        'status': status,
        'rejection_reason': reason,
        'application_date': app_date.strftime('%Y-%m-%d')
    })

apps_df = pd.DataFrame(applications)
apps_df.to_csv('data/raw/raw_credit_applications.csv', index=False)

print("Mock data generated successfully in 'data/raw'!")