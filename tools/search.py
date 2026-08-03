"""
Web search tool used by the "search" and "both" graph nodes.

Uses DuckDuckGo's free search endpoint via langchain_community so no extra
API key is required beyond GROQ_API_KEY. If you'd rather use Tavily (higher
quality results, needs TAVILY_API_KEY), swap the implementation below.
"""

from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()
