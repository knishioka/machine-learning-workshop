"""Use Code cognitive tool implementation."""

import sys
import io
import contextlib
import traceback
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.language_models import BaseLanguageModel
from pydantic import BaseModel, Field

from .base import CognitiveTool
from ..prompts.system_prompts import USE_CODE_PROMPT


class UseCodeInput(BaseModel):
    """Input schema for use_code tool."""
    problem: str = Field(description="The problem to solve with code")
    reasoning: str = Field(
        default="", 
        description="Previous reasoning or code that may contain mistakes"
    )


class UseCodeTool(CognitiveTool):
    """Tool for generating and executing Python code to solve problems."""
    
    name: str = "use_code"
    description: str = (
        "Generates correct and efficient Python code to solve mathematical problems. "
        "Executes the code and returns both the code and its output."
    )
    args_schema: Type[BaseModel] = UseCodeInput
    llm: BaseLanguageModel
    
    def _run(
        self,
        problem: str,
        reasoning: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the use_code tool."""
        prompt = f"""{USE_CODE_PROMPT}

Problem: {problem}
Previous Reasoning: {reasoning}"""
        
        response = self.llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            response_text = response.content
        else:
            response_text = str(response)
        
        # Extract code from response
        code = self._extract_code(response_text)
        
        if code:
            # Execute the code safely
            execution_result = self._execute_code_safely(code)
            return f"{response_text}\n\nExecution Output:\n{execution_result}"
        
        return response_text
    
    def _extract_code(self, response: str) -> Optional[str]:
        """Extract Python code from the response."""
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()
        return None
    
    def _execute_code_safely(self, code: str) -> str:
        """Execute Python code safely and capture output."""
        # Create StringIO object to capture output
        output_buffer = io.StringIO()
        
        # Save original stdout
        old_stdout = sys.stdout
        
        try:
            # Redirect stdout to our buffer
            sys.stdout = output_buffer
            
            # Create execution namespace
            exec_globals = {}
            exec_locals = {}
            
            # Execute the code with full builtins available
            exec(code, exec_globals, exec_locals)
            
            # Get the output
            output = output_buffer.getvalue()
            
            # If no output from print, try to get the last expression value
            if not output:
                # Try to find the last expression in the code
                lines = code.strip().split('\n')
                last_line = lines[-1].strip()
                
                # If last line is not an assignment or import, evaluate it
                if (last_line and 
                    not last_line.startswith(('import ', 'from ', 'def ', 'class ')) and
                    '=' not in last_line and
                    not last_line.startswith(('#', 'print('))):
                    try:
                        result = eval(last_line, exec_globals, exec_locals)
                        if result is not None:
                            output = str(result)
                    except:
                        pass
            
            if not output:
                # Check if any variables were created
                created_vars = {k: v for k, v in exec_locals.items() if not k.startswith('_')}
                if created_vars:
                    output = "Variables created:\n"
                    for name, value in created_vars.items():
                        output += f"{name} = {value}\n"
                else:
                    output = "Code executed successfully but produced no output."
            
            return output
            
        except Exception as e:
            # Capture the error
            return f"Error executing code:\n{type(e).__name__}: {str(e)}"
        
        finally:
            # Restore original stdout
            sys.stdout = old_stdout
            output_buffer.close()