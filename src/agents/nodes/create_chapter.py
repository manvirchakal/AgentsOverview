from src.agents.workflows.book_state import CreatePrefaceState
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel
from typing import Optional


class ChapterResponseStructure(BaseModel):
    chapter_number: int
    chapter_content: str
    is_done: bool
    num_pages: Optional[int]


def create_chapter_node(state: CreatePrefaceState) -> CreatePrefaceState:
    """
    Node that generates a chapter for a book based on its title and preface.
    
    Args:
        state: The current state containing book title, preface, and chapters
        llm: The language model to use for generating the chapter
        
    Returns:
        Updated state with the generated chapter
    """
    book_title = state.get("book_title", "")
    preface = state.get("preface", "")
    
    if not book_title or not preface:
        error_msg = "Book title or preface missing. Please provide both to generate a chapter."
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=error_msg)],
            "chapters": state.get("chapters", [])
        }
    
    chapters = state.get("chapters", [])

    # Create the prompt for generating a chapter
    previous_chapters_str = "; ".join(map(str, chapters)) if chapters else "None"
    chapter_prompt = f"""
    Write the following chapter for a book titled "{book_title}" with the given preface and previous chapters:

    Preface: {preface}

    Previous Chapters: {previous_chapters_str}

    I need the book to have 10-15 chapters
    """

    llm = state.get("llm")

    try:
        resp = llm.with_structured_output(ChapterResponseStructure).invoke(
            [HumanMessage(content=chapter_prompt)]
        )

        chapter_number = resp.chapter_number
        chapter_content = resp.chapter_content
        num_pages = resp.num_pages
        is_done = resp.is_done
        state["is_done"] = is_done
        chapter = f"Chapter {chapter_number}:\n\n {chapter_content} \n({num_pages} pages)"
        chapters = state.get("chapters", [])
        chapters.append(chapter)
        state["chapters"] = chapters

        # Update the state with the new chapter information
        # Keep `chapters` as a list[str] only to avoid type issues on subsequent joins
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content="Chapter created successfully.")],
            "chapters": state.get("chapters", [])
        }
    except Exception as e:
        error_msg = f"Error occurred while creating chapter: {e}"
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=error_msg)],
            "chapters": state.get("chapters", [])
        }