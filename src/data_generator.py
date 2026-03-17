import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_shell_network(num_companies=500, num_people=200):
    print(f"Generating synthetic shell company network with {num_companies} companies and {num_people} people...")
    
    # 1. Create Base Entities
    companies = pd.DataFrame({
        'company_id': [f"COMP_{i:04d}" for i in range(num_companies)],
        'name': [f"Shell Co {i:04d} Ltd" for i in range(num_companies)],
        'incorporation_date': [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(num_companies)]
    })
    
    people = pd.DataFrame({
        'person_id': [f"PERS_{i:04d}" for i in range(num_people)],
        'name': [f"Individual {i:04d}" for i in range(num_people)]
    })
    
    # 2. Time-Series Ownership (Months 1-12)
    ownership_records = []
    
    # Normal network (Decentralized)
    for i in range(num_companies):
        owner = random.choice(people['person_id'])
        start_date = companies.iloc[i]['incorporation_date']
        ownership_records.append({
            'company_id': companies.iloc[i]['company_id'],
            'person_id': owner,
            'start_date': start_date,
            'end_date': None, # Current owner
            'share_pct': random.uniform(50, 100)
        })
        
    # 3. THE FRAUD EVENT (Spike in centrality)
    # Let's pick ONE person (the "Hidden Owner") who starts consolidating power in Q4 (Months 10-12)
    fraudster_id = people.iloc[0]['person_id'] # PERS_0000
    print(f"Injecting fraud event for {fraudster_id} in Q4...")
    
    q4_start = datetime(2023, 10, 1)
    
    # Fraudster suddenly takes over 20% of the companies in October/November
    sampled_companies = companies.sample(int(num_companies * 0.20))
    for i, row in sampled_companies.iterrows():
        # Update current records - end previous owner's term
        # (In a real DB, you'd find the existing record, but for mock CSV we just add new ones)
        ownership_records.append({
            'company_id': row['company_id'],
            'person_id': fraudster_id,
            'start_date': q4_start + timedelta(days=random.randint(0, 30)),
            'end_date': None,
            'share_pct': 100 # Total control
        })
        
    df_ownership = pd.DataFrame(ownership_records)
    
    # Save datasets
    os.makedirs('data', exist_ok=True)
    companies.to_csv('data/companies.csv', index=False)
    people.to_csv('data/people.csv', index=False)
    df_ownership.to_csv('data/ownership_timeseries.csv', index=False)
    
    print("Datasets saved to data/ directory.")
    return df_ownership

if __name__ == "__main__":
    generate_shell_network()
