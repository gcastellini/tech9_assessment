from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

class AnalysisAgent:
    def __init__(self, llm=None):
        self.llm = llm or ChatOllama(model="mistral")

    def analyze_trends(self, summary: str):
        print("[AnalysisAgent] Analyzing summarized trends...")
        message = HumanMessage(
            content=(
                f"Analyze the following consumer trend summary. "
                f"Identify key themes, industries, sentiment, and potential opportunities.\n\n{summary}"
            )
        )
        response = self.llm.invoke([message])
        return response.content