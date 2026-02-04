"""Run Telegram bot."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.tools.tavily import TavilyTools

from src.config import settings
from src.rag.agno import ContextualAgnoKnowledgeBase
from src.integrations.telegram import TelegramBot


def main():
    """Initialize and run Telegram bot."""
    # Initialize knowledge base
    print("📚 Carregando base de conhecimento...")
    kb = ContextualAgnoKnowledgeBase(table_name="economics_enhanced_gemini")
    
    # Check if knowledge base has documents
    try:
        test_search = kb.knowledge.search("test", max_results=1)
        print(f"✅ Knowledge base conectada (tabela: economics_enhanced_gemini)")
    except Exception as e:
        print(f"⚠️  Aviso: {e}")
    
    # Initialize tools
    tools = [YFinanceTools()]
    if settings.tavily_api_key:
        tools.append(TavilyTools(api_key=settings.tavily_api_key))
        print("✅ Tavily habilitado")
    
    # Initialize agent
    print("🤖 Inicializando agente...")
    agent = Agent(
        model=Gemini(id="gemini-2.5-flash", api_key=settings.google_api_key),
        knowledge=kb.knowledge,
        search_knowledge=True,
        markdown=True,
        tools=tools,
    )
    
    # Get Telegram token
    telegram_token = getattr(settings, 'telegram_bot_token', None)
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN não encontrado no .env")
        print("📝 Adicione: TELEGRAM_BOT_TOKEN=seu_token_aqui")
        return
    
    # Start bot
    print("\n🚀 Iniciando bot Telegram...")
    print("📱 Acesse: https://t.me/VMihaelBot")
    bot = TelegramBot(token=telegram_token, agent=agent)
    bot.run()


if __name__ == "__main__":
    main()
