# Cognitive Tools Implementation with LangGraph

This project implements the cognitive tools approach from the paper "Eliciting Reasoning in Language Models with Cognitive Tools" using LangGraph.

📄 **Paper**: [Eliciting Reasoning in Language Models with Cognitive Tools](https://arxiv.org/abs/2506.12115)  
🔧 **Framework**: LangGraph + LangChain  
📊 **Models Tested**: GPT-4, GPT-3.5-turbo, Claude-3.5-Sonnet  
👥 **Authors**: Brown Ebouky, Andrea Bartezzaghi, Mattia Rigotti (2025)

## Overview

The experiment compares two approaches for solving mathematical problems:
1. **Cognitive Tools**: Uses specialized tools (understand_question, recall_related, examine_answer, backtracking, use_code) to enhance reasoning
2. **Baseline**: Standard chain-of-thought prompting without tools

## Setup

### Prerequisites
- Python 3.10+
- uv package manager

### Installation

1. Clone and navigate to the project:
```bash
cd langchain/eliciting_reasoning
```

2. Create virtual environment and install:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Set up environment variables:
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  # Optional, for Claude models
```

## Project Structure

```
langchain/eliciting_reasoning/
├── src/                        # Source code
│   ├── tools/                  # Cognitive tool implementations
│   ├── agents/                 # LangGraph agent
│   ├── graphs/                 # StateGraph implementation
│   └── prompts/               # System prompts
├── experiments/                # Experiment framework
│   ├── datasets/              # Problem datasets
│   ├── evaluation.py          # Evaluation logic
│   └── run_experiment.py      # Main experiment runner
├── results/                    # Experiment results
└── docs/                      # Documentation
```

## Quick Start

### 1. Simple Example
```bash
python examples/simple_example.py
```

### 2. Model Comparison
```bash
python examples/model_comparison.py
```

## Running Full Experiments

### Basic Usage
```bash
python experiments/run_experiment.py --model gpt-4
```

### Different Models
```bash
# GPT-3.5
python experiments/run_experiment.py --model gpt-3.5-turbo

# Claude 3.5
python experiments/run_experiment.py --model claude-3-5-sonnet-20241022
```

### Custom Dataset

```bash
python experiments/run_experiment.py --dataset path/to/your/dataset.json
```

## Cognitive Tools

### 1. understand_question
- Analyzes problem structure
- Identifies mathematical concepts
- Suggests solution strategies

### 2. recall_related
- Retrieves similar solved problems
- Provides analogous examples
- Helps with pattern recognition

### 3. examine_answer
- Verifies solution correctness
- Checks logical consistency
- Identifies calculation errors

### 4. backtracking
- Identifies reasoning errors
- Suggests corrections
- Proposes alternative approaches

### 5. use_code
- Generates Python code
- Executes calculations
- Validates numerical results

## Results

After running an experiment, you'll find:
- `results/results_TIMESTAMP.json`: Raw experiment data
- `results/report_TIMESTAMP.md`: Detailed analysis report
- `results/results_plot_TIMESTAMP.png`: Visualization plots

## Dataset Format

Problems should be in JSON format:
```json
{
  "problems": [
    {
      "id": "unique_id",
      "question": "Problem statement",
      "answer": "Expected answer",
      "type": "problem_category",
      "difficulty": "easy|medium|hard"
    }
  ]
}
```

## Extending the Experiment

### Adding New Tools

1. Create a new tool in `src/tools/`
2. Inherit from `CognitiveTool` base class
3. Implement the `_run` method
4. Add to the tools list in `reasoning_graph.py`

### Adding New Problem Types

1. Add problems to the dataset
2. Update evaluation logic if needed for special answer formats

## Key Findings

### Performance Summary (5 problems, medium difficulty)
| Model | Cognitive Tools | Baseline | 
|-------|----------------|----------|
| GPT-4 | 40% | 100% |
| GPT-3.5-turbo | 40% | 80% |
| Claude-3.5 | 40% | 100% |

### When Cognitive Tools Help
- ✅ Complex computational problems
- ✅ Problems requiring code execution
- ✅ Multi-step mathematical reasoning

### When Baseline is Better
- ✅ Simple arithmetic
- ✅ Direct pattern recognition
- ✅ When token efficiency matters (10x fewer tokens)

See the [comprehensive report](COMPREHENSIVE_FINAL_REPORT.md) for detailed analysis.

## Citation

Based on the paper:

> **Eliciting Reasoning in Language Models with Cognitive Tools**  
> Brown Ebouky, Andrea Bartezzaghi, Mattia Rigotti  
> arXiv:2506.12115 [cs.CL], June 2025  
> https://arxiv.org/abs/2506.12115

```bibtex
@article{ebouky2025eliciting,
  title={Eliciting Reasoning in Language Models with Cognitive Tools},
  author={Ebouky, Brown and Bartezzaghi, Andrea and Rigotti, Mattia},
  journal={arXiv preprint arXiv:2506.12115},
  year={2025}
}
```