from langchain_community.chat_models.openai import ChatOpenAI
from agents.workflows.book_state import CreatePrefaceState
from agents.nodes.create_preface import create_preface_node

# Example usage function
def create_preface_workflow_node(llm: ChatOpenAI):
    """
    Factory function to create a preface node with a specific LLM.
    
    Args:
        llm: The language model to use
        
    Returns:
        A configured preface node function
    """
    def node(state: CreatePrefaceState) -> CreatePrefaceState:
        return create_preface_node(state, llm)
    return node