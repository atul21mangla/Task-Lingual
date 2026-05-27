from datetime import datetime
from typing import List, Optional
from database import SessionLocal, Todo

def add_todo(title: str, description: str = "", priority: str = "medium") -> str:
    """Adds a new Todo item to the database."""
    session = SessionLocal()
    try:
        new_todo = Todo(title=title, description=description, priority=priority)
        session.add(new_todo)
        session.commit()       # committing the changes 
        session.refresh(new_todo)  # refreshing the new todo 
        return f"Successfully created Todo [ID: {new_todo.id}] Title: '{new_todo.title}' | Priority: {new_todo.priority}"
    except Exception as e:
        session.rollback()
        return f"Error adding todo: {str(e)}"
    finally:
        session.close()

def list_todos(status: str = "all", priority: str = "all") -> str:
    """Lists all Todo items from the database."""
    session = SessionLocal()
    try:
        query = session.query(Todo)
        if status != "all":
            query = query.filter(Todo.status == status)
            
        if priority != "all":
            query = query.filter(Todo.priority == priority)

        todos = query.order_by(Todo.created_at.desc()).all()
        if not todos:
            return "No todos found."
        
        result = []
        for todo in todos:
            status = todo.status.capitalize()  # capitalize the first letter of the status
            priority = todo.priority.capitalize()  # capitalize the first letter of the priority
            desc_str = f" - {todo.description}" if todo.description else ""
            result.append(f"# ID: {todo.id} ||| Title: {todo.title} ||| Status: {status} ||| Priority: {priority} ||| Description: {desc_str}")
        return "\n".join(result)
    except Exception as e:
        return f"Error listing todos: {str(e)}"
    finally:
        session.close()

def update_todo(
    todo_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    status: Optional[str] = None, 
    priority: Optional[str] = None
) -> str:

    """Updates an existing Todo item by its ID. Can set a new title, description, or change completion status."""
    session = SessionLocal()
    try:
        todo = session.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return f"Todo with ID {todo_id} not found."
        
        updated_fields = []
        if title is not None:
            todo.title = title
            updated_fields.append("title")
        if description is not None:
            todo.description = description
            updated_fields.append("description")
        if priority is not None:
            todo.priority = priority
            updated_fields.append("priority")
        if status is not None:
            todo.status = status
            updated_fields.append("status")
        
        if not updated_fields:
            return f"No update parameters specified for Todo #{todo_id}."
        
        session.commit()
        session.refresh(todo)
        status_text = todo.status.capitalize()
        priority_text = todo.priority.capitalize()
        
        return f"Updated Todo #{todo.id} ({', '.join(updated_fields)}). Current status: {status_text}. Current priority: {priority_text}."
    except Exception as e:
        session.rollback()
        return f"Error updating todo: {str(e)}"
    finally:
        session.close()

def delete_todo(todo_id: int) -> str:
    """Deletes a Todo item from the database by its ID."""
    session = SessionLocal()
    try:
        todo = session.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return f"Todo with ID {todo_id} not found."
        
        session.delete(todo)
        session.commit()
        return f"Successfully deleted Todo #{todo_id}: '{todo.title}'"
    except Exception as e:
        session.rollback()
        return f"Error deleting todo: {str(e)}"
    finally:
        session.close()

def search_todos_by_title(title_query: str) -> List[dict]:
    """Helper function to find todos matching a partial title (useful for lookup by name)."""
    session = SessionLocal()
    try:
        todos = session.query(Todo).filter(Todo.title.like(f"%{title_query}%")).all()
        return [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority} for t in todos]
    finally:
        session.close()


def list_todos_structured(status: str = "all", priority: str = "all") -> List[dict]:
    """Returns structured list of todo dicts with all fields for the Streamlit UI."""
    session = SessionLocal()
    try:
        query = session.query(Todo)
        if status != "all":
            query = query.filter(Todo.status == status)
        if priority != "all":
            query = query.filter(Todo.priority == priority)
        todos = query.order_by(Todo.created_at.desc()).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "priority": t.priority,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in todos
        ]
    finally:
        session.close()
