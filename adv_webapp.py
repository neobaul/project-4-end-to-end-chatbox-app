# library configuration
import streamlit as st
import os
import sqlite3
import json
import requests
from dotenv import load_dotenv

# langchain ecosystem structural core imports
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# model platform connector
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

# initialize secure environment variable arrays
load_dotenv()

# --------------- COMPREHENSIVE MULTI-LAYER DATABASE SAFETY MECHANISMS ---------------
DB_FILE='agency_matrix.db'

def init_db():
    """Initializes high-throughput transactional storage maps cleanly."""
    try:
        with sqlite3.connect(DB_FILE, timeout=15) as conn:
            cursor = conn.cursor()
            # Create a table for storing user interactions with encryption
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactional_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # sophisticated behavioral monitoring space
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cognitive_profiles (
                    user_id TEXT PRIMARY KEY,
                    profile_payload TEXT,
                    metrics_count INTEGER DEFAULT 1,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Critical Storage Layer Signal Fault: {str(e)}")
        return False

def save_log(session_id, role, content):
    """Safely records conversation logs into local database streams."""
    try:
        with sqlite3.connect(DB_FILE, timeout=15) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactional_logs (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )
            conn.commit()
    except Exception as e:
        st.error(f"Data write security lockout: {str(e)}")

def fetch_logs(session_id):
    """Reconstructs historical communication tracking arrays directly into langchain classes."""
    try:
        with sqlite3.connect(DB_FILE, timeout=15) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM transactional_logs WHERE session_id = ? ORDER BY timestamp ASC",
                (session_id,)
            )
            rows = cursor.fetchall()

            chain_memory = []
            for role, content in rows:
                if role == "user":
                    chain_memory.append(HumanMessage(content=content))
                elif role == "assistant":
                    chain_memory.append(AIMessage(content=content))
                elif role == "system":
                    chain_memory.append(SystemMessage(content=content))
            return chain_memory
    except Exception as e:
        st.error(f"Data retrieval security lockout: {str(e)}")
        return []

def obliterate_logs(session_id):
    """Wipes log architecture immediately without fracturing metadata frameworks."""
    try:
        with sqlite3.connect(DB_FILE, timeout=15) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM transactional_logs WHERE session_id = ?",
                (session_id,)
            )
            conn.commit()
    except Exception as e:
        st.error(f"Data purge routine aborted: {str(e)}")

def acquire_profile(user_id):
    """Gathers complex profile matrix indices regarding the active operative."""
    baseline = {
        "style_alignment": "Highly Adaptive / Metric Factored",
        "conceptual_depth": "Advanced Infrastructure Engineer",
        "semantic_focus_vectors": [],
        "inferred_behavior_intent": "Analyzing execution pipeline thresholds."
    }
    try:
        with sqlite3.connect(DB_FILE, timeout=15) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT profile_payload FROM cognitive_profiles WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
    except Exception:
        pass
    return baseline

def update_profile(user_id, last_input):
    """Agency Engine Matrix: Asynchronously updates cognitive profile indicators."""
    current = acquire_profile(user_id)

    # advanced domain discovery filter array
    lexicon_map = ["architecture", "pipeline", "database", "latency", "optimization", "security", "microservices", "deployment"]
    detected_vectors = [term for term in lexicon_map if term in last_input.lower()]

    for vector in detected_vectors:
        if vector not in current["semantic_focus_vectors"]:
            current["semantic_focus_vectors"].append(vector)

    if len(last_input) > 200 or "architect" in last_input.lower():
        current["style_alignment"] = "Hyper-Dense / Raw Syntax Direct"

    try:
        with sqlite3.connect(DB_FILE, timeout=15) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cognitive_profiles (user_id, profile_payload, metrics_count, last_updated)
                VALUES (?, ?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                profile_payload = excluded.profile_payload,
                metrics_count = metrics_count + 1,
                last_updated = CURRENT_TIMESTAMP
            """, (user_id, json.dumps(current)))
            conn.commit()
    except Exception:
        pass

init_db()  # ensure database is initialized at startup
# --------------- END OF DATABASE SAFETY MECHANISMS ---------------

#---------------MAIN PAGE WINDOW SPECIFICATIONS AND INTERFACE LOGIC--------------

st.set_page_config(
    page_title="Agentic AI System Studio",
    page_icon="🤖",
    layout="wide"
)

# initialize session storage states without causing ui reset loops.
if "active_user_id" not in st.session_state:
    st.session_state.active_user_id = "agency_production_agent_alpha_01"

if "trigger_rerun" not in st.session_state:
    st.session_state.trigger_rerun = False

# handle clean page refreshes safely to prevent white screen crashes.
if st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.rerun()

#----------- ENVIROMENT BASED DISCOVERY LOGIC -----------------
@st.cache_data(ttl=15)
def locate_local_ollama_engines():
    """Discovers local Ollama instances and retrieves available model lists."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3.5)
        if response.status_code == 200:
            return [model["name"] for model in response.json().get("models", [])]
    except Exception:
        return []
    return []

def route_matrix_options(provider):
    """Dynamically adjusts model selection options based on provider choice."""
    if provider == "OpenAI":
        return ["gpt-3.5-turbo", "gpt-4o", "gpt-4-32k"]
    elif provider == "Groq":
        return ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"]
    elif provider == "Ollama (Local)":
        discovered = locate_local_ollama_engines()
        return discovered if discovered else ["No Local Ollama Engines Detected. Start Ollama."]
    else:
        return []

#------------------ CONTROL ARCHITECTURE (LEFT PANEL) FOR MODEL SELECTION AND CONFIGURATION ------------------
with st.sidebar:
    st.title("Control Panel")
    st.markdown("---")

    st.subheader("Master Agency Directive")
    system_prompt_input = st.text_area(
        "Custom System Instructions:",
        value="You are an elite, multi-agent orchestrator executing tasks within strict operational parameters. designed to provide detailed, accurate, and context-aware responses. Always ask clarifying questions if the user's query is ambiguous.",
        height=140
    )
    st.markdown("---")

    st.subheader("Tracked Cognitive Footprint")
    profile_live = acquire_profile(st.session_state.active_user_id)
    st.markdown(f"**Structural Format Target:** '{profile_live['style_alignment']}'")
    st.markdown(f"**Cognitive Depth Assessment:** '{profile_live['conceptual_depth']}'")
    st.markdown(f"**Mapped Engineering Vectors:** {', '.join([f'`{v}`' for v in profile_live['semantic_focus_vectors']]) if profile_live['semantic_focus_vectors'] else 'None detected'}")

    st.markdown("---")

    st.subheader("Model Router")
    provider_choice = st.selectbox("Ecosystem Pool Selector:", ["OpenAI", "Groq", "Ollama (Local)"])
    selected_model = st.selectbox(f"Active {provider_choice} Core Engine:", route_matrix_options(provider_choice))

    st.markdown("---")
    st.subheader("Secure Token Management")
    api_key = ""
    if provider_choice == "OpenAI":
        api_key = st.text_input("OpenAI Secure Token:", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    elif provider_choice == "Groq":
        api_key = st.text_input("Groq Secure Token:", type="password", value=os.getenv("GROQ_API_KEY", ""))

    st.markdown("---")
    st.subheader("Execution Variables")
    temperature = st.slider("Temperature Range (Variance)", 0.0, 2.0, 0.3, 0.1)
    max_tokens = st.slider("Allocation Range (Max Tokens)", 64, 4096, 2048, 64)

    if st.button("Reset Operational Memory Maps", use_container_width=True):
        obliterate_logs(st.session_state.active_user_id)
        st.toast("Internal conversation maps successfully deleted.")
        st.session_state.trigger_rerun = True
        st.rerun()

#--------------- BACKEND MODEL ORCHESTRATION CONSTRUCTION----------------
def instantiate_engine(provider, model, key, temp, max_t):
    try:
        if provider == "OpenAI":
            if not key: return None, "OpenAI token missing inside credential sub-tier panels."
            return ChatOpenAI(api_key=key, model=model, temperature=temp, max_tokens=max_t), None
        elif provider == "Groq":
            if not key: return None, "Groq token missing inside credential sub-tier panels."
            return ChatGroq(api_key=key, model=model, temperature=temp, max_tokens=max_t), None
        elif provider == "Ollama (Local)":
            if model == "No Local Ollama Engines Detected. Start Ollama.":
                return None, "Verify local client socket bindings (ollama serve) running on port 11434."
            return ChatOllama(model=model, temperature=temp, base_url="http://localhost:11434"), None
    except Exception as e:
        return None, str(e)
    return None, "System configuration unmapped."

#--------------MAIN EXECUTION INTERFACE---------------------
st.title("Enterprise Agency AI Platform")
st.caption(f"Pipeline Context ID: `{st.session_state.active_user_id}` | Direct Router: **{provider_choice}**")
st.markdown("---")

# render historical context maps safely from the database
active_history = fetch_logs(st.session_state.active_user_id)
for message in active_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# process operational interface inputs
user_query = st.chat_input("Dispatch task guidelines...")

if user_query:
    # immediately render input to ensure crisp visual updates
    with st.chat_message("user"):
        st.markdown(user_query)

    save_log(st.session_state.active_user_id, "user", user_query)

    llm, router_fault = instantiate_engine(provider_choice, selected_model, api_key, temperature, max_tokens)

    if router_fault:
        st.error(f"Core Router Routing Intercept Failure: {router_fault}")
    elif llm:
        # pull real-time behavioral data structures.
        behavior_metrics = acquire_profile(st.session_state.active_user_id)

        # Hyper-Advanced dynamic context injection system prompt
        composite_agency_system_directive = f"""
        {system_prompt_input}

        [COGNITIVE OPERATIVE CONSTRAINTS - ADAPT EXECUTIVE PATTERNS IMMEDIATELY]:
        - Formatting Style Mirror Profile: {behavior_metrics['style_alignment']}
        - Cognitive Granularity Baseline: {behavior_metrics['conceptual_depth']}
        - System Focus Vector: {', '.join(behavior_metrics['semantic_focus_vectors']) if behavior_metrics['semantic_focus_vectors'] else 'General Architectural Design Exploration'}

        Dynamically adjust your output structure, terminology, and information density to align perfectly with the target profile above.
        """

        prompt_blueprint = ChatPromptTemplate.from_messages([
            ("system", composite_agency_system_directive),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])

        execution_chain = prompt_blueprint | llm | StrOutputParser()

        with st.chat_message("assistant"):
            with st.spinner("Synchronizing Matrix Processing Pools..."):
                try:
                    computed_payload = execution_chain.invoke({
                        "history": active_history,
                        "question": user_query
                    })
                    st.markdown(computed_payload)

                    # store variables securely
                    save_log(st.session_state.active_user_id, "assistant", computed_payload)
                    update_profile(st.session_state.active_user_id, user_query)

                    # set a non-blocking state flag and run an isolated refresh
                    st.session_state.trigger_rerun = True
                    st.rerun()

                except Exception as compute_fault:
                    st.error(f"Computational flow pipeline exception: {str(compute_fault)}")
