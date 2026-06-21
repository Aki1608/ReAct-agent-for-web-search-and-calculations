import gradio as gr
from agent_core import ReActAgent

# Initialize the autonomous agent
agent = ReActAgent()

def format_reasoning_chain(intermediate_steps):
    """Parses LangChain's intermediate steps into a beautiful UI markdown string."""
    if not intermediate_steps:
        return "*The agent used its internal knowledge directly without external tools.*"
    
    chain_log = ""
    for step, observation in intermediate_steps:
        # step is an AgentAction object which contains the raw log of the thought
        # observation is the string returned by the tool
        
        # The 'log' contains the Thought, Action, and Action Input
        chain_log += f"```text\n{step.log}\n"
        chain_log += f"Observation: {observation}\n```\n\n"
        
    return chain_log

def process_query(user_input, history):
    """Processes the query and formats the chat UI response."""
    if not user_input.strip():
        return history + [("Please enter a question.", None)]
    
    # Run the agent
    final_answer, intermediate_steps = agent.solve(user_input)
    
    # Format the intermediate steps into a clean markdown block
    reasoning_markdown = format_reasoning_chain(intermediate_steps)
    
    # Combine the reasoning chain and the final answer
    full_response = f"### 🧠 Agent Reasoning Chain\n{reasoning_markdown}\n### Final Answer\n{final_answer}"
    
    # Append to Gradio chat history
    history.append((user_input, full_response))
    return "", history

# Build the Chatbot Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Autonomous ReAct Agent")
    gr.Markdown("Ask a complex question. The agent will decide if it needs to search the web, calculate math, or use its own brain. **Try asking:** *'What is the current age of Leonardo DiCaprio multiplied by 4?'*")
    
    chatbot = gr.Chatbot(height=600)
    
    with gr.Row():
        user_input = gr.Textbox(
            show_label=False, 
            placeholder="Type your complex question here and press Enter...",
            container=False,
            scale=8
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)
        
    # Bind actions
    user_input.submit(process_query, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    submit_btn.click(process_query, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
