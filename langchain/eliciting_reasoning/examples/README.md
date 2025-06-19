# Examples

This directory contains example scripts demonstrating the cognitive tools system.

## Available Examples

### 1. simple_example.py
Basic usage of the cognitive tools system to solve a single math problem.

```bash
python examples/simple_example.py
```

### 2. model_comparison.py
Compares different LLM models (GPT-4, GPT-3.5-turbo, Claude-3.5) on the same problem using both cognitive tools and baseline approaches.

```bash
python examples/model_comparison.py
```

## Writing Your Own Examples

To create custom examples, follow this pattern:

```python
from src.agents import CognitiveAgent
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.1)

# Create agent
agent = CognitiveAgent(llm)

# Solve problem
result = agent.solve("Your math problem here", max_iterations=5)
print(f"Answer: {result.get('final_answer')}")
```