import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent

# .env load
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

openai_api_key = os.environ.get("OPENAI_API_KEY")
groq_api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("Groq_API_KEY")

if not openai_api_key and not groq_api_key:
    raise EnvironmentError(
        "Neither OPENAI_API_KEY nor GROQ_API_KEY was found."
    )

if not os.environ.get("TAVILY_API_KEY"):
    raise EnvironmentError(
        "TAVILY_API_KEY not found."
    )


def get_live_assistant():

    # Groq supported model
    model_name = "llama-3.3-70b-versatile"

    if groq_api_key:
        llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=openai_api_key,
        )

    # Search Tool
    search_tool = TavilySearchResults(max_results=5)

    tools = [search_tool]

    system_prompt = """
    You are a Live AI Assistant.

    Rules:
    1. Always search the internet before answering.
    2. Verify information using search results.
    3. Give accurate and up-to-date answers.
    4. If possible mention sources.
    5. Remember previous conversation context.
    """

    agent = create_agent(
        llm,
        tools,
        system_prompt=system_prompt,
        debug=True,
        name="live-search-agent",
    )

    return agent