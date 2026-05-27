from typing import Optional
from langchain_core.tools import tool
import todo_service


@tool
def add_todo_tool(title: str, description: str = "", priority: str = "medium") -> str:
    """Add a new todo item. Use this tool when the user wants to create, add, or insert a new todo/task.

    Args:
        title: Short title fpr the task (Required)
        description: Description of the task (Optional)
        priority: 'low', 'medium', 'high' (default = medium)
    """
    return todo_service.add_todo(title, description, priority)

@tool
def list_todos_tool(status: str = "all", priority: str = "all") -> str:
    """List todo items. Use this tool when the user wants to see, list, show, or check their todos or tasks.
    Optionally filter by status or priority.

    Args:
        status: 'pending', 'in_progress', 'completed', 'all' (default = 'all')
        priority: 'low', 'medium', 'high', 'all' (default = 'all')
    """
    return todo_service.list_todos(status, priority)

@tool
def search_todos_by_title_tool(title_query: str) -> str:
    """Search for todos by a search query on the title. Use this tool when the user refers to a task by name/text
    (e.g., 'mark buy milk as completed' or 'delete the task write code') instead of an ID, so you can find its ID first.
    Returns a list of matching tasks and their IDs.
    """
    matches = todo_service.search_todos_by_title(title_query)
    if not matches:
        return f"No todos found matching '{title_query}'."
    return "\n".join([f"ID {m['id']}: '{m['title']}' (Status: {m['status']})" for m in matches])

@tool
def update_todo_tool(
    todo_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    status: Optional[str] = None, 
    priority: Optional[str] = None) -> str:

    """Update an existing todo item by its ID. Use this tool when the user wants to modify, edit, mark as completed,
    mark as incomplete, or update a specific todo item.
    Ensure you have the exact todo_id (if they refer to it by name, search/look up the ID first using search_todos_by_title_tool).

    Args:
        todo_id: The ID of the todo item to update (Required)
        title: New title for the todo item (Optional)
        description: New description for the todo item (Optional)
        status: 'pending', 'in_progress', 'completed' (Optional)
        priority: 'low', 'medium', 'high' (Optional)
    """
    return todo_service.update_todo(todo_id, title, description, status, priority)

@tool
def delete_todo_tool(todo_id: int) -> str:
    """Delete an existing todo item by its ID. Use this tool when the user wants to delete, remove, or clear a task.
    Ensure you have the exact todo_id (if they refer to it by name, search/look up the ID first using search_todos_by_title_tool).
    """
    return todo_service.delete_todo(todo_id)



# Bind the tools to the LLM
all_tools = [add_todo_tool, list_todos_tool, search_todos_by_title_tool, update_todo_tool, delete_todo_tool]



