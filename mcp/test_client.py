#!/usr/bin/env python3
"""
Test client for the Simple MCP Server
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_server():
    """Test the MCP server functionality."""
    
    # Connect to the server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        cwd="/Users/ken/Developer/private/machine-learning-workshop/mcp"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("=== Connected to MCP Server ===\n")
            
            # Test listing tools
            print("1. Available Tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description}")
            
            print("\n2. Testing Tools:")
            
            # Test calculate tool
            print("\n   a) Testing 'calculate' tool (10 + 5):")
            result = await session.call_tool(
                "calculate",
                {"operation": "add", "a": 10, "b": 5}
            )
            print(f"      Result: {result.content[0].text}")
            
            # Test echo tool
            print("\n   b) Testing 'echo' tool:")
            result = await session.call_tool(
                "echo",
                {"message": "Hello from MCP client!"}
            )
            print(f"      Result: {result.content[0].text}")
            
            # Test get_time tool
            print("\n   c) Testing 'get_time' tool:")
            result = await session.call_tool("get_time", {})
            print(f"      Result: {result.content[0].text}")
            
            # Test listing prompts
            print("\n3. Available Prompts:")
            prompts = await session.list_prompts()
            for prompt in prompts.prompts:
                print(f"   - {prompt.name}: {prompt.description}")
            
            print("\n4. Testing Prompts:")
            
            # Test greeting prompt
            print("\n   a) Testing 'greeting' prompt (Japanese):")
            result = await session.get_prompt(
                "greeting",
                {"name": "Ken", "language": "Japanese"}
            )
            print(f"      Result: {result.messages[0].content.text}")
            
            # Test math_problem prompt
            print("\n   b) Testing 'math_problem' prompt (medium difficulty):")
            result = await session.get_prompt(
                "math_problem",
                {"difficulty": "medium"}
            )
            print(f"      Result: {result.messages[0].content.text}")
            
            print("\n=== All tests completed successfully! ===")


if __name__ == "__main__":
    asyncio.run(test_server())