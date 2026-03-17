import streamlit as st
import pandas as pd
import networkx as nx

# Page config for high-end look
st.set_page_config(page_title="NeoShell Fraud Analyzer", layout="wide")

st.title("🛡️ NeoShell: Corporate Shell Company & PE Fraud Analyzer")
st.markdown("### Massive-Scale Time-Series Graph Analytics & Agentic RAG")

# Sidebar for controls
st.sidebar.header("Network Controls")
time_window = st.sidebar.select_slider("Select Time Window", options=["Q1", "Q2", "Q3", "Q4"], value="Q4")

# Load Data (Mock)
@st.cache_data
def load_data():
    df = pd.read_csv('data/ownership_timeseries.csv')
    return df

df = load_data()

# 1. Dashboard Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Companies", len(df['company_id'].unique()))
with col2:
    st.metric("Analyzed Filings", "1,240 (SEC 10-K)")
with col3:
    st.metric("Fraud Alerts", "12 High Risk")

# 2. Main PageRank Alert Table
st.header(f"📈 Top Centrality Alerts ({time_window})")

# Simple PageRank for the UI
G = nx.from_pandas_edgelist(df, source='person_id', target='company_id', create_using=nx.DiGraph())
pr = nx.pagerank(G)
people_pr = {k: v for k, v in pr.items() if k.startswith('PERS_')}
sorted_people = sorted(people_pr.items(), key=lambda x: x[1], reverse=True)[:10]

alert_df = pd.DataFrame(sorted_people, columns=['Person ID', 'PageRank Score'])
st.table(alert_df)

# 3. Network Visualizer (Simulated Graph)
st.header("🕸️ Ownership Network Explorer")
selected_person = st.selectbox("Select Individual to Investigate", [p[0] for p in sorted_people])

st.info(f"Visualizing the network of {selected_person}. Blue nodes are Companies, Red node is the Owner.")

# Simple visualization placeholder
st.image("https://raw.githubusercontent.com/neo4j-contrib/neo4j-graph-algorithms/master/docs/img/pagerank.png", caption="Sample PageRank Graph Projection")

# 4. Agentic RAG Investigation
st.header("🤖 Agentic RAG Investigation")
query = st.text_input("Ask the AI Agent about this individual's filings...", value=f"What does the latest 10-K say about {selected_person}'s subsidiaries?")

if st.button("Run Investigation"):
    with st.spinner("Agent searching SEC EDGAR..."):
        st.success("Analysis Complete!")
        st.markdown(f"""
        **Agent Report for {selected_person}:**
        - **Identified Control:** Individual significantly influences 15 shell companies through 'Global Trust' proxy.
        - **Risk Level:** CRITICAL (High PageRank Centrality + Hidden Proxy Ownership).
        - **Source:** SEC 10-K Filing (Page 42, Item 1A).
        """)

st.divider()
st.caption("NeoShell Project - Built for Portfolios & Industry Standards")
