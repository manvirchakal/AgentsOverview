from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models.openai import ChatOpenAI
from src.agents.workflows.book_state import CreatePrefaceState
import operator


def create_preface_node(state: CreatePrefaceState, llm: ChatOpenAI) -> CreatePrefaceState:
    """
    LangGraph node that generates a preface for a book based on its title.
    
    Args:
        state: The current state containing book title and messages
        llm: The language model to use for generating the preface
        
    Returns:
        Updated state with the generated preface
    """
    book_title = state.get("book_title", "")
    
    if not book_title:
        error_msg = "No book title provided. Please provide a book title to generate a preface."
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=error_msg)],
            "preface": ""
        }
    
    # Create the prompt for generating a preface
    preface_prompt = f"""
    Write a compelling and thoughtful preface for a book titled "{book_title}".
    
    The preface should:
    - Be approximately 200-400 words
    - Introduce the main themes or subject matter
    - Explain why this book is important or relevant
    - Connect with the reader on a personal level
    - Set appropriate expectations for what the reader will discover
    
    Write in a warm, engaging tone that would appeal to the book's intended audience.
    """
    
    try:
        # Generate the preface using the LLM
        response = llm.invoke([HumanMessage(content=preface_prompt)])
        generated_preface = response.content
        
        success_msg = f"Successfully generated preface for '{book_title}'"
        
        return {
            **state,
            "messages": state["messages"] + [
                HumanMessage(content=f"Generate preface for: {book_title}"),
                AIMessage(content=success_msg)
            ],
            "preface": generated_preface
        }
        
    except Exception as e:
        error_msg = f"Error generating preface: {str(e)}"
        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=error_msg)],
            "preface": ""
        }