# Agent Design

## Overview

This document describes the design of a simple two-agent pipeline implemented in Python: a **SearchAgent** (web/sourcing) and an **AnalysisAgent** (interpretation/LLM). The architecture favors separation of concerns: one agent gathers and condenses external information; the other analyzes that condensed information and produces actionable insights.

Goals:
- Keep agents small, testable and replaceable.
- Use LLMs for summarization and analysis while avoiding overuse of API calls.
- Make configuration (API keys, models) environment-driven.

---

## Components

### `SearchAgent`
**Responsibility:** Query external search (Tavily client in current repo), aggregate results, produce a concise summary for downstream consumption.

**Key behaviours:**
- Accepts a `query` string and returns a `summary` string.
- Uses an external search client (`TavilyClient`) to fetch results.
- Trims/limits content passed to the LLM to respect token limits.
- Uses an LLM (wrapped by `langchain_ollama.ChatOllama` in the current code) to produce a short, high-level summary.

**Important fields and methods:**
```py
class SearchAgent:
    def __init__(self, llm=None, search_client=None):
        # llm: LLM wrapper object
        # search_client: external search tool (TavilyClient)
    def search_trends(self, query: str) -> str:
        # returns a summarized string
```

**Configuration / environment:**
- `TAVILY_API_KEY` in `.env` or environment.

**Failure modes & mitigation:**
- No results returned -> return a friendly string and/or raise a custom exception.
- Unreliable search responses -> validate response structure before using it.
- LLM errors -> catch and return a fallback or raise up for caller to handle.

---

### `AnalysisAgent`
**Responsibility:** Accept a textual summary and produce structured analysis: key themes, sentiment, affected industries, opportunities, and recommended actions.

**Key behaviours:**
- Receives text from `SearchAgent` and runs a reasoning prompt to extract insights.
- Returns LLM output (ideally structured: JSON or bullet lists).

**Important fields and methods:**
```py
class AnalysisAgent:
    def __init__(self, llm=None):
        # create or accept an LLM instance
    def analyze_trends(self, summary: str) -> str:
        # produce analysis
```

**Output format suggestion:** Prefer structured JSON for programmatic consumption, for example:
```json
{
  "themes": ["sustainability", "ai adoption"],
  "industries": ["retail", "financial services"],
  "sentiment": "mixed",
  "opportunities": ["subscription models", "automation tooling"]
}
```

---

### `main.py`
**Responsibility:** Orchestrate the pipeline: instantiate agents, run search, then analysis, and print/store outputs.

**Pattern:** Keep `main()` thin; use dependency injection to help testing.

---

## Data Flow

1. `main()` creates a `SearchAgent` and `AnalysisAgent` (or uses dependency injection).
2. `SearchAgent.search_trends(query)` calls the search API, builds a consolidated `web_content` string, and asks the LLM to summarize.
3. The summary (string) is returned to `main()` and passed to `AnalysisAgent.analyze_trends(summary)`.
4. `AnalysisAgent` issues a prompt asking the LLM to extract key themes, sentiment, industries, and opportunities.
5. Final analysis is printed and/or stored.

---

## Prompts & LLM Usage

- **Search summarization prompt** should instruct the model to be concise, prioritize recency, and extract verifiable facts.
- **Analysis prompt** should ask for structured output (JSON or markdown lists). Always include a short example of the desired format to reduce hallucinations.
- **Token control**: truncate or prioritize content when `web_content` exceeds the model's effective context window.

Example analysis prompt snippet:
```
Analyze the following summary and return JSON with fields: themes, industries, sentiment, and opportunities.
Summary: <summary text>
```

---

## Error Handling and Observability

- Wrap external API calls with retry/backoff (e.g., `tenacity`) and clear logging.
- Validate third-party responses before using them (check keys like `results`).
- Add structured logging for:
  - Search queries and result counts
  - Summarization start/end and token usage (if available)
  - Analysis start/end and LLM response status
- Add metrics counters: `search_requests`, `search_failures`, `analysis_requests`, `analysis_failures`.

---

## Configuration & Dependencies

- Store secrets and keys in environment variables, loaded with `python-dotenv` for local development.
- Key dependencies in `requirements.txt` (example):
```
python-dotenv
langchain-ollama
tavily
tenacity
```

---

## Extensibility

- **Pluggable search clients:** create an abstract `SearchClient` interface and make `TavilyClient` an implementation. That makes it easy to swap Bing/Google/other search providers.
- **Pluggable LLMs:** accept an `llm` argument in agent constructors so you can inject OpenAI, Ollama, or locally-run models.
- **Output adapters:** write adapters to persist analysis to JSON, a database, or send to a dashboard.

---

## Testing

- Unit tests for each agent: mock LLM and search client responses.
- Integration tests: run a lightweight end-to-end flow with a deterministic stubbed search client.
- Example pytest structure:
```
tests/
  test_search_agent.py
  test_analysis_agent.py
  test_pipeline_integration.py
```

---

## Security & Privacy

- Avoid logging full web content or PII. Mask or redact sensitive fields.
- Rate-limit queries to avoid API key abuse.
- Be explicit in the README about what data is sent to external LLM providers.

---

## Example: Minimal improvements to the provided code

- Return consistent types (always a string summary or structured JSON). Current `search_agent.search_trends` returns `summary.content` (string) — keep that but prefer JSON when possible.
- Add small helpers:
  - `_format_web_content(results, max_chars=4000)` — responsible for truncation & sanitization
  - `_call_llm(prompt)` — centralizes LLM invocation, retries, and error handling

---

## Next steps / To Do
- Add tests and CI pipeline
- Implement retry/backoff and rate limiting
- Add schema validation for analysis output (e.g., `pydantic` models)
- Provide a CLI and/or a small web UI for interactive queries

---

*End of document.*

