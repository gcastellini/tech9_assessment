from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

class AnalysisAgent:
    def __init__(self, llm=None):
        self.llm = llm or ChatOllama(model="mistral")

    def analyze_trends(self, summary: str):
        print("[AnalysisAgent] Analyzing summarized trends...")
        message = HumanMessage(
            content=(
                f"Analyze the following summary. "
                f"Identify key themes, industries, sentiment, and potential opportunities.\n\n{summary}"
            )
        )
        try:
            response = self.llm.invoke([message])
            return response.content

        except Exception as e:
            print(f"[AnalysisAgent] Error during analysis: {e}")
            return "AnalysisAgent encountered an error while analyzing the trends."