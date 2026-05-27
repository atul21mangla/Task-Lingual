# 🚀 Task Lingual: The Natural Language Todo List of the Future 🧠🤖✨

> **Welcome to the Todo app that *understands* you.**  
> No more clunky ID inputs, syntax commands, or endless button-clicking. Just talk to it in plain English — or use the sleek Streamlit dashboard. **Pick your weapon.** ⚔️

---

## 📡 The Big Picture: Two Ways to Rule Your Tasks

```
        ┌─────────────────────────────────────────────────────┐
        │                                                     │
        │   🖥️  CLI TERMINAL                          │
        │   "Add buy groceries for tomorrow"                  │
        │                                                     │
        │            │                                        │
        │            ▼                                        │
        │   ┌─────────────────┐     ┌─────────────────┐       │
        │   │  LangChain      │────▶│  Groq Llama 3.3 │       │
        │   │  Agent          │◀────│  LLM            │       │
        │   └────────┬────────┘     └─────────────────┘       │
        │            │                                        │
        │            ▼                                        │
        │   ┌──────────────────────────────────────┐          │
        │   │  Tools (add/list/update/delete/search)│          │
        │   └──────────────────┬───────────────────┘          │
        │                      │                              │
        │                      ▼                              │
        │   ┌──────────────────────────────────────┐          │
        │   │  SQLAlchemy ORM → SQLite (todos.db)  │          │
        │   └──────────────────────────────────────┘          │
        │                      ▲                              │
        │                      │                              │
        │   ┌──────────────────┴───────────────────┐          │
        │   │  Streamlit Web UI (streamlit_app.py)  │          │
        │   │  📋 Manage Todos Tab                 │          │
        │   │  🤖 AI Chat Tab                      │          │
        │   └─────────────────────────────────────┘          │
        │                      ▲                              │
        │   🌐  BROWSER       │                               │
        │   "Click, type, chat — your call"                   │
        └─────────────────────────────────────────────────────┘
```

**Two interfaces. One database. Zero compromises.**  
Whether you're a terminal cowboy or a dashboard dweller, your todos stay in sync.

---

## 🔥 What Makes This App Insane

| Feature | CLI Mode | Streamlit UI |
|---------|----------|-------------|
| 🗣️ **Natural Language** | Full GPT-level conversation | Dedicated AI Chat tab |
| ⚡ **Speed** | Groq's sub-100ms inference | Instant UI feedback |
| 🖱️ **Click & Point** | — | Full CRUD with buttons |
| 🔄 **Inline Editing** | Via LLM rephrase | Click ✏️ → edit in place |
| 🏷️ **Filters** | Ask "show high priority" | Dropdown + search box |
| 📊 **Stats at a Glance** | "How many todos?" | Sidebar live counters |
| 🎨 **Visual Badges** | Text-only | Color-coded status/priority |
| 💬 **Chat History** | Per-session memory | Persistent in tab |
| 🗑️ **Delete with Confirm** | "Remove the task..." | ✅ Confirm button |

---

## 🏗️ Project Architecture (The Full Picture)

```mermaid
graph TB
    subgraph "🖥️ CLI Interface"
        CLI[main.py REPL Loop]
    end

    subgraph "🌐 Web Interface"
        WEB[streamlit_app.py<br/>Streamlit Server]
    end

    subgraph "🧠 AI Layer"
        AGENT[agent.py<br/>LangChain Agent]
        LLM[Groq LLM<br/>llama3/ gpt-oss-120b]
        TOOLS[tools.py<br/>@tool decorators]
        MEM[InMemorySaver<br/>Conversation Memory]
    end

    subgraph "💾 Service Layer"
        SVC[todo_service.py<br/>CRUD Functions]
        DB_STRUCT[list_todos_structured<br/>returns List[dict]]
    end

    subgraph "🗄️ Data Layer"
        ORM[database.py<br/>SQLAlchemy ORM]
        DB[(todos.db<br/>SQLite)]
    end

    CLI --> AGENT
    WEB --> SVC
    WEB --> AGENT
    AGENT --> LLM
    LLM --> TOOLS
    TOOLS --> SVC
    AGENT --> MEM
    SVC --> ORM
    SVC --> DB_STRUCT
    ORM --> DB
    DB_STRUCT --> WEB
```

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| 🧠 **LLM** | Groq (`llama-3.3-70b-versatile` / `openai/gpt-oss-120b`) | Latest |
| 🤖 **Agent Framework** | LangChain + LangGraph | ≥0.3.0 |
| 🔧 **Tool Binding** | LangChain `@tool` decorators | ≥0.3.0 |
| 🌐 **Web UI** | Streamlit | ≥1.35.0 |
| 🗄️ **ORM** | SQLAlchemy | ≥2.0.0 |
| 💾 **Database** | SQLite (file-based) | — |
| 🔐 **Env Management** | python-dotenv | ≥1.0.0 |
| ✅ **Validation** | Pydantic | ≥2.0.0 |
| 📦 **Package Manager** | `uv` (fast Python package manager) | Latest |

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) — *the blisteringly fast Python package manager*
- A Groq API key → [get one free at console.groq.com](https://console.groq.com)

### 2. Clone & Environment Setup

```powershell
# Clone (if you haven't already)
git clone <repo-url>
cd TodosGenAi

# Create virtual environment
uv venv

# Activate it
.venv\Scripts\activate

# Install ALL dependencies (CLI + Streamlit)
uv pip install -r requirements.txt
```

### 3. API Key

Drop this in `.env` at the project root:
```env
GROQ_API_KEY="gsk_your-actual-groq-api-key-here"
```

---

## 🎮 How to Launch

### 🖥️ Option A: CLI Mode (Terminal Cowboy 🤠)

```powershell
python main.py
```

```
============================================================
Welcome to your Natural Language Todo Assistant!
Powered by Groq LLM and LangChain.
Type 'exit' or 'quit' to quit.
============================================================

You: Add buy groceries for tomorrow
Assistant: Successfully created Todo [ID: 1] Title: 'buy groceries' | Priority: medium

You: List all my high priority tasks
Assistant: # ID: 3 ||| Title: Fix critical bug ||| Status: Pending ||| Priority: High
```

### 🌐 Option B: Streamlit UI (Dashboard Dweller 🖱️)

```powershell
python -m streamlit run streamlit_app.py
```

This opens **http://localhost:8501** in your browser with two tabs:

#### 📋 Manage Todos Tab
- **Add** — Expander form with title, description, priority selector
- **Filter** — By status (All / Pending / In Progress / Completed) + priority + text search
- **Toggle** — One-click ✅ / ⬜ to mark completed/pending
- **Edit** — Click ✏️ for inline editing of every field
- **Delete** — 🗑️ with ✅ confirmation to prevent accidents
- **Live Stats** — Sidebar shows Total / Pending / Completed / In Progress counters

#### 🤖 AI Chat Tab
- Full conversational interface powered by the same Groq LLM agent
- Type anything: *"Add watch The Boys"*, *"What's left to do?"*, *"Delete the grocery task"*
- Chat history persists during your session
- Spinner shows when the AI is thinking

---

## 💬 Natural Language Examples (CLI & AI Chat)

| What You Say | What Happens |
|-------------|--------------|
| *"Add buy groceries for tomorrow"* | Creates todo with title "buy groceries" |
| *"Add a high priority task: fix login bug with details about the auth module"* | Creates with priority "high" + description |
| *"Show me all my tasks"* | Lists every todo |
| *"What's pending?"* | Filters by status=pending |
| *"List high priority items"* | Filters by priority=high |
| *"Mark the grocery task as done"* | 🔍 Searches by title → finds ID → updates status |
| *"Change the grocery task to in progress"* | 🔍 Search → sets status to in_progress |
| *"Update the grocery task — change title to 'Buy organic groceries' and priority to high"* | 🔍 Search → batch update |
| *"Remove the task about groceries"* | 🔍 Search → deletes by ID |
| *"Delete everything that's completed"* | Lists completed → deletes each by ID |
| *"How many tasks do I have?"* | Counts all todos |
| *"What did I do yesterday?"* | Lists with date filter (LLM interprets) |

---

## 📂 Project Structure (Annotated)

```text
📦 TodosGenAi
├── 🧠 agent.py                 # LangChain agent + Groq LLM setup
├── 💾 database.py               # SQLAlchemy engine, session, Todo model
├── 🛠️ tools.py                  # LangChain @tool CRUD wrappers
├── 📋 todo_service.py           # Pure Python CRUD + list_todos_structured()
├── 🖥️ main.py                   # CLI REPL loop
├── 🌐 streamlit_app.py          # Streamlit web UI (2 tabs)
│
├── 🔑 .env                      # API keys (GROQ_API_KEY)
├── 📜 requirements.txt          # Python dependencies
├── 📦 pyproject.toml            # Project metadata (uv)
├── 🐍 .python-version           # Python 3.11
├── 🚫 .gitignore                # Git exclusions
│
├── 🗄️ todos.db                  # SQLite database (auto-created)
└── 📖 README.md                 # You are here 🎯
```

---

## 📦 Dependencies at a Glance

```
# Core AI
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0
langchain-groq>=0.2.0

# Database
sqlalchemy>=2.0.0

# Configuration
python-dotenv>=1.0.0
pydantic>=2.0.0

# Web UI
streamlit>=1.35.0
```

---

## 🧠 How the Agent Thinks (Under the Hood)

When you type *"Mark the grocery task as done"*, here's the **exact** chain reaction:

1. **`main.py`** reads your input and calls `agent.run_agent()`
2. **`agent.py`** sends your message to Groq's LLM with a system prompt and 5 tool definitions
3. **Groq** recognizes the intent: "mark as done" → `update_todo_tool`, but needs the ID
4. **Tool call #1**: `search_todos_by_title_tool(title_query="grocery")` → returns `ID 1: 'buy groceries'`
5. **Groq** now has the ID → calls `update_todo_tool(todo_id=1, status="completed")`
6. **`tools.py`** delegates to **`todo_service.py`**, which updates **SQLite via SQLAlchemy**
7. Result flows back: `todo_service` → `tools` → `agent` → Groq formats a natural language response → you see *"✅ Marked 'buy groceries' as completed!"*

**All of this happens in under 2 seconds.** ⚡

---

## ❤️ Made with passion by Atul

> *If you can describe it in English, this app can do it.*  
> No syntax to learn. No buttons to memorize. Just **type what you want.**

---

*Built with 🤖 Groq + LangChain + 🎈 Streamlit + ☕ too much coffee*
