import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import AGENT_TOOLS

load_dotenv()

class ReActAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # LangChain 1.0 Standard: create_agent replaces the old AgentExecutor!
        self.agent = create_agent(
            model=self.llm,
            tools=AGENT_TOOLS
        )

    def solve(self, question: str) -> tuple[str, list]:
        try:
            # The new API uses standardized message dictionaries
            response = self.agent.invoke(
                {"messages": [{"role": "user", "content": question}]}
            )
            
            # Extract the conversation history loop
            messages = response.get("messages", [])
            
            if not messages:
                return "Error: No response generated.", []
                
            # The final LLM response is always the last message in the list
            final_answer = messages[-1].content
            
            # The intermediate steps (Thought -> Action -> Observation) are everything in between
            intermediate_steps = messages[1:-1]
            
            return final_answer, intermediate_steps
            
        except Exception as e:
            return f"Agent Error: {str(e)}", []
