#!/usr/bin/env python3
"""
Simple MCP (Model Context Protocol) Server Implementation
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
    GetPromptResult,
    Prompt,
    PromptMessage,
    PromptArgument,
)


class SimpleMCPServer:
    """A simple MCP server with basic tools and prompts."""
    
    def __init__(self):
        self.server = Server("simple-mcp-server")
        self._setup_tools()
        self._setup_prompts()
    
    def _setup_tools(self):
        """Register available tools."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="calculate",
                    description="Perform basic arithmetic calculations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["add", "subtract", "multiply", "divide"],
                                "description": "The arithmetic operation to perform"
                            },
                            "a": {
                                "type": "number",
                                "description": "First number"
                            },
                            "b": {
                                "type": "number",
                                "description": "Second number"
                            }
                        },
                        "required": ["operation", "a", "b"]
                    }
                ),
                Tool(
                    name="echo",
                    description="Echo back the provided message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message to echo back"
                            }
                        },
                        "required": ["message"]
                    }
                ),
                Tool(
                    name="get_time",
                    description="Get the current time",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[CallToolResult]:
            if name == "calculate":
                try:
                    operation = arguments["operation"]
                    a = float(arguments["a"])
                    b = float(arguments["b"])
                    
                    if operation == "add":
                        result = a + b
                    elif operation == "subtract":
                        result = a - b
                    elif operation == "multiply":
                        result = a * b
                    elif operation == "divide":
                        if b == 0:
                            return [CallToolResult(
                                content=[TextContent(type="text", text="Error: Division by zero")],
                                isError=True
                            )]
                        result = a / b
                    else:
                        return [CallToolResult(
                            content=[TextContent(type="text", text=f"Unknown operation: {operation}")],
                            isError=True
                        )]
                    
                    return [CallToolResult(
                        content=[TextContent(type="text", text=f"Result: {result}")]
                    )]
                except Exception as e:
                    return [CallToolResult(
                        content=[TextContent(type="text", text=f"Error: {str(e)}")],
                        isError=True
                    )]
            
            elif name == "echo":
                message = arguments.get("message", "")
                return [CallToolResult(
                    content=[TextContent(type="text", text=f"Echo: {message}")]
                )]
            
            elif name == "get_time":
                from datetime import datetime
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return [CallToolResult(
                    content=[TextContent(type="text", text=f"Current time: {current_time}")]
                )]
            
            else:
                return [CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                    isError=True
                )]
    
    def _setup_prompts(self):
        """Register available prompts."""
        
        @self.server.list_prompts()
        async def list_prompts() -> List[Prompt]:
            return [
                Prompt(
                    name="greeting",
                    description="Generate a greeting message",
                    arguments=[
                        PromptArgument(
                            name="name",
                            description="Name of the person to greet",
                            required=True
                        ),
                        PromptArgument(
                            name="language",
                            description="Language for the greeting (default: English)",
                            required=False
                        )
                    ]
                ),
                Prompt(
                    name="math_problem",
                    description="Generate a math problem explanation",
                    arguments=[
                        PromptArgument(
                            name="difficulty",
                            description="Difficulty level: easy, medium, hard",
                            required=True
                        )
                    ]
                )
            ]
        
        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: Optional[Dict[str, str]] = None) -> GetPromptResult:
            if name == "greeting":
                name_arg = arguments.get("name", "World") if arguments else "World"
                language = arguments.get("language", "English") if arguments else "English"
                
                greetings = {
                    "English": f"Hello, {name_arg}! Welcome to the MCP server.",
                    "Japanese": f"こんにちは、{name_arg}さん！MCPサーバーへようこそ。",
                    "Spanish": f"¡Hola, {name_arg}! Bienvenido al servidor MCP.",
                    "French": f"Bonjour, {name_arg}! Bienvenue sur le serveur MCP."
                }
                
                message = greetings.get(language, greetings["English"])
                
                return GetPromptResult(
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=message)
                        )
                    ]
                )
            
            elif name == "math_problem":
                difficulty = arguments.get("difficulty", "easy") if arguments else "easy"
                
                problems = {
                    "easy": "What is 2 + 2?",
                    "medium": "Solve for x: 3x + 7 = 22",
                    "hard": "Find the derivative of f(x) = x³ - 4x² + 2x - 8"
                }
                
                problem = problems.get(difficulty, problems["easy"])
                
                return GetPromptResult(
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=f"Please solve this math problem: {problem}")
                        )
                    ]
                )
            
            else:
                return GetPromptResult(
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=f"Unknown prompt: {name}")
                        )
                    ]
                )
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, self.server.create_initialization_options())


async def main():
    """Main entry point."""
    server = SimpleMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())