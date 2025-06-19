"""Cognitive Agent that uses the reasoning graph."""

from typing import Dict, Optional
from langchain_core.language_models import BaseLanguageModel

from ..graphs.reasoning_graph import CognitiveReasoningGraph


class CognitiveAgent:
    """Agent that solves problems using cognitive tools."""
    
    def __init__(self, llm: BaseLanguageModel):
        """Initialize the cognitive agent.
        
        Args:
            llm: Language model to use for reasoning
        """
        self.llm = llm
        self.graph = CognitiveReasoningGraph(llm)
    
    def solve(self, problem: str, max_iterations: int = 10) -> Dict:
        """Solve a problem using cognitive tools.
        
        Args:
            problem: The problem to solve
            max_iterations: Maximum number of reasoning iterations
            
        Returns:
            Dictionary containing:
                - problem: The original problem
                - final_answer: The extracted answer
                - reasoning_trace: Full reasoning process
                - tool_usage: List of tools used
                - iterations: Number of iterations taken
        """
        return self.graph.solve(problem, max_iterations)
    
    def solve_batch(self, problems: list[str], max_iterations: int = 10) -> list[Dict]:
        """Solve multiple problems.
        
        Args:
            problems: List of problems to solve
            max_iterations: Maximum iterations per problem
            
        Returns:
            List of solution dictionaries
        """
        results = []
        for problem in problems:
            try:
                result = self.solve(problem, max_iterations)
                results.append(result)
            except Exception as e:
                results.append({
                    "problem": problem,
                    "final_answer": None,
                    "reasoning_trace": f"Error: {str(e)}",
                    "tool_usage": [],
                    "iterations": 0,
                    "error": str(e)
                })
        return results