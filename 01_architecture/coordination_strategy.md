# 🔄 Coordination Strategy

## How Agents Communicate

### 🧩 Overview
The system uses a **sequential message-passing architecture**, where each agent performs a specialized function and passes structured data to the next.  
This design ensures **clear boundaries**, **data consistency**, and **ease of debugging** across the agentic workflow.

---

### 🧠 Agent Interaction Flow

1. **Initialization**
   - The `main.py` script orchestrates execution.
   - `SearchAgent` and `AnalysisAgent` are instantiated independently.

2. **Information Retrieval**
   - The `SearchAgent` executes a query (via **Tavily Search**) and returns a structured text or JSON summary.
   - This summary represents the **shared context** between agents.

3. **Data Handoff**
   - The output from `SearchAgent` is passed as an argument to the `AnalysisAgent`:
     ```python
     summary = search_agent.search_trends(query)
     analysis = analysis_agent.analyze_trends(summary)
     ```
   - This ensures a **controlled handoff** — only validated, formatted data is shared downstream.

4. **Independent Processing**
   - `AnalysisAgent` uses **Ollama** to interpret and summarize the input, performing deeper semantic analysis without modifying the original data.
   - Each agent maintains **stateless execution**, avoiding shared mutable memory.
 ---
