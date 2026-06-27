# End-to-End Chatbot App — Simple QA to Agentic Multi-Provider Chat

Two Streamlit chatbot apps built on LangChain: a straightforward OpenAI QA interface and an advanced multi-provider chatbot with persistent conversation memory and a user profiling system.

---

## What's Inside

### `end to end chatbot app and apis.py` — Simple QA Chatbot
A clean, single-turn Q&A interface powered by OpenAI. Enter a question, get an answer. Configurable from the sidebar — model, temperature, and max tokens. Built with LangChain's LCEL pattern (`prompt | llm | StrOutputParser()`).

### `adv_webapp.py` — Advanced Multi-Provider Chatbot
A full-featured chat application with persistent message history stored in SQLite. Features include:
- **Multi-provider support** — switch between OpenAI, Groq, and local Ollama models from the sidebar
- **Persistent conversation memory** — all messages saved to a local SQLite database and loaded back into the LangChain message history on every turn
- **User profiling** — tracks the topics you discuss (architecture, databases, security, etc.) and dynamically adapts the system prompt to match your communication style
- **Session reset** — wipe conversation history without losing the app state
- **Auto-discovery of local Ollama models** — queries `localhost:11434` to populate the model list

### `simple_app.ipynb` — Notebook exploration of chatbot concepts

---

## Project Structure

```
├── end to end chatbot app and apis.py   # Simple OpenAI QA chatbot
├── adv_webapp.py                        # Advanced multi-provider chatbot with memory
├── simple_app.ipynb                     # Notebook experiments
└── requirements.txt                     # Python dependencies
```

---

## Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/neobaul/project-4-end-to-end-chatbox-app.git
cd project-4-end-to-end-chatbox-app
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install langchain-ollama streamlit
```

### 4. Set up API keys
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here      # for Groq models
```
For Ollama, make sure it's running locally:
```bash
ollama serve
```

### 5. Run the apps
```bash
# Simple QA chatbot
streamlit run "end to end chatbot app and apis.py"

# Advanced multi-provider chatbot
streamlit run adv_webapp.py
```

---

## How the Advanced App Works

```
User message
    ↓
SQLite (save message)
    ↓
Fetch full history from SQLite → LangChain message objects
    ↓
User profile analysis (topic detection → dynamic system prompt)
    ↓
ChatPromptTemplate (system + history + current question)
    ↓
Selected LLM (OpenAI / Groq / Ollama)
    ↓
Response → display + save to SQLite
```

The user profile tracks detected engineering topics across your conversation history and adjusts the assistant's communication style accordingly — no extra prompting needed.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Web App | Streamlit |
| LLM Providers | OpenAI, Groq, Ollama (local) |
| Orchestration | LangChain LCEL |
| Conversation Memory | SQLite (`agency_matrix.db`) |
| Message History | `HumanMessage`, `AIMessage`, `MessagesPlaceholder` |
| Language | Python 3.11 |

---

## Features at a Glance

**Simple App**
- Model selector (GPT-3.5 / GPT-4 / GPT-4-32k)
- Temperature and max tokens sliders
- API key input via sidebar

**Advanced App**
- Provider switcher (OpenAI / Groq / Ollama)
- Persistent multi-turn memory via SQLite
- Dynamic system prompt based on user topic history
- Auto-detection of locally running Ollama models
- One-click conversation history reset
