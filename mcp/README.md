# Simple MCP Server

A simple implementation of a Model Context Protocol (MCP) server in Python.

## Features

This MCP server provides:

### Tools
- **calculate**: Perform basic arithmetic operations (add, subtract, multiply, divide)
- **echo**: Echo back a provided message
- **get_time**: Get the current time

### Prompts
- **greeting**: Generate a greeting message in different languages
- **math_problem**: Generate math problems of varying difficulty

## Installation

```bash
# Clone the repository
cd mcp

# Install dependencies using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage

### Running the Server

```bash
# Run directly
python server.py

# Or if installed
simple-mcp-server
```

### Configuring with Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "simple-mcp": {
      "command": "python",
      "args": ["/path/to/your/mcp/server.py"]
    }
  }
}
```

Replace `/path/to/your/mcp/server.py` with the actual path to your server.py file.

## Testing with MCP Inspector

MCP Inspector is a useful tool for testing and debugging MCP servers.

### Install MCP Inspector

```bash
npm install -g @modelcontextprotocol/inspector
```

### Test the Server

1. Start the inspector:
   ```bash
   mcp-inspector
   ```

2. Open your browser to `http://localhost:5173`

3. Connect to your server by entering:
   ```
   python /path/to/your/mcp/server.py
   ```

4. Test the available tools and prompts:

   **Testing Tools:**
   - Click on "Tools" tab
   - Select "calculate" and test with:
     ```json
     {
       "operation": "add",
       "a": 10,
       "b": 5
     }
     ```
   
   - Select "echo" and test with:
     ```json
     {
       "message": "Hello MCP!"
     }
     ```
   
   - Select "get_time" (no parameters needed)

   **Testing Prompts:**
   - Click on "Prompts" tab
   - Select "greeting" and test with:
     ```json
     {
       "name": "Alice",
       "language": "Japanese"
     }
     ```
   
   - Select "math_problem" and test with:
     ```json
     {
       "difficulty": "medium"
     }
     ```

### Debugging Tips

1. The inspector shows real-time communication between client and server
2. Check the "Messages" tab to see the JSON-RPC messages
3. Any errors will be displayed in the console output
4. Use the browser's developer console for additional debugging

### Testing with the Test Client

A test client is included to verify server functionality:

```bash
cd mcp
python test_client.py
```

This will test all available tools and prompts and display the results.

## Server Structure

```
mcp/
├── server.py          # Main server implementation
├── pyproject.toml     # Package configuration
└── README.md          # This file
```

## Extending the Server

To add new tools or prompts:

1. Add tool definitions in `_setup_tools()` method
2. Add prompt definitions in `_setup_prompts()` method
3. Implement the corresponding handlers

Example of adding a new tool:

```python
# In list_tools()
Tool(
    name="your_tool",
    description="Tool description",
    inputSchema={
        "type": "object",
        "properties": {
            "param": {"type": "string"}
        },
        "required": ["param"]
    }
)

# In call_tool()
elif name == "your_tool":
    # Your implementation here
    return [CallToolResult(
        content=[TextContent(text="Result")]
    )]
```

## Troubleshooting

1. **Connection Issues**: Ensure the server path is correct in your configuration
2. **Import Errors**: Make sure the `mcp` package is installed
3. **Permission Errors**: The server script needs to be executable
4. **Inspector Issues**: Check that Node.js and npm are properly installed

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)