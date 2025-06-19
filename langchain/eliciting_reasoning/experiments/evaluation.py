"""Evaluation framework for cognitive tools experiment."""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np


@dataclass
class EvaluationResult:
    """Result of evaluating a single problem."""
    problem_id: str
    problem_type: str
    is_correct: bool
    predicted_answer: Optional[str]
    expected_answer: str
    reasoning_trace: str
    tool_usage: List[Dict]
    iterations: int
    error: Optional[str] = None


@dataclass
class ExperimentResults:
    """Results of an entire experiment run."""
    total_problems: int
    correct_count: int
    accuracy: float
    results_by_type: Dict[str, Dict]
    tool_usage_stats: Dict[str, int]
    average_iterations: float
    detailed_results: List[EvaluationResult]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_problems": self.total_problems,
            "correct_count": self.correct_count,
            "accuracy": self.accuracy,
            "results_by_type": self.results_by_type,
            "tool_usage_stats": self.tool_usage_stats,
            "average_iterations": self.average_iterations,
            "detailed_results": [
                {
                    "problem_id": r.problem_id,
                    "problem_type": r.problem_type,
                    "is_correct": r.is_correct,
                    "predicted_answer": r.predicted_answer,
                    "expected_answer": r.expected_answer,
                    "tool_usage": r.tool_usage,
                    "iterations": r.iterations,
                    "error": r.error
                }
                for r in self.detailed_results
            ]
        }


class Evaluator:
    """Evaluates problem-solving performance."""
    
    def __init__(self):
        self.normalizers = {
            "number": self._normalize_number,
            "expression": self._normalize_expression,
            "interval": self._normalize_interval,
            "set": self._normalize_set
        }
    
    def evaluate_solution(
        self, 
        problem: Dict,
        solution: Dict
    ) -> EvaluationResult:
        """Evaluate a single solution against expected answer."""
        predicted = solution.get("final_answer")
        expected = problem["answer"]
        
        # Check for errors
        if solution.get("error"):
            return EvaluationResult(
                problem_id=problem["id"],
                problem_type=problem["type"],
                is_correct=False,
                predicted_answer=None,
                expected_answer=expected,
                reasoning_trace=solution.get("reasoning_trace", ""),
                tool_usage=solution.get("tool_usage", []),
                iterations=solution.get("iterations", 0),
                error=solution["error"]
            )
        
        # Check if answer exists
        if not predicted:
            is_correct = False
        else:
            # Determine answer type and normalize
            is_correct = self._check_answer(predicted, expected, problem["type"])
        
        return EvaluationResult(
            problem_id=problem["id"],
            problem_type=problem["type"],
            is_correct=is_correct,
            predicted_answer=predicted,
            expected_answer=expected,
            reasoning_trace=solution.get("reasoning_trace", ""),
            tool_usage=solution.get("tool_usage", []),
            iterations=solution.get("iterations", 0)
        )
    
    def evaluate_experiment(
        self,
        problems: List[Dict],
        solutions: List[Dict]
    ) -> ExperimentResults:
        """Evaluate an entire experiment run."""
        results = []
        
        # Evaluate each problem
        for problem, solution in zip(problems, solutions):
            result = self.evaluate_solution(problem, solution)
            results.append(result)
        
        # Calculate statistics
        total = len(results)
        correct = sum(1 for r in results if r.is_correct)
        accuracy = correct / total if total > 0 else 0
        
        # Results by problem type
        results_by_type = defaultdict(lambda: {"total": 0, "correct": 0})
        for result in results:
            results_by_type[result.problem_type]["total"] += 1
            if result.is_correct:
                results_by_type[result.problem_type]["correct"] += 1
        
        # Calculate accuracy by type
        for type_name, counts in results_by_type.items():
            counts["accuracy"] = counts["correct"] / counts["total"] if counts["total"] > 0 else 0
        
        # Tool usage statistics
        tool_usage_stats = defaultdict(int)
        for result in results:
            for tool_call in result.tool_usage:
                tool_usage_stats[tool_call["tool"]] += 1
        
        # Average iterations
        iterations = [r.iterations for r in results if r.iterations > 0]
        avg_iterations = np.mean(iterations) if iterations else 0
        
        return ExperimentResults(
            total_problems=total,
            correct_count=correct,
            accuracy=accuracy,
            results_by_type=dict(results_by_type),
            tool_usage_stats=dict(tool_usage_stats),
            average_iterations=avg_iterations,
            detailed_results=results
        )
    
    def _check_answer(self, predicted: str, expected: str, problem_type: str) -> bool:
        """Check if predicted answer matches expected answer."""
        # Normalize both answers
        pred_norm = self._normalize_answer(predicted)
        exp_norm = self._normalize_answer(expected)
        
        # Direct string comparison
        if pred_norm == exp_norm:
            return True
        
        # Try numeric comparison
        try:
            pred_num = self._extract_number(pred_norm)
            exp_num = self._extract_number(exp_norm)
            if pred_num is not None and exp_num is not None:
                return abs(pred_num - exp_num) < 1e-6
        except:
            pass
        
        # Try set/interval comparison for certain problem types
        if problem_type in ["algebra", "inequality"]:
            return self._compare_algebraic_answers(predicted, expected)
        
        return False
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize answer string for comparison."""
        # Convert to lowercase and strip whitespace
        answer = answer.lower().strip()
        
        # Remove common prefixes
        prefixes = ["answer:", "the answer is", "final answer:"]
        for prefix in prefixes:
            if answer.startswith(prefix):
                answer = answer[len(prefix):].strip()
        
        # Normalize mathematical notation
        answer = answer.replace("×", "*").replace("÷", "/")
        answer = answer.replace("^", "**")
        
        return answer
    
    def _extract_number(self, text: str) -> Optional[float]:
        """Extract a number from text."""
        # Try to find a number pattern
        patterns = [
            r"[-+]?\d*\.?\d+",  # Regular number
            r"[-+]?\d+/\d+",    # Fraction
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num_str = match.group()
                try:
                    # Handle fractions
                    if "/" in num_str:
                        num, denom = num_str.split("/")
                        return float(num) / float(denom)
                    return float(num_str)
                except:
                    continue
        
        return None
    
    def _normalize_number(self, text: str) -> Optional[float]:
        """Normalize a numeric answer."""
        return self._extract_number(text)
    
    def _normalize_expression(self, text: str) -> str:
        """Normalize an algebraic expression."""
        # Remove spaces and lowercase
        text = text.replace(" ", "").lower()
        # Sort terms if it's a sum
        if "+" in text or "-" in text:
            # Simple term sorting (not perfect but helps)
            terms = re.split(r'([+-])', text)
            terms = [t for t in terms if t]
            # This is simplified; real implementation would parse properly
        return text
    
    def _normalize_interval(self, text: str) -> Tuple[float, float]:
        """Normalize an interval answer."""
        # Extract bounds from interval notation
        match = re.search(r'([\[\(])\s*([-\d.]+)\s*,\s*([-\d.]+)\s*([\]\)])', text)
        if match:
            left_bracket, left, right, right_bracket = match.groups()
            return (float(left), float(right))
        
        # Try inequality format: a < x < b
        match = re.search(r'([-\d.]+)\s*<\s*x\s*<\s*([-\d.]+)', text)
        if match:
            return (float(match.group(1)), float(match.group(2)))
        
        return None
    
    def _normalize_set(self, text: str) -> List[float]:
        """Normalize a set answer."""
        # Extract numbers from set notation or list
        numbers = re.findall(r'[-+]?\d*\.?\d+', text)
        return sorted([float(n) for n in numbers])
    
    def _compare_algebraic_answers(self, pred: str, exp: str) -> bool:
        """Compare algebraic answers with more flexibility."""
        # Handle "x = a or x = b" format
        pred_values = self._extract_solution_values(pred)
        exp_values = self._extract_solution_values(exp)
        
        if pred_values and exp_values:
            # Check if sets of values match
            return set(pred_values) == set(exp_values)
        
        # Handle interval answers
        pred_interval = self._normalize_interval(pred)
        exp_interval = self._normalize_interval(exp)
        
        if pred_interval and exp_interval:
            return (abs(pred_interval[0] - exp_interval[0]) < 1e-6 and
                   abs(pred_interval[1] - exp_interval[1]) < 1e-6)
        
        return False
    
    def _extract_solution_values(self, text: str) -> Optional[List[float]]:
        """Extract solution values from 'x = a or x = b' format."""
        # Look for "x = number" patterns
        matches = re.findall(r'x\s*=\s*([-+]?\d*\.?\d+)', text)
        if matches:
            return [float(m) for m in matches]
        
        # Look for just numbers separated by "or"
        if " or " in text:
            parts = text.split(" or ")
            values = []
            for part in parts:
                num = self._extract_number(part)
                if num is not None:
                    values.append(num)
            if values:
                return values
        
        return None