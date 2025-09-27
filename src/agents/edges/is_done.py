from src.agents.workflows.book_state import CreatePrefaceState
from langgraph.graph import END

def is_done(state: CreatePrefaceState):
    """
    Edge function to determine if the book creation process is done.
    
    Args:
        state: The current state containing book title, preface, chapters, and is_done flag

    Returns:
        [END, "chapter_creation_node"] if the process is done, otherwise continue
    """
    if state.get("is_done"):
        return END
    return "chapter_creation_node"