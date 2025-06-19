"""State definition for the cognitive reasoning graph."""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import MessagesState


class CognitiveReasoningState(MessagesState):
    """State for the cognitive reasoning process."""
    
    # Problem and solution tracking
    problem: str
    current_reasoning: str
    final_answer: Optional[str]
    
    # Tool usage tracking
    tool_calls: List[Dict[str, Any]]
    tool_outputs: List[str]
    
    # Iteration control
    iteration: int
    max_iterations: int
    
    # Solution verification
    solution_verified: bool
    verification_result: Optional[str]
    
    # Error tracking
    errors: List[str]
    needs_backtracking: bool