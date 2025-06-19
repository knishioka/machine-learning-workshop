"""LangGraph implementation of the cognitive reasoning system."""

import re
from typing import Dict, List, Literal, Optional, Sequence, Annotated
from operator import add

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.language_models import BaseLanguageModel
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

from .state import CognitiveReasoningState
from ..tools import (
    UnderstandQuestionTool,
    RecallRelatedTool,
    ExamineAnswerTool,
    BacktrackingTool,
    UseCodeTool
)
from ..prompts.system_prompts import MAIN_SYSTEM_PROMPT


class CognitiveReasoningGraph:
    """Graph for cognitive reasoning with tools."""
    
    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm
        self.tools = self._create_tools(llm)
        self.graph = self._build_graph()
    
    def _create_tools(self, llm: BaseLanguageModel) -> List:
        """Create cognitive tools with the given LLM."""
        return [
            UnderstandQuestionTool(llm=llm),
            RecallRelatedTool(llm=llm),
            ExamineAnswerTool(llm=llm),
            BacktrackingTool(llm=llm),
            UseCodeTool(llm=llm)
        ]
    
    def _build_graph(self) -> StateGraph:
        """Build the reasoning graph."""
        # Create graph
        graph = StateGraph(CognitiveReasoningState)
        
        # Add nodes
        graph.add_node("reason", self._reason_node)
        graph.add_node("tools", ToolNode(self.tools))
        graph.add_node("check_solution", self._check_solution_node)
        graph.add_node("finalize", self._finalize_node)
        
        # Add edges
        graph.add_edge(START, "reason")
        graph.add_conditional_edges(
            "reason",
            self._should_continue,
            {
                "tools": "tools",
                "check": "check_solution",
                "end": END
            }
        )
        graph.add_edge("tools", "reason")
        graph.add_conditional_edges(
            "check_solution",
            self._check_result,
            {
                "continue": "reason",
                "finalize": "finalize"
            }
        )
        graph.add_edge("finalize", END)
        
        return graph.compile()
    
    def _format_tool_descriptions(self) -> str:
        """Format tool descriptions for the system prompt."""
        descriptions = []
        for tool in self.tools:
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)
    
    def _reason_node(self, state: CognitiveReasoningState) -> Dict:
        """Main reasoning node that decides on actions."""
        # Increment iteration
        iteration = state.get("iteration", 0) + 1
        
        # Check if we've reached max iterations
        if iteration >= state.get("max_iterations", 10):
            # Try to extract answer from reasoning trace
            extracted_answer = self._extract_answer_from_reasoning(state.get("current_reasoning", ""))
            if extracted_answer:
                return {
                    "messages": [AIMessage(content=f"ANSWER: {extracted_answer}")],
                    "iteration": iteration,
                    "final_answer": extracted_answer
                }
            else:
                return {
                    "messages": [AIMessage(content="Maximum iterations reached. Unable to provide a final answer.")],
                    "iteration": iteration,
                    "final_answer": None
                }
        
        # Build context from previous messages
        messages = state.get("messages", [])
        
        # Create system message if this is the first iteration
        if iteration == 1:
            system_prompt = MAIN_SYSTEM_PROMPT.format(
                tool_descriptions=self._format_tool_descriptions()
            )
            messages = [
                HumanMessage(content=f"{system_prompt}\n\nProblem: {state['problem']}\n\nRemember: You MUST end your response with 'ANSWER: [your final answer]' when you have solved the problem.")
            ]
        
        # Get LLM response
        response = self.llm.bind_tools(self.tools).invoke(messages)
        
        # Extract content from response
        response_content = ""
        if hasattr(response, 'content'):
            if isinstance(response.content, list):
                # Handle list content (Claude-3.5 format)
                response_content = " ".join(str(item) for item in response.content)
            else:
                response_content = str(response.content)
        
        # Update state
        updates = {
            "messages": [response],
            "iteration": iteration,
            "current_reasoning": state.get("current_reasoning", "") + "\n" + response_content
        }
        
        # Check if answer is provided
        if response_content and "ANSWER:" in response_content.upper():
            updates["final_answer"] = self._extract_answer(response_content)
        
        # Also check the entire reasoning trace for answers
        if not updates.get("final_answer") and updates["current_reasoning"]:
            updates["final_answer"] = self._extract_answer(updates["current_reasoning"])
        
        return updates
    
    def _should_continue(self, state: CognitiveReasoningState) -> Literal["tools", "check", "end"]:
        """Decide whether to use tools, check solution, or end."""
        messages = state.get("messages", [])
        if not messages:
            return "end"
        
        last_message = messages[-1]
        
        # Check if tool was called
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        
        # Check if answer was provided
        if state.get("final_answer"):
            return "check"
        
        # Check if max iterations reached
        if state.get("iteration", 0) >= state.get("max_iterations", 10):
            return "end"
        
        return "tools"  # Default to trying tools
    
    def _check_solution_node(self, state: CognitiveReasoningState) -> Dict:
        """Check if the solution needs verification."""
        # For now, we'll skip automatic verification
        # In a full implementation, this could use examine_answer tool
        return {
            "solution_verified": True,
            "verification_result": "Solution accepted without verification."
        }
    
    def _check_result(self, state: CognitiveReasoningState) -> Literal["continue", "finalize"]:
        """Decide based on verification result."""
        if state.get("solution_verified", False):
            return "finalize"
        return "continue"
    
    def _finalize_node(self, state: CognitiveReasoningState) -> Dict:
        """Finalize the solution."""
        return {
            "messages": [AIMessage(content=f"Final Answer: {state.get('final_answer', 'No answer found')}")],
        }
    
    def _extract_answer(self, text: str) -> Optional[str]:
        """Extract the final answer from text."""
        # Try multiple patterns for answer extraction
        patterns = [
            r'ANSWER:\s*(.+?)(?:\n|$)',
            r'Final Answer:\s*(.+?)(?:\n|$)',
            r'The answer is:\s*(.+?)(?:\n|$)',
            r'Result:\s*(.+?)(?:\n|$)',
            r'Solution:\s*(.+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        # If no explicit answer pattern, try to extract from execution output
        if "Execution Output:" in text:
            output_start = text.find("Execution Output:") + len("Execution Output:")
            output_text = text[output_start:].strip()
            # Take first line of output as answer
            first_line = output_text.split('\n')[0].strip()
            if first_line and not first_line.startswith(("Error", "Code executed")):
                return first_line
        
        return None
    
    def _extract_answer_from_reasoning(self, reasoning: str) -> Optional[str]:
        """Extract answer from reasoning trace using various heuristics."""
        # First try standard extraction
        answer = self._extract_answer(reasoning)
        if answer:
            return answer
        
        # Look for common answer patterns in the text
        patterns = [
            r'(?:GCD|gcd|answer|result|solution)(?:\s+is\s+|\s*:\s*|\s*=\s*)(\d+)',
            r'(?:equals?|is)\s+(\d+)',
            r'(?:x\s*=\s*)([\d\s,or]+)',
            r'(?:The\s+)?(?:final\s+)?(?:answer|result|solution)\s+(?:is\s+)?([^\n.]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, reasoning, re.IGNORECASE)
            if matches:
                # Return the last match
                return matches[-1].strip()
        
        # For code execution results, look for the last number
        if "Execution Output:" in reasoning:
            output_section = reasoning.split("Execution Output:")[-1]
            numbers = re.findall(r'\b\d+\b', output_section)
            if numbers:
                return numbers[-1]
        
        return None
    
    def solve(self, problem: str, max_iterations: int = 10) -> Dict:
        """Solve a problem using the cognitive reasoning graph."""
        initial_state = {
            "problem": problem,
            "messages": [],
            "current_reasoning": "",
            "final_answer": None,
            "tool_calls": [],
            "tool_outputs": [],
            "iteration": 0,
            "max_iterations": max_iterations,
            "solution_verified": False,
            "verification_result": None,
            "errors": [],
            "needs_backtracking": False
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            "problem": problem,
            "final_answer": result.get("final_answer"),
            "reasoning_trace": result.get("current_reasoning", ""),
            "tool_usage": self._extract_tool_usage(result.get("messages", [])),
            "iterations": result.get("iteration", 0)
        }
    
    def _extract_tool_usage(self, messages: List[BaseMessage]) -> List[Dict]:
        """Extract tool usage information from messages."""
        tool_usage = []
        
        for msg in messages:
            if hasattr(msg, "tool_calls"):
                for tool_call in msg.tool_calls:
                    tool_usage.append({
                        "tool": tool_call["name"],
                        "args": tool_call["args"]
                    })
        
        return tool_usage