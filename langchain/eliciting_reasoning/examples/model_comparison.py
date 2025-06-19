"""
Compare different models on the cognitive tools approach.

This script runs a single problem across multiple models to compare
their performance with cognitive tools vs baseline approaches.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.agents import CognitiveAgent


def extract_baseline_answer(text: str) -> str:
    """Extract answer from baseline response."""
    match = re.search(r'ANSWER:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
    return match.group(1).strip() if match else "No answer found"


def test_model(model_name: str, llm: Any, problem: str, expected_answer: str) -> Dict[str, Any]:
    """Test a model with both cognitive tools and baseline approach."""
    print(f"\n{model_name}:")
    print("-" * 30)
    
    # Test with cognitive tools
    agent = CognitiveAgent(llm)
    ct_result = agent.solve(problem, max_iterations=5)
    
    ct_answer = ct_result.get('final_answer', 'No answer')
    ct_correct = str(ct_answer).strip() == str(expected_answer).strip()
    
    print(f"Cognitive Tools answer: {ct_answer} {'✓' if ct_correct else '✗'}")
    print(f"  Iterations: {ct_result.get('iterations')}")
    print(f"  Tools used: {[t['tool'] for t in ct_result.get('tool_usage', [])]}")
    
    # Test baseline
    baseline_prompt = f"""Solve this step by step:

{problem}

Think through this carefully and show your work. 
When you have the final answer, write "ANSWER: [your answer]"."""
    
    baseline_response = llm.invoke(baseline_prompt)
    baseline_text = baseline_response.content if hasattr(baseline_response, 'content') else str(baseline_response)
    baseline_answer = extract_baseline_answer(baseline_text)
    baseline_correct = baseline_answer.strip() == str(expected_answer).strip()
    
    print(f"Baseline answer: {baseline_answer} {'✓' if baseline_correct else '✗'}")
    
    return {
        "cognitive_tools": {"answer": ct_answer, "correct": ct_correct},
        "baseline": {"answer": baseline_answer, "correct": baseline_correct}
    }


def main():
    # Load environment variables
    load_dotenv()
    
    # Define test problem
    problem = "Find the sum of all positive divisors of 720."
    expected_answer = "2418"
    
    # Initialize models
    models = {
        "GPT-4": ChatOpenAI(model="gpt-4", temperature=0.1),
        "GPT-3.5-turbo": ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1),
    }
    
    # Add Claude if API key is available
    if os.getenv("ANTHROPIC_API_KEY"):
        models["Claude-3.5"] = ChatAnthropic(
            model="claude-3-5-sonnet-20241022", 
            temperature=0.1
        )
    
    print("="*60)
    print("Model Comparison: Cognitive Tools vs Baseline")
    print("="*60)
    print(f"Problem: {problem}")
    print(f"Expected answer: {expected_answer}")
    print("="*60)
    
    # Test each model
    results = {}
    for model_name, llm in models.items():
        results[model_name] = test_model(model_name, llm, problem, expected_answer)
    
    # Summary
    print("\n" + "="*60)
    print("Summary:")
    print("-"*60)
    print("Model           | Cognitive Tools | Baseline")
    print("-"*60)
    
    for model_name, result in results.items():
        ct_status = "✓" if result["cognitive_tools"]["correct"] else "✗"
        bl_status = "✓" if result["baseline"]["correct"] else "✗"
        print(f"{model_name:<15} | {ct_status:<15} | {bl_status}")


if __name__ == "__main__":
    main()