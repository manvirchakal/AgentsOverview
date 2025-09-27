import os
import json
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from src.agents.workflows.book_state import CreatePrefaceState
from src.agents.nodes.create_preface import create_preface_node
from src.agents.nodes.create_chapter import create_chapter_node
from src.agents.edges.is_done import is_done

# Define the workflow for creating a book
def create_book_workflow() -> StateGraph[CreatePrefaceState]:
    workflow = StateGraph(CreatePrefaceState)
    workflow.add_node("preface_creation_node", create_preface_node)
    workflow.add_node("chapter_creation_node", create_chapter_node)
    workflow.add_edge(START, "preface_creation_node")
    workflow.add_edge("preface_creation_node", "chapter_creation_node")
    workflow.add_conditional_edges("chapter_creation_node", is_done)
    return workflow

def stream_workflow(
    book_title: str
):
    """
    Execute the book creation workflow with streaming output.
    
    Args:
        book_title: The title of the book to create
        
    Returns:
        Final state of the workflow after execution
    """
    llm = ChatOpenAI(model="gpt-4.1", temperature=0.7, streaming=True, api_key=os.getenv("OPENAI_API_KEY"))
    
    initial_state: CreatePrefaceState = {
        "book_title": book_title,
        "preface": "",
        "is_done": False,
        "chapters": [],
        "llm": llm,
        "messages": []
    }
    
    workflow = create_book_workflow()
    
    try:
        graph = workflow.compile()

        for event in graph.stream(initial_state, llm=llm):
            # Each event may be a mapping of keys to values. Convert each
            # value to a JSON-serializable string and format as an SSE data
            # chunk so FastAPI/Starlette can stream it safely.
            for value in event.values():
                # If it's already a string, use it; otherwise JSON-encode.
                if isinstance(value, (str, bytes)):
                    data_str = value if isinstance(value, str) else value.decode("utf-8", errors="ignore")
                    yield f"data: {data_str}\n\n"
                else:
                    try:
                        payload = json.dumps(value)
                    except Exception:
                        # Fallback to string representation if not JSON-serializable
                        payload = json.dumps({"value": str(value)})
                    yield f"data: {payload}\n\n"
    except Exception as e:
        # Yield an SSE error event instead of returning a dict (which would
        # cause Starlette to try to encode a dict with .encode and fail).
        err_msg = str(e)
        print(f"Error during workflow execution: {err_msg}")
        yield f"event: error\ndata: {json.dumps({'error': err_msg})}\n\n"
        return