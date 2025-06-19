"""Base classes for cognitive tools."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel, Field


class CognitiveToolInput(BaseModel):
    """Base input schema for cognitive tools."""
    question: str = Field(description="The problem or question to analyze")
    context: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional context from previous reasoning steps"
    )


class CognitiveTool(BaseTool, ABC):
    """Base class for cognitive tools."""
    
    @abstractmethod
    def _run(
        self, 
        question: str,
        context: Optional[Dict[str, Any]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the cognitive tool."""
        pass
    
    async def _arun(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Async execution - not implemented for this experiment."""
        raise NotImplementedError("Async execution not implemented")