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
5. Final analysis is printed.

---

*End of document.*

