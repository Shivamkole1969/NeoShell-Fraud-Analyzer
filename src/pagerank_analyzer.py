import pandas as pd
import networkx as nx

def calculate_pagerank_spikes():
    print("Loading time-series ownership records...")
    df = pd.read_csv('data/ownership_timeseries.csv')
    df['start_date'] = pd.to_datetime(df['start_date'])
    
    # 1. Split Data into Time Windows (Q3 vs Q4 for simplicity)
    q3_mask = (df['start_date'] < '2023-10-01')
    
    df_q3 = df[q3_mask]
    df_q4 = df  # Q4 view includes all current status (Historical + New)
    
    # 2. Build Q3 Graph (Person -> Company)
    G_q3 = nx.DiGraph()
    for _, row in df_q3.iterrows():
        G_q3.add_edge(row['person_id'], row['company_id'])
        
    # 3. Build Q4 Graph
    G_q4 = nx.DiGraph()
    for _, row in df_q4.iterrows():
        G_q4.add_edge(row['person_id'], row['company_id'])
        
    # 4. Calculate Pagerank for both
    print("Running PageRank algorithms...")
    pr_q3 = nx.pagerank(G_q3)
    pr_q4 = nx.pagerank(G_q4)
    
    # 5. Detect Spikes (Centrality Delta)
    results = []
    # Only check "Person" nodes for fraud spikes
    all_people = [n for n in G_q4.nodes if n.startswith('PERS_')]
    
    for person in all_people:
        score_q3 = pr_q3.get(person, 0.0) # Might not even exist in Q3 graph if new
        score_q4 = pr_q4.get(person, 0.0)
        
        # Avoid division by zero
        change_pct = ((score_q4 - score_q3) / score_q3 * 100) if score_q3 > 0 else float('inf')
        
        results.append({
            'person_id': person,
            'pagerank_q3': score_q3,
            'pagerank_q4': score_q4,
            'spike_pct': change_pct
        })
        
    df_results = pd.DataFrame(results).sort_values(by='spike_pct', ascending=False)
    
    print("\n--- TOP FRAUD ALERTS (PageRank Spike) ---")
    print(df_results.head(10).to_string(index=False))
    
    # 6. Summary for Resume
    top_fraudster = df_results.iloc[0]['person_id']
    print(f"\nALERT: Person {top_fraudster} identified as HIGH RISK for shell-company orchestration.")
    print("This person's network centrality exploded in Q4.")

if __name__ == "__main__":
    calculate_pagerank_spikes()
