"""
Simple example of using the Cognitive Tools system.

This script demonstrates how to solve a math problem using both
the cognitive tools approach and a baseline approach.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.agents import CognitiveAgent


def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    
    # Create cognitive agent
    agent = CognitiveAgent(llm)
    
    # Example problem
    problem = "Find the greatest common divisor (GCD) of 48 and 18."
    
    print("="*60)
    print("Cognitive Tools Example")
    print("="*60)
    print(f"Problem: {problem}\n")
    
    # Solve with cognitive tools
    print("Solving with Cognitive Tools...")
    result = agent.solve(problem, max_iterations=5)
    
    print(f"\nFinal answer: {result.get('final_answer')}")
    print(f"Iterations used: {result.get('iterations')}")
    print(f"Tools used: {len(result.get('tool_usage', []))}")
    
    print("\nTool sequence:")
    for tool in result.get('tool_usage', []):
        print(f"  - {tool['tool']}")


if __name__ == "__main__":
    main()