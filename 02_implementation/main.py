from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent


def main():
    search_agent = SearchAgent()
    analysis_agent = AnalysisAgent()

    
    summary = search_agent.search_trends("consumer trends 2025 global")
    print("\n=== SUMMARY FROM WEB AGENT ===\n")
    print(summary)

    analysis = analysis_agent.analyze_trends(summary)
    print("\n=== ANALYSIS FROM ANALYSIS AGENT ===\n")
    print(analysis)

if __name__ == "__main__":
    main()