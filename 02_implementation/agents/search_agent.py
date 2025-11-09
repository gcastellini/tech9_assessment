from langchain_ollama import ChatOllama
from tavily import TavilyClient
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()
print("Loaded Tavily key:", os.getenv("TAVILY_API_KEY"))

class SearchAgent:
    def __init__(self, llm=None):
        self.llm = llm or ChatOllama(model="mistral")
        self.search_tool = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def search_trends(self, query: str):
        print(f"[SearchAgent] Searching Tavily for: {query}")
        response = self.search_tool.search(query)
        results = response.get("results", [])
    
        if not results:
            print("[SearchAgent] No results found.")
            return "No results found for this query."

        web_content = ""
        for r in results:
            title = r.get("title", "No title")
            url = r.get("url", "No URL")
            content = r.get("content", "")
        
            web_content += f"\n\nTitle: {title}\nURL: {url}\nSnippet: {content[:500]}"

        print("[WebAgent] Summarizing retrieved information...")
    
        message = HumanMessage(
            content=f"Summarize the following recent consumer trend information for 2025:\n{web_content[:4000]}"
        )   

        summary = self.llm.invoke([message])
        return summary.content