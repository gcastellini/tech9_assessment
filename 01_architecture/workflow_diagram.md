```mermaid
flowchart TD
    A[User Input] --> B[SearchAgent]
    B -->|query via Tavily| C[Tavily API]
    C -->|returns structured summary| D[SearchAgent Output]
    D --> E[AnalysisAgent]
    E -->|semantic analysis via Ollama| F[Ollama Model]
    F -->|returns insights| G[AnalysisAgent Output]
    G --> H[Console + execution_log.txt]
