import streamlit as st
from database import init_db
from todo_service import add_todo, update_todo, delete_todo, list_todos_structured
from agent import run_agent

st.set_page_config(
    page_title="Task Lingual",
    page_icon="✅",
    layout="wide",
)

init_db()

# --- Process pending mutations before any data fetch ---

if "pending_add" in st.session_state:
    p = st.session_state.pop("pending_add")
    add_todo(p["title"], p["description"], p["priority"])

if "pending_toggle" in st.session_state:
    p = st.session_state.pop("pending_toggle")
    update_todo(p["id"], status=p["status"])

if "pending_delete" in st.session_state:
    p = st.session_state.pop("pending_delete")
    delete_todo(p["id"])
    st.session_state.deleting_id = None

if "pending_update" in st.session_state:
    p = st.session_state.pop("pending_update")
    update_todo(p["id"], title=p.get("title"), description=p.get("description"),
                status=p.get("status"), priority=p.get("priority"))
    st.session_state.editing_id = None

if "pending_editing_id" in st.session_state:
    st.session_state.editing_id = st.session_state.pop("pending_editing_id")

if "pending_deleting_id" in st.session_state:
    st.session_state.deleting_id = st.session_state.pop("pending_deleting_id")

if "pending_cancel_edit" in st.session_state:
    st.session_state.pop("pending_cancel_edit")
    st.session_state.editing_id = None

if "pending_cancel_delete" in st.session_state:
    st.session_state.pop("pending_cancel_delete")
    st.session_state.deleting_id = None

if "pending_clear_ids" in st.session_state:
    st.session_state.pop("pending_clear_ids")
    existing_ids = {t["id"] for t in list_todos_structured()}
    if st.session_state.editing_id is not None and st.session_state.editing_id not in existing_ids:
        st.session_state.editing_id = None
    if st.session_state.deleting_id is not None and st.session_state.deleting_id not in existing_ids:
        st.session_state.deleting_id = None


# --- Session defaults ---

if "messages" not in st.session_state:
    st.session_state.messages = []
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
if "deleting_id" not in st.session_state:
    st.session_state.deleting_id = None


# --- Sidebar (data fetched after mutations processed) ---

with st.sidebar:
    st.title("🗣️ Task Lingual")
    st.markdown("Natural language powered todo management")
    st.divider()

    all_todos = list_todos_structured()
    total_count = len(all_todos)
    pending_count = len([t for t in all_todos if t["status"] == "pending"])
    in_progress_count = len([t for t in all_todos if t["status"] == "in_progress"])
    completed_count = len([t for t in all_todos if t["status"] == "completed"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", total_count)
    c2.metric("Pending", pending_count)
    c3.metric("Completed", completed_count)
    c4.metric("In Progress", in_progress_count)

    st.divider()
    st.caption("Built with LangChain + Groq + Streamlit")


# --- Tabs ---

tab1, tab2 = st.tabs(["🤖 AI Chat", "📋 Manage Todos"])


with tab1:
    st.header("🤖 AI Assistant")
    st.markdown("Chat with your AI assistant to manage todos using natural language.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("What would you like to do with your todos?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = run_agent(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


with tab2:
    st.header("Manage Your Todos")

    with st.expander("➕ Add New Todo", expanded=False):
        with st.form("add_todo_form", clear_on_submit=True):
            col_a1, col_a2 = st.columns([3, 1])
            with col_a1:
                add_title = st.text_input("Title", placeholder="What needs to be done?")
                add_desc = st.text_area("Description", placeholder="Optional details...")
            with col_a2:
                add_priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
                submitted = st.form_submit_button("Add Todo", use_container_width=True, type="primary")
            if submitted and add_title.strip():
                st.session_state.pending_add = {
                    "title": add_title.strip(),
                    "description": add_desc.strip(),
                    "priority": add_priority,
                }

    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    with col_f1:
        filter_status = st.selectbox(
            "Status",
            ["all", "pending", "in_progress", "completed"],
            format_func=lambda x: {
                "all": "All",
                "pending": "🟡 Pending",
                "in_progress": "🔵 In Progress",
                "completed": "🟢 Completed",
            }.get(x, x),
        )
    with col_f2:
        filter_priority = st.selectbox(
            "Priority",
            ["all", "low", "medium", "high"],
            format_func=lambda x: {
                "all": "All",
                "low": "🔽 Low",
                "medium": "➖ Medium",
                "high": "🔼 High",
            }.get(x, x),
        )
    with col_f3:
        search_query = st.text_input("🔍 Search", placeholder="Search by title...")

    st.divider()

    todos = list_todos_structured(status=filter_status, priority=filter_priority)
    if search_query:
        todos = [t for t in todos if search_query.lower() in t["title"].lower()]

    if not todos:
        st.info("No todos found. Add one above!")
    else:
        for todo in todos:
            is_editing = st.session_state.editing_id == todo["id"]
            is_deleting = st.session_state.deleting_id == todo["id"]

            with st.container(border=True):
                if is_editing:
                    with st.form(key=f"edit_form_{todo['id']}"):
                        e_title = st.text_input("Title", value=todo["title"])
                        e_desc = st.text_area("Description", value=todo["description"])
                        col_e1, col_e2 = st.columns(2)
                        with col_e1:
                            e_status = st.selectbox(
                                "Status",
                                ["pending", "in_progress", "completed"],
                                index=["pending", "in_progress", "completed"].index(todo["status"]),
                            )
                        with col_e2:
                            e_priority = st.selectbox(
                                "Priority",
                                ["low", "medium", "high"],
                                index=["low", "medium", "high"].index(todo["priority"]),
                            )
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            saved = st.form_submit_button("💾 Save", use_container_width=True, type="primary")
                        with col_cancel:
                            cancelled = st.form_submit_button("Cancel", use_container_width=True)
                        if saved:
                            st.session_state.pending_update = {
                                "id": todo["id"],
                                "title": e_title,
                                "description": e_desc,
                                "status": e_status,
                                "priority": e_priority,
                            }
                        if cancelled:
                            st.session_state.pending_cancel_edit = True
                else:
                    cols = st.columns([0.04, 0.35, 0.13, 0.1, 0.07, 0.07])

                    with cols[0]:
                        if todo["status"] == "completed":
                            if st.button("✅", key=f"uncheck_{todo['id']}", help="Mark as pending"):
                                st.session_state.pending_toggle = {"id": todo["id"], "status": "pending"}
                        else:
                            if st.button("⬜", key=f"check_{todo['id']}", help="Mark as completed"):
                                st.session_state.pending_toggle = {"id": todo["id"], "status": "completed"}

                    with cols[1]:
                        st.markdown(f"**{todo['title']}**")
                        if todo["description"]:
                            desc = todo["description"][:120]
                            if len(todo["description"]) > 120:
                                desc += "..."
                            st.caption(desc)

                    with cols[2]:
                        st.markdown(
                            {"pending": "🟡 Pending", "in_progress": "🔵 In Progress", "completed": "🟢 Completed"}.get(
                                todo["status"], todo["status"]
                            )
                        )

                    with cols[3]:
                        st.markdown(
                            {"low": "🔽 Low", "medium": "➖ Medium", "high": "🔼 High"}.get(
                                todo["priority"], todo["priority"]
                            )
                        )

                    with cols[4]:
                        if st.button("✏️", key=f"edit_{todo['id']}", help="Edit"):
                            st.session_state.pending_editing_id = todo["id"]

                    with cols[5]:
                        if is_deleting:
                            if st.button("✅", key=f"confirm_del_{todo['id']}", help="Confirm delete"):
                                st.session_state.pending_delete = {"id": todo["id"]}
                        else:
                            if st.button("🗑️", key=f"del_{todo['id']}", help="Delete"):
                                st.session_state.pending_deleting_id = todo["id"]

                if is_deleting and not is_editing:
                    _, _, col_cancel_del, _ = st.columns([0.04, 0.35, 0.3, 0.27])
                    with col_cancel_del:
                        if st.button("❌ Cancel delete", key=f"cancel_del_{todo['id']}"):
                            st.session_state.pending_cancel_delete = True

                st.caption(f"ID: {todo['id']} — Created: {todo['created_at'][:10] if todo['created_at'] else 'N/A'}")
