import gradio as gr
from agent_core import ReActAgent

# Initialize the autonomous agent
agent = ReActAgent()

def format_reasoning_chain(intermediate_steps):
    """Parses LangChain 1.0 message objects into a readable UI format."""
    if not intermediate_steps:
        return "*The agent used its internal knowledge directly without external tools.*\n\n"
    
    chain_log = ""
    for msg in intermediate_steps:
        # Extract the Agent's decision to use a tool (Action)
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tool in msg.tool_calls:
                chain_log += f"**Thought:** I need to use an external tool.\n"
                chain_log += f"**Action:** {tool['name']}\n"
                chain_log += f"**Action Input:** {tool['args']}\n\n"
                
        # Extract the Tool's response (Observation)
        elif msg.__class__.__name__ == "ToolMessage":
            chain_log += f"**Observation:** {msg.content}\n\n"
            
    return chain_log

def process_query(user_input, history):
    """Processes the query and formats the chat UI response."""
    if not user_input.strip():
        return "", history
    
    # Run the agent
    final_answer, intermediate_steps = agent.solve(user_input)
    
    # Format the intermediate steps into a clean block
    reasoning_markdown = format_reasoning_chain(intermediate_steps)
    
    # Combine the reasoning chain and the final answer
    full_response = f"### Agent Reasoning Chain\n\n{reasoning_markdown}\n### Final Answer\n\n{final_answer}"
    
    # Append dictionaries instead of a tuple (matches modern Gradio requirements)
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": full_response})
    
    return "", history

# Build the Chatbot Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Autonomous AI Agent")
    gr.Markdown("Ask a complex question. The agent will decide if it needs to search the web, calculate math, or use its own brain. **Try asking:** *'What is the current age of Leonardo DiCaprio multiplied by 4?'*")
    
    # Removed the unsupported 'type' argument
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
