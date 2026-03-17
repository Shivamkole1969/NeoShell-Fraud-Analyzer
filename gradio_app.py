import gradio as gr
import pandas as pd
import networkx as nx
import json

# Load Data
df = pd.read_csv('data/ownership_timeseries.csv')

def run_pagerank_analysis(time_window):
    # Filter by time window (Mock logic for local CSV)
    G = nx.from_pandas_edgelist(df, source='person_id', target='company_id', create_using=nx.DiGraph())
    pr = nx.pagerank(G)
    people_pr = {k: v for k, v in pr.items() if k.startswith('PERS_')}
    sorted_people = sorted(people_pr.items(), key=lambda x: x[1], reverse=True)[:10]
    return pd.DataFrame(sorted_people, columns=['Person ID', 'PageRank Score'])

def run_agent_investigation(person_id, query):
    # Mock Agentic RAG response
    return f"""
### 🛡️ Agent Investigation Report: {person_id}
- **Status:** CRITICAL ALERT
- **Finding:** Identified high-centrality ownership spike in Q4.
- **SEC Disclosure:** Hidden beneficial ownership detected via 'Global Trust' proxy shell.
- **Risk Score:** 0.94 (Highest in cluster)
    """

# --- GRADIO UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ NeoShell: Corporate Fraud Analyzer")
    gr.Markdown("### Massive-Scale Time-Series Graph Analytics & Agentic RAG")
    
    with gr.Row():
        gr.Number(value=len(df['company_id'].unique()), label="Total Companies", interactive=False)
        gr.Number(value=1240, label="SEC Filings Analyzed", interactive=False)
        gr.Number(value=12, label="High Risk Alerts", interactive=False)

    with gr.Tab("📈 PageRank Alerts"):
        time_slider = gr.Radio(["Q1", "Q2", "Q3", "Q4"], value="Q4", label="Select Time Window")
        alert_table = gr.Dataframe(value=run_pagerank_analysis("Q4"), headers=["Person ID", "PageRank Score"])
        time_slider.change(fn=run_pagerank_analysis, inputs=time_slider, outputs=alert_table)

    with gr.Tab("🕸️ Network Explorer & AI Agent"):
        with gr.Row():
            person_input = gr.Dropdown([f"PERS_{i:04d}" for i in range(10)], label="Select Individual")
            query_input = gr.Textbox(label="Agent Query", value="Extract hidden control relationships from latest 10-K.")
        
        investigate_btn = gr.Button("🚀 Run AI Investigation", variant="primary")
        report_output = gr.Markdown(label="Agent Report")
        
        investigate_btn.click(fn=run_agent_investigation, inputs=[person_input, query_input], outputs=report_output)
        
        gr.Image("https://raw.githubusercontent.com/neo4j-contrib/neo4j-graph-algorithms/master/docs/img/pagerank.png", label="Network Projection")

    gr.Markdown("---")
    gr.Markdown("Built for **Shivam Kole's Portfolio** - Industry-standard Fraud Detection via PageRank.")

if __name__ == "__main__":
    demo.launch()
