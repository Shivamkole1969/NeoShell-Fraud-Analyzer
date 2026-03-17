# NeoShell: Corporate Shell Company & PE Fraud Analyzer (Time-Series GraphRAG)

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Data_Science-lightgrey)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-yellow)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-green)

**NeoShell** is a massive-scale, time-series graph analytics and Agentic RAG platform designed to uncover hidden beneficial owners and detect corporate shell-company fraud.

By correlating millions of public company records (OpenCorporates) with unstructured financial filings (SEC EDGAR PDFs), this system dynamically builds an evolving knowledge graph. It uses **Temporal PageRank** and **Graph Neural Networks (GNNs)** to identify highly central, high-risk entities manipulating complex corporate webs.

---

## 🏗️ System Architecture

1.  **Data Ingestion (Time-Series ETL)**
    *   **Structured:** Ingests daily OpenCorporates snapshots (Directors, Registered Addresses, Shareholders).
    *   **Unstructured (Agentic RAG):** LangChain/LlamaIndex agents monitor SEC filings (10-K, 13F). They use PyMuPDF and Anthropic Claude to extract newly disclosed relationships and subsidiaries over time.
2.  **Graph Construction (Neo4j & Temporal Data)**
    *   Nodes: `Company`, `Person`, `Address`, `Filing`.
    *   Edges: `OWNS`, `DIRECTOR_OF`, `REGISTERED_AT`.
    *   *Time-Series Aspect:* Every edge has `valid_from` and `valid_until` timestamps.
3.  **Graph Analytics: Temporal PageRank**
    *   We run PageRank dynamically across time-windows (e.g., Q1 vs Q2).
    *   Sudden spikes in a hidden node's PageRank (a "nobody" suddenly becoming central to 50 new shell companies in 3 months) trigger a fraud alert.
4.  **Hugging Face Dashboard**
    *   A Streamlit interface where investigators can search a Person/Company, view their temporal graph evolution, and chat with the SEC filings supporting the connections.

---

## 🛠️ Tech Stack (Aligned with Industry Standards)
*   **Graph DB:** Neo4j (Cypher, Graph Data Science Library)
*   **LLM / Agents:** Anthropic Claude (via API), LangChain, LangGraph
*   **Vector DB:** Pinecone / FAISS (for SEC document matching)
*   **Machine Learning:** PyTorch Geometric (Temporal GNNs), XGBoost (Classification)
*   **MLOps & CI/CD:** GitHub Actions (Automated testing/linting), Docker
*   **UI:** Streamlit hosted on Hugging Face Spaces

---

## 🔄 CI/CD Pipeline
This project utilizes GitHub Actions for continuous integration.
*   **Trigger:** On push to `main` or Pull Requests.
*   **Jobs:**
    *   `lint`: Ruff and Black formatting checks.
    *   `test`: Pytest executing unit tests on knowledge graph construction logic.
    *   `deploy`: (Optional/Manual) Syncs to Hugging Face Spaces.

---

## 🧠 Interview Preparation Guide

When discussing this project in an AI/Data Science interview, focus on these key talking points:

### 1. "Why use PageRank for Fraud Detection?"
**Your Answer:** "Traditional ML struggles with tabular representations of complex networks. PageRank calculates the *influence* or *centrality* of a node. In money laundering or PE fraud, illicit actors try to hide behind layers of shell companies. By running PageRank on an ownership graph, the algorithm mathematical trace the paths back to the true 'beneficial owner', revealing hidden control that simple SQL queries would miss."

### 2. "How did you incorporate Time-Series data?"
**Your Answer:** "Static graphs miss the 'bust-out' behavior. I modeled the Neo4j graph with temporal edges (start/end dates). I then tracked the *Derivative* of the PageRank score over time. If a node's centrality spikes by 400% within a 30-day window, it signals rapid shell-company generation—a classic red flag for impending fraud or tax evasion."

### 3. "How does the Agentic RAG component work?"
**Your Answer:** "Not all ownership data is cleanly structured in databases. Significant disclosures are hidden in the unstructured text of SEC PDFs. I built a LangGraph agent that ingests these PDFs using PyMuPDF, chunks them, and uses an LLM to perform Named Entity Recognition (NER) and Relation Extraction (RE). The agent formats these extractions as Cypher queries and injects them directly into the Neo4j graph, augmenting the tabular OpenCorporates data."

### 4. "How do you handle Massive Datasets (Millions of nodes)?"
**Your Answer:** "I utilized Neo4j's Graph Data Science (GDS) library, which allows for in-memory graph projection. Instead of running PageRank via iterative Python loops, I projected the relevant subgraphs into RAM and executed Neo4j's optimized C++ algorithms, taking execution time from hours down to seconds."
