import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from tools import AGENT_TOOLS

load_dotenv()

class ReActAgent:
    def __init__(self):
        # We use temperature=0 for agents to prevent hallucinations in tool usage
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # This is the classic ReAct prompt that forces the "Thought -> Action -> Observation" loop
        template = """Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Question: {input}
        Thought:{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)

        # Build the agent logic
        agent = create_react_agent(
            llm=self.llm,
            tools=AGENT_TOOLS,
            prompt=prompt
        )

        # The Executor runs the loop. return_intermediate_steps=True is critical
        # so we can extract the thought process to show in the UI!
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=AGENT_TOOLS, 
            verbose=True, 
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

    def solve(self, question: str) -> tuple[str, list]:
        """Runs the agent and extracts the final answer alongside its thought process."""
        try:
            response = self.agent_executor.invoke({"input": question})
            
            final_answer = response.get("output", "I could not find an answer.")
            intermediate_steps = response.get("intermediate_steps", [])
            
            return final_answer, intermediate_steps
            
        except Exception as e:
            return f"Agent Error: {str(e)}", []
