"""Agent factory for creating configured agents."""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.tools.tavily import TavilyTools
from agno.db.postgres import PostgresDb

from src.config import settings
from src.rag.agno import ContextualAgnoKnowledgeBase


def create_rag_agent(
    table_name: str = "economics_enhanced_gemini",
    num_history_runs: int = 10,
) -> Agent:
    """Create a RAG agent with knowledge base and tools.
    
    Args:
        table_name: Knowledge base table name.
        num_history_runs: Number of history runs to include in context.
        
    Returns:
        Configured Agent instance.
    """
    # Knowledge base
    kb = ContextualAgnoKnowledgeBase(table_name=table_name)
    
    # Tools
    tools = [YFinanceTools()]
    if settings.tavily_api_key:
        tools.append(TavilyTools(api_key=settings.tavily_api_key))
    
    # Database for sessions
    db = PostgresDb(db_url=settings.db_url)
    
    # Agent
    agent = Agent(
        model=Gemini(id="gemini-2.5-flash", api_key=settings.google_api_key),
        knowledge=kb.knowledge,
        search_knowledge=True,
        markdown=True,
        add_history_to_context=True,
        num_history_runs=num_history_runs,
        db=db,
        tools=tools,
    )
    
    return agent
