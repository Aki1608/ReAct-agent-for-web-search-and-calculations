import numexpr as ne
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Tool 1: Live Web Search (Using DuckDuckGo - Free, no API key needed)
search_tool = DuckDuckGoSearchRun(
    name="Web_Search",
    description="Useful for when you need to answer questions about current events, real-time data, or facts you don't know."
)

# Tool 2: Mathematical Calculator
@tool("Calculator")
def calculator_tool(expression: str) -> str:
    """
    Useful for when you need to answer questions about math.
    Input should be a mathematical expression (e.g., '12 * 4.5 / 2').
    """
    try:
        # numexpr is a safe, fast numerical evaluator for Python
        result = ne.evaluate(expression).item()
        return str(result)
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

# Export tools as a list for the Agent
AGENT_TOOLS = [search_tool, calculator_tool]
