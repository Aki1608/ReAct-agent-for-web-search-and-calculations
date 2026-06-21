# Autonomous Multi-Agent AI Team (CrewAI)

An advanced AI orchestration project that upgrades from a single-agent ReAct architecture to a **Multi-Agent System** using the **CrewAI** framework. Instead of relying on one AI model to juggle multiple tools and contexts, this repository creates a specialized "workforce" of AI agents that collaborate, delegate, and communicate to solve complex problems.

Powered by LangChain tools, Groq's Llama-3, and a custom Gradio interface that captures real-time agent-to-agent dialogue.

---

## The AI Crew (Agents)

This system currently employs two highly specialized agents:
1. **The Senior Researcher:** Has exclusive access to live web browsing (DuckDuckGo). Its only job is to find accurate numerical data, dates, and facts. It is strictly forbidden from doing math.
2. **The Lead Mathematician:** Has exclusive access to the Python `numexpr` calculator tool. It cannot search the web; it relies entirely on the data handed to it by the Researcher to perform accurate calculations.

---

## Core Features

* **Role-Based Execution:** Reduces LLM hallucinations by restricting agents to single, focused tasks.
* **Sequential Processing:** Tasks are linked in a pipeline. The Researcher completes its data-gathering task and automatically passes its findings to the Mathematician's task.
* **Terminal Interception:** Uses Python's `contextlib` to intercept CrewAI's standard terminal output and route it directly into the Gradio UI, allowing users to watch the agents "talk" to each other in real-time.
* **Dynamic Context Injection:** Automatically injects the current system `datetime` into the task descriptions so the agents never have to waste API calls searching for today's date.

---

## Project Structure

* `tools.py`: Defines the capabilities available to the agents (search and calculator tools).
* `agent_core.py`: Defines the CrewAI Agents, Tasks, and the Sequential Crew process.
* `app.py`: The Gradio web server that handles user input and captures the multi-agent console logs for the UI.
* `requirements.txt`: Project dependencies (now including `crewai`).
* `.env`: Configuration for the Groq API key.

---

## Installation & Setup

**1. Clone the repository:**

    git clone https://github.com/yourusername/multi-agent-crewai.git
    cd multi-agent-crewai

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

Open the provided local URL in your web browser. Try asking: *"Find the current stock price of Tesla and divide it by 2."*