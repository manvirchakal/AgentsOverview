from src.agents.workflows.book_state import CreatePrefaceState
from langgraph import END

def is_done(state: CreatePrefaceState) -> [END, "chapter_creation_node"]:
    """
    Edge function to determine if the book creation process is done.
    
    Args:
        state: The current state containing book title, preface, chapters, and is_done flag