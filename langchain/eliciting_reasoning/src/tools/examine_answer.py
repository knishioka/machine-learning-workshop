"""Examine Answer cognitive tool implementation."""

from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel, Field

from .base import CognitiveTool
from ..prompts.system_prompts import EXAMINE_ANSWER_PROMPT


class ExamineAnswerInput(BaseModel):
    """Input schema for examine_answer tool."""
    question: str = Field(description="The original mathematical problem")
    current_proposed_answer: str = Field(description="The proposed solution to verify")


class ExamineAnswerTool(CognitiveTool):
    """Tool for verifying and improving solutions to mathematical problems."""
    
    name: str = "examine_answer"
    description: str = (
        "Critically analyzes a proposed solution for correctness, clarity, and completeness. "
        "Checks logical consistency, mathematical correctness, and identifies any errors."
    )
    args_schema: Type[BaseModel] = ExamineAnswerInput
    llm: BaseLanguageModel
    
    def _run(
        self,
        question: str,
        current_proposed_answer: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the examine_answer tool."""
        prompt = f"""{EXAMINE_ANSWER_PROMPT}

Question: {question}
Current Proposed Answer: {current_proposed_answer}"""
        
        response = self.llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            return response.content
        return str(response)