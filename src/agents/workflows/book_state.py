from typing import TypedDict

class CreatePrefaceState(TypedDict):
    """State for the create preface node."""
    book_title: str = ""
    preface: str = ""
    is_done: bool = False
    chapters: list[str] = []