# Autonomous ReAct AI Agent

A lightweight, single-agent system built using the **Reason + Act (ReAct)** framework. Powered by **LangChain 1.0**, **Groq's Llama-3**, and an interactive **Gradio** UI, this agent doesn't just predict text—it autonomously decides when to use external tools to solve complex, multi-step queries.

This repository serves as a foundational exploration of autonomous AI workflows, featuring live web browsing and mathematical evaluation tools.

---

## Core Features

* **ReAct Architecture:** The agent is forced to "think" out loud before acting, looping through a Thought -> Action -> Observation cycle until it finds a final answer.
* **Native Tool Calling:** Utilizes LangChain's modern `create_agent` API for stable, JSON-based tool execution, avoiding legacy text-parsing errors.
* **Live Web Search:** Integrates DuckDuckGo to break out of its training data cutoff and fetch real-world facts.
* **Math Evaluator:** Uses Python's `numexpr` to safely evaluate complex mathematical expressions based on researched data.
* **Transparent Thought UI:** A custom Gradio chat interface that visually parses and displays the agent's internal monologue and tool usage.

---

## Project Structure

* `tools.py`: Defines the capabilities available to the agent (search and calculator tools).
* `agent_core.py`: Initializes the LLM, binds the tools, and establishes the LangChain execution loop.
* `app.py`: The Gradio web server that handles user input, system prompt injection (like current date), and chat history formatting.
* `requirements.txt`: Project dependencies.
  
---

## Installation & Setup

**1. Clone the repository:**

    git clone https://github.com/yourusername/ReAct-agent-for-web-search-and-calculations.git
    cd ReAct-agent-for-web-search-and-calculations

**2. Create a virtual environment:**

    python -m venv venv
    source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

**3. Install dependencies:**

    pip install -r requirements.txt

**4. Set up Environment Variables:**
Create a `.env` file in the root directory and add your free Groq API key:

    GROQ_API_KEY=your_groq_api_key_here

**5. Run the application:**

    python app.py

Open the provided local URL in your web browser to start interacting with the agent.

---

## Known Limitations & Future Roadmap

While this single-agent ReAct architecture is a powerful proof-of-concept, it intentionally demonstrates the architectural boundaries of relying on a single Large Language Model for complex workflows. Documenting these trade-offs paves the way for future iterations:

1. **The Single-Agent Bottleneck:** A single LLM prompt is responsible for researching, parsing data, and executing math. If a web search returns messy text, the agent can become overwhelmed and inject non-mathematical strings into the Calculator tool, causing a crash.
2. **Lack of Specialization:** Because one agent wears all the hats (Researcher, Mathematician, QA), complex tasks can degrade its focus. It lacks the safety of a "reviewer" node.
3. **Temporal Blindness:** LLMs do not possess an internal clock. This architecture relies on hardcoded system prompt injections (passing the system `datetime` behind the scenes) to prevent the agent from hallucinating or wasting API calls trying to search for "today's date".

### Next Steps: Multi-Agent Architecture
To resolve these bottlenecks, the planned next iteration of this workflow is a transition to a **Multi-Agent System** (using frameworks like CrewAI or LangGraph). Delegating tasks to specialized agents (e.g., a dedicated "Researcher" passing clean data to a "Mathematician") will drastically reduce hallucinations and improve tool reliability.
