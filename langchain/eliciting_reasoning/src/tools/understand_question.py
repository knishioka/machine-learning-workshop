"""Understand Question cognitive tool implementation."""

from typing import Any, Dict, Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel, Field

from .base import CognitiveTool
from ..prompts.system_prompts import UNDERSTAND_QUESTION_PROMPT


class UnderstandQuestionInput(BaseModel):
    """Input schema for understand_question tool."""
    question: str = Field(description="The mathematical problem to analyze")
    model: str = Field(
        default="math_problem",
        description="Type of problem (e.g., 'math_problem', 'logic_puzzle')"
    )


class UnderstandQuestionTool(CognitiveTool):
    """Tool for analyzing and breaking down complex mathematical problems."""
    
    name: str = "understand_question"
    description: str = (
        "Analyzes and breaks down complex mathematical problems into structured steps. "
        "Identifies core concepts, extracts relevant symbols, and suggests solution strategies."
    )
    args_schema: Type[BaseModel] = UnderstandQuestionInput
    llm: BaseLanguageModel
    
    def _run(
        self,
        question: str,
        model: str = "math_problem",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the understand_question tool."""
        prompt = f"{UNDERSTAND_QUESTION_PROMPT}\n\nProblem: {question}\nModel: {model}"
        
        response = self.llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            return response.content
        return str(response)