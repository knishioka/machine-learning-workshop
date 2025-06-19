"""Recall Related cognitive tool implementation."""

from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel, Field

from .base import CognitiveTool
from ..prompts.system_prompts import RECALL_RELATED_PROMPT


class RecallRelatedInput(BaseModel):
    """Input schema for recall_related tool."""
    question: str = Field(description="The mathematical problem to find analogous examples for")


class RecallRelatedTool(CognitiveTool):
    """Tool for retrieving similar solved problems from memory."""
    
    name: str = "recall_related"
    description: str = (
        "Retrieves 2-3 similar solved problems that require comparable mathematical concepts "
        "or reasoning steps. Provides complete solutions to help reason through the current problem."
    )
    args_schema: Type[BaseModel] = RecallRelatedInput
    llm: BaseLanguageModel
    
    def _run(
        self,
        question: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the recall_related tool."""
        prompt = f"{RECALL_RELATED_PROMPT}\n\nCurrent Problem: {question}"
        
        response = self.llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            return response.content
        return str(response)