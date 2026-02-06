import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents import create_rag_agent
from src.logger import logger


def test_memory_isolation_with_fresh_agents():
    logger.info("Initializing test with fresh agents per request...")

    # User 1: Vitor
    logger.info("User 1 (Vitor) says hello (Agent A)")
    agent_a = create_rag_agent()
    agent_a.run(
        "My name is Vitor. Remember that.", session_id="user_1", user_id="user_1"
    )

    # User 2: Bob
    logger.info("User 2 (Bob) asks who the other person is (Agent B)")
    agent_b = create_rag_agent()
    response = agent_b.run(
        "What is the name of the person you were just talking to?",
        session_id="user_2",
        user_id="user_2",
    )

    logger.info(f"Agent response to Bob: {response.content}")

    if "Vitor" in response.content:
        logger.error("❌ MEMORY LEAK DETECTED: Agent told Bob about Vitor!")
    else:
        logger.info("✅ SUCCESS: Agent did not leak Vitor's name to Bob.")

    # User 1 again
    logger.info("User 1 (Vitor) asks for their name (Agent C)")
    agent_c = create_rag_agent()
    response = agent_c.run("What is my name?", session_id="user_1", user_id="user_1")
    logger.info(f"Agent response to Vitor: {response.content}")

    if "Vitor" in response.content:
        logger.info("✅ SUCCESS: Agent remembered Vitor's name via DB history.")
    else:
        logger.warning("❌ FAIL: Agent forgot Vitor's name.")


if __name__ == "__main__":
    test_memory_isolation_with_fresh_agents()
