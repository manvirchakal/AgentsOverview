from typing import TypedDict
from langchain_openai import ChatOpenAI

class CreatePrefaceState(TypedDict):
    """State for the create preface node."""
    messages: list
    book_title: str
    preface: str = ""
    is_done: bool = False
    chapters: list[str] = []
    llm: ChatOpenAI