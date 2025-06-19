"""Run cognitive tools experiment."""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.agents import CognitiveAgent
from experiments.evaluation import Evaluator, ExperimentResults


class ExperimentRunner:
    """Runs experiments comparing cognitive tools vs baseline."""
    
    def __init__(self, model_name: str = "gpt-4"):
        """Initialize experiment runner.
        
        Args:
            model_name: Name of the model to use (gpt-4, claude-3, etc.)
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize LLM
        self.llm = self._create_llm(model_name)
        self.model_name = model_name
        
        # Initialize agent and evaluator
        self.agent = CognitiveAgent(self.llm)
        self.evaluator = Evaluator()
        
        # Set up directories
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
    
    def _create_llm(self, model_name: str):
        """Create LLM based on model name."""
        if model_name.startswith("gpt"):
            return ChatOpenAI(
                model=model_name,
                temperature=0.1,
                max_tokens=2000
            )
        elif model_name.startswith("claude"):
            return ChatAnthropic(
                model=model_name,
                temperature=0.1,
                max_tokens=2000
            )
        else:
            raise ValueError(f"Unknown model: {model_name}")
    
    def load_problems(self, dataset_path: str) -> List[Dict]:
        """Load problems from JSON file."""
        with open(dataset_path, 'r') as f:
            data = json.load(f)
        return data["problems"]
    
    def run_cognitive_tools_experiment(
        self,
        problems: List[Dict],
        max_iterations: int = 10
    ) -> ExperimentResults:
        """Run experiment with cognitive tools."""
        print("\n=== Running Cognitive Tools Experiment ===")
        
        solutions = []
        for problem in tqdm(problems, desc="Solving problems"):
            try:
                solution = self.agent.solve(
                    problem["question"],
                    max_iterations=max_iterations
                )
                solutions.append(solution)
            except Exception as e:
                print(f"Error solving {problem['id']}: {e}")
                solutions.append({
                    "problem": problem["question"],
                    "final_answer": None,
                    "reasoning_trace": f"Error: {str(e)}",
                    "tool_usage": [],
                    "iterations": 0,
                    "error": str(e)
                })
        
        # Evaluate results
        results = self.evaluator.evaluate_experiment(problems, solutions)
        return results
    
    def run_baseline_experiment(
        self,
        problems: List[Dict]
    ) -> ExperimentResults:
        """Run baseline experiment (direct prompting without tools)."""
        print("\n=== Running Baseline Experiment ===")
        
        solutions = []
        for problem in tqdm(problems, desc="Solving problems"):
            try:
                # Simple CoT prompt
                prompt = f"""Solve this step by step:

{problem["question"]}

Think through this carefully and show your work. When you have the final answer, write "ANSWER: [your answer]"."""
                
                response = self.llm.invoke(prompt)
                answer_text = response.content if hasattr(response, 'content') else str(response)
                
                # Extract answer
                import re
                match = re.search(r'ANSWER:\s*(.+?)(?:\n|$)', answer_text, re.IGNORECASE)
                final_answer = match.group(1).strip() if match else None
                
                solutions.append({
                    "problem": problem["question"],
                    "final_answer": final_answer,
                    "reasoning_trace": answer_text,
                    "tool_usage": [],
                    "iterations": 1
                })
            except Exception as e:
                print(f"Error solving {problem['id']}: {e}")
                solutions.append({
                    "problem": problem["question"],
                    "final_answer": None,
                    "reasoning_trace": f"Error: {str(e)}",
                    "tool_usage": [],
                    "iterations": 0,
                    "error": str(e)
                })
        
        # Evaluate results
        results = self.evaluator.evaluate_experiment(problems, solutions)
        return results
    
    def save_results(self, results: Dict[str, ExperimentResults], timestamp: str):
        """Save experiment results."""
        # Save raw results
        results_data = {
            name: result.to_dict()
            for name, result in results.items()
        }
        
        with open(self.results_dir / f"results_{timestamp}.json", 'w') as f:
            json.dump(results_data, f, indent=2)
    
    def generate_report(
        self,
        results: Dict[str, ExperimentResults],
        timestamp: str
    ):
        """Generate experiment report."""
        report_path = self.results_dir / f"report_{timestamp}.md"
        
        with open(report_path, 'w') as f:
            f.write("# Cognitive Tools Experiment Report\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Model**: {self.model_name}\n\n")
            
            # Overall results
            f.write("## Overall Results\n\n")
            f.write("| Method | Accuracy | Correct/Total |\n")
            f.write("|--------|----------|---------------|\n")
            
            for name, result in results.items():
                f.write(f"| {name} | {result.accuracy:.2%} | {result.correct_count}/{result.total_problems} |\n")
            
            f.write("\n")
            
            # Results by problem type
            f.write("## Results by Problem Type\n\n")
            
            for name, result in results.items():
                f.write(f"### {name}\n\n")
                f.write("| Problem Type | Accuracy | Correct/Total |\n")
                f.write("|--------------|----------|---------------|\n")
                
                for prob_type, stats in result.results_by_type.items():
                    f.write(f"| {prob_type} | {stats['accuracy']:.2%} | {stats['correct']}/{stats['total']} |\n")
                
                f.write("\n")
            
            # Tool usage statistics (for cognitive tools)
            if "Cognitive Tools" in results:
                f.write("## Tool Usage Statistics\n\n")
                f.write("| Tool | Usage Count |\n")
                f.write("|------|-------------|\n")
                
                tool_stats = results["Cognitive Tools"].tool_usage_stats
                for tool, count in sorted(tool_stats.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"| {tool} | {count} |\n")
                
                f.write(f"\n**Average iterations per problem**: {results['Cognitive Tools'].average_iterations:.2f}\n\n")
            
            # Detailed problem analysis
            f.write("## Detailed Problem Analysis\n\n")
            
            # Find problems where cognitive tools succeeded but baseline failed
            if "Cognitive Tools" in results and "Baseline" in results:
                ct_results = {r.problem_id: r for r in results["Cognitive Tools"].detailed_results}
                bl_results = {r.problem_id: r for r in results["Baseline"].detailed_results}
                
                f.write("### Problems Where Cognitive Tools Outperformed Baseline\n\n")
                
                for prob_id, ct_result in ct_results.items():
                    bl_result = bl_results.get(prob_id)
                    if ct_result.is_correct and bl_result and not bl_result.is_correct:
                        f.write(f"**Problem {prob_id}** ({ct_result.problem_type})\n")
                        f.write(f"- Expected: {ct_result.expected_answer}\n")
                        f.write(f"- Cognitive Tools: ✓ {ct_result.predicted_answer}\n")
                        f.write(f"- Baseline: ✗ {bl_result.predicted_answer}\n")
                        f.write(f"- Tools used: {', '.join(t['tool'] for t in ct_result.tool_usage)}\n\n")
        
        print(f"\nReport saved to: {report_path}")
    
    def plot_results(self, results: Dict[str, ExperimentResults], timestamp: str):
        """Create visualization plots."""
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Overall accuracy comparison
        ax = axes[0, 0]
        methods = list(results.keys())
        accuracies = [r.accuracy for r in results.values()]
        ax.bar(methods, accuracies)
        ax.set_ylim(0, 1.0)
        ax.set_ylabel('Accuracy')
        ax.set_title('Overall Accuracy Comparison')
        for i, v in enumerate(accuracies):
            ax.text(i, v + 0.01, f'{v:.2%}', ha='center')
        
        # 2. Accuracy by problem type
        ax = axes[0, 1]
        problem_types = set()
        for result in results.values():
            problem_types.update(result.results_by_type.keys())
        problem_types = sorted(list(problem_types))
        
        x = range(len(problem_types))
        width = 0.35
        
        for i, (name, result) in enumerate(results.items()):
            accuracies = [
                result.results_by_type.get(pt, {"accuracy": 0})["accuracy"]
                for pt in problem_types
            ]
            offset = width * (i - 0.5)
            ax.bar([xi + offset for xi in x], accuracies, width, label=name)
        
        ax.set_xlabel('Problem Type')
        ax.set_ylabel('Accuracy')
        ax.set_title('Accuracy by Problem Type')
        ax.set_xticks(x)
        ax.set_xticklabels(problem_types, rotation=45)
        ax.legend()
        
        # 3. Tool usage distribution (if cognitive tools used)
        if "Cognitive Tools" in results:
            ax = axes[1, 0]
            tool_stats = results["Cognitive Tools"].tool_usage_stats
            if tool_stats:
                tools = list(tool_stats.keys())
                counts = list(tool_stats.values())
                ax.pie(counts, labels=tools, autopct='%1.1f%%')
                ax.set_title('Tool Usage Distribution')
            else:
                ax.text(0.5, 0.5, 'No tools used', ha='center', va='center')
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
        
        # 4. Success rate by iterations (if cognitive tools used)
        if "Cognitive Tools" in results:
            ax = axes[1, 1]
            ct_results = results["Cognitive Tools"].detailed_results
            iterations = [r.iterations for r in ct_results]
            success = [r.is_correct for r in ct_results]
            
            if iterations:
                # Group by iteration count
                iter_success = {}
                for it, succ in zip(iterations, success):
                    if it not in iter_success:
                        iter_success[it] = {"success": 0, "total": 0}
                    iter_success[it]["total"] += 1
                    if succ:
                        iter_success[it]["success"] += 1
                
                iter_counts = sorted(iter_success.keys())
                success_rates = [
                    iter_success[it]["success"] / iter_success[it]["total"]
                    for it in iter_counts
                ]
                
                ax.plot(iter_counts, success_rates, 'o-')
                ax.set_xlabel('Number of Iterations')
                ax.set_ylabel('Success Rate')
                ax.set_title('Success Rate vs Iterations')
                ax.set_ylim(0, 1.0)
        
        plt.tight_layout()
        plt.savefig(self.results_dir / f"results_plot_{timestamp}.png", dpi=150)
        print(f"Plot saved to: {self.results_dir / f'results_plot_{timestamp}.png'}")
    
    def run_full_experiment(self, dataset_path: str):
        """Run full experiment comparing cognitive tools vs baseline."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load problems
        problems = self.load_problems(dataset_path)
        print(f"Loaded {len(problems)} problems")
        
        # Run experiments
        results = {}
        
        # Cognitive tools experiment
        results["Cognitive Tools"] = self.run_cognitive_tools_experiment(problems)
        
        # Baseline experiment
        results["Baseline"] = self.run_baseline_experiment(problems)
        
        # Save results
        self.save_results(results, timestamp)
        
        # Generate report
        self.generate_report(results, timestamp)
        
        # Create plots
        self.plot_results(results, timestamp)
        
        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run cognitive tools experiment")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4",
        help="Model to use (gpt-4, gpt-3.5-turbo, claude-3-opus, etc.)"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="experiments/datasets/math_problems.json",
        help="Path to dataset JSON file"
    )
    
    args = parser.parse_args()
    
    # Run experiment
    runner = ExperimentRunner(model_name=args.model)
    results = runner.run_full_experiment(args.dataset)
    
    # Print summary
    print("\n=== Experiment Summary ===")
    for name, result in results.items():
        print(f"{name}: {result.accuracy:.2%} ({result.correct_count}/{result.total_problems})")


if __name__ == "__main__":
    main()