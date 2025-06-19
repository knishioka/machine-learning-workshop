"""Backtracking cognitive tool implementation."""

from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel, Field

from .base import CognitiveTool
from ..prompts.system_prompts import BACKTRACKING_PROMPT


class BacktrackingInput(BaseModel):
    """Input schema for backtracking tool."""
    question: str = Field(description="The original problem")
    reasoning_trace: str = Field(description="The current reasoning trace that may contain errors")


class BacktrackingTool(CognitiveTool):
    """Tool for identifying errors in reasoning and suggesting corrections."""
    
    name: str = "backtracking"
    description: str = (
        "Analyzes reasoning traces to identify errors, bad assumptions, or confusion. "
        "Proposes how to revise the approach from the first error point or suggests a new strategy."
    )
    args_schema: Type[BaseModel] = BacktrackingInput
    llm: BaseLanguageModel
    
    def _run(
        self,
        question: str,
        reasoning_trace: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the backtracking tool."""
        prompt = f"""{BACKTRACKING_PROMPT}

Problem: {question}
Current Reasoning Trace: {reasoning_trace}"""
        
        response = self.llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            return response.content
        return str(response)