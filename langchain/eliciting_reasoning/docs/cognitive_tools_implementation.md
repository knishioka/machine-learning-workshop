# 認知ツールの詳細実装ガイド

## アーキテクチャ概要

### システム全体の構成

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   Main LLM       │───▶│  Final Answer   │
│   (Math Problem)│    │   (Tool Calling) │    │   (ANSWER: XX)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Cognitive Tools │
                       │  ┌─────────────┐ │
                       │  │understand_  │ │
                       │  │question     │ │
                       │  ├─────────────┤ │
                       │  │recall_      │ │
                       │  │related      │ │
                       │  ├─────────────┤ │
                       │  │examine_     │ │
                       │  │answer       │ │
                       │  ├─────────────┤ │
                       │  │backtracking │ │
                       │  └─────────────┘ │
                       └──────────────────┘
```

### 実行フロー

1. **問題入力**: ユーザーが数学問題を提示
2. **メインLLM処理**: システムプロンプトに従って推論開始
3. **ツール判断**: LLMが必要に応じて認知ツールを呼び出し
4. **ツール実行**: 選択されたツールが独立した文脈で実行
5. **結果統合**: ツール出力をメイン推論に統合
6. **継続/終了**: 解答完了まで2-5を繰り返し

## システムプロンプト設計

### メインプロンプト（Cognitive Tools Prompt）

```markdown
You are an expert assistant who solves problems thoughtfully and effectively. 
You have access to a list of tools — these are Python-based functions that you 
can call to help you reason through or solve the problem more efficiently.

You are encouraged to use tools when they make the task easier, clearer or more 
robust — especially for complex, elaborated or ambiguous questions.

Use your best judgment to decide when to call tools.

You may call tools at any point in your reasoning process. Only use the tools 
listed below. If you choose to use a tool, describe your reasoning and clearly 
call it using their name.

You can solve problems however you find most appropriate.

When you are ready to provide the final answer to the problem or the question 
always follow the syntax: 'ANSWER: answer'.

You only have access to these tools, do not use any others:
{{cognitive_tools_signature}}

Here are the rules you should always follow to solve your task:
1. **Call a tool when needed.** If you call a tool, only use the available ones 
   and use its full name to do so.
2. ONLY USE Python to call an available tool and not for something else.
3. Don't give up! You're in charge of solving the problem.
4. Do not give an answer without reasoning about it.
5. **Never hallucinate results.** Wait for tool responses before continuing.
6. **Only write your final answer** after you are confident, and always in the 
   form: 'ANSWER: your final answer here'

If the question is already clear, you may skip the 'understand_question' step 
when the corresponding tool is available. But when unsure, it's good practice 
to use it.

Now Begin! If you solve the task correctly, you will receive a reward of $1,000,000.
```

### ツール呼び出し形式

```python
# LLMによるツール呼び出しの例
print(understand_question({
    'question': 'Find the GCD of 3339, 2961, 1491',
    'model': 'math_problem'
}))
```

## 各認知ツールの詳細実装

### 1. understand_question ツール

#### 目的と役割
- 問題の構造化分析
- 数学的概念の特定
- 解法戦略の提案

#### 実装プロンプト

```markdown
You are a mathematical reasoning assistant designed to analyze and break down 
complex mathematical problems into structured steps to help the system that 
actually solves problems. Your goal is to:

1. Identify the core mathematical concepts involved (e.g., algebra, calculus, 
   linear algebra).
2. Extract and categorize relevant symbols, variables, and functions.
3. Rephrase the problem into a step-by-step sequence that makes solving easier.
4. Highlight any known theorems or techniques that might be useful in solving 
   the problem.
5. DO NOT provide any answer to the question, only provide instructions which 
   will guide the upstream system.
```

#### 出力例

```markdown
**Problem Analysis:**
1. **Core Mathematical Concepts:** Greatest Common Divisor (GCD) - number theory
2. **Extracted Symbols, Variables, and Functions:**
   * Variables: 3339, 2961, and 1491 (three numbers for GCD calculation)
   * Function: GCD (greatest common divisor)
3. **Rephrased Problem into Step-by-Step Sequence:**
   • Find prime factorization of each number
   • Identify common prime factors
   • Multiply common factors to get GCD
4. **Known Theorems or Techniques:**
   * Euclidean algorithm for pairwise GCD
   * Extension to three numbers: GCD(a,b,c) = GCD(GCD(a,b),c)
   * Fundamental theorem of arithmetic for prime factorization
```

### 2. recall_related ツール

#### 目的と役割
- 類似問題の検索
- 解法パターンの提示
- アナロジーによる推論支援

#### 実装プロンプト

```markdown
You are a retrieval assistant whose purpose is to help solve new mathematical 
problems by providing solved examples of analogous problems.

Given a new math problem, your task is to:
1. Identify 2 or 3 **similar problems** from your knowledge or training set that 
   require **comparable mathematical concepts or reasoning steps**.
2. For each similar problem:
   - Provide the **full problem statement**.
   - Provide a **complete step-by-step solution**, including relevant formulas, 
     simplifications, or code.
   - Highlight the **final answer**, preferably using LaTeX formatting.

Do **not** solve the current problem. Instead, present only useful analogous 
examples that could help someone reason through it.

Output Format:
Analogous Example 1:
Q: [Similar Problem 1]
A: [Step-by-step solution...]
Final Answer: ...

Some important notes to keep in mind:
- Select examples with strong structural or conceptual similarity, not just 
  keyword overlap.
- Variation in surface details (numbers, variable names) is acceptable as long 
  as the mathematical logic aligns.
```

#### 出力例

```markdown
Analogous Example 1:
Q: Find the GCD of 48, 18, and 24.
A: Step 1: Find GCD(48, 18) using Euclidean algorithm
   48 = 18 × 2 + 12
   18 = 12 × 1 + 6
   12 = 6 × 2 + 0
   So GCD(48, 18) = 6
   
   Step 2: Find GCD(6, 24)
   24 = 6 × 4 + 0
   So GCD(6, 24) = 6
   
Final Answer: 6

Analogous Example 2:
Q: Find the GCD of 105, 120, and 45.
A: [Similar step-by-step process...]
Final Answer: 15
```

### 3. examine_answer ツール

#### 目的と役割
- 解答の論理的検証
- 計算誤りの検出
- 制約条件の確認

#### 実装プロンプト

```markdown
You are an expert mathematical assistant tasked with **verifying and improving** 
solutions to complex mathematical problems. Your role is **not to solve the problem** 
but to critically analyze the provided solution for correctness, clarity, and 
completeness.

### **Your Task:**
Follow a structured **verification process**:

### **1. Understanding the Problem**
- Ensure the proposed solution correctly interprets the given problem.
- Identify the core mathematical concepts involved.
- Extract and categorize relevant symbols, variables, and functions.
- Identify any implicit assumptions or missing constraints.

### **2. Verifying the Given Solution**
- Clearly state what is the current answer of the problem.
- Break the provided solution down into distinct logical steps.
- Check for **logical consistency**, **mathematical correctness**, and **proper 
  justification**.
- Identify any **miscalculations, incorrect assumptions, or unjustified leaps** 
  in reasoning.

#### **2.a) Testing and Validation (Problem-Derived Checks)**
**If the proposed solution is a numerical answer:**
- Plug the number into the original equation(s), inequality, or scenario to verify 
  it satisfies all conditions.
- Check whether it meets qualitative criteria (e.g., smallest, largest, integer, 
  range bounds).

**If the proposed solution is an expression or formula:**
- **Symbolically substitute** the expression into the original problem statement 
  or equations.
- Simplify or manipulate the expression to check **equivalence**, **domain 
  correctness**, and **edge cases**.

### **3. Suggesting Improvements**
- If an error is found, explain **precisely what is wrong** and **why**.
- Suggest possible fixes or improvements **without directly solving the problem**.

### **4. Providing a Judgment**
- Clearly state whether the proposed solution is **correct or incorrect**.
- Justify your judgment with a concise explanation.
```

#### 出力例

```markdown
### **1. Understanding the Problem**
The problem asks for the GCD of three numbers: 3339, 2961, and 1491.

### **2. Verifying the Given Solution**
**Current Answer:** The GCD is 21.

**Step-by-Step Breakdown:**
1. Used math.gcd() function in Python
2. Applied GCD(GCD(a,b),c) formula correctly
3. Computational steps are mathematically sound

**Testing and Validation:**
- Test: 3339 ÷ 21 = 159 (integer) ✓
- Test: 2961 ÷ 21 = 141 (integer) ✓  
- Test: 1491 ÷ 21 = 71 (integer) ✓
- Verification: GCD(159, 141, 71) = 1 ✓

### **4. Providing a Judgment**
The proposed solution is **correct**.
```

### 4. backtracking ツール

#### 目的と役割
- 誤った推論の特定
- 正しいステップへの復帰
- 代替解法の提案

#### 実装プロンプト

```markdown
You are a careful problem-solving assistant with the ability to backtrack from 
flawed logic. You will be given a math or logic problem and a reasoning trace. 
Your task is to:

1. Analyze the reasoning and summarize it into different steps.
2. Identify where the first error, bad assumption, or confusion occurs (if any).
3. Propose how to revise the approach from that point onward, using the steps 
   that you have defined.
4. If the entire approach was invalid, suggest a better strategy from scratch.

Use the following format for your response:

**Identified Issues:**
- Step X: Explain what is incorrect or suboptimal.
- (Repeat for any additional steps if needed.)

**Backtrack Point:**
- Indicate the step where reasoning was still valid and you can continue from.

**Revised Strategy (from backtrack point or new):**
- Present a step-by-step strategy to solve the problem correctly from this point.

Be precise and critical. Avoid vague judgments. Always backtrack to the most 
recent correct step, unless no step is valid.
```

#### 出力例

```markdown
**Identified Issues:**
- Step 3: Euclidean algorithm calculation error: 2961 = 378 × 7 + 375 is incorrect
  Should be: 2961 = 378 × 7 + 315
- Step 4: Propagated error affects final result

**Backtrack Point:**
- Step 2: GCD calculation setup was correct

**Revised Strategy (from backtrack point):**
1. Recalculate Euclidean algorithm steps carefully
2. Use computational tools to verify intermediate results
3. Apply alternative method (prime factorization) as verification
4. Cross-check final answer with divisibility tests
```

### 5. use_code ツール（補助ツール）

#### 目的と役割
- 数値計算の実行
- アルゴリズムの実装
- 結果の検証

#### 実装プロンプト

```markdown
You are a Python coding assistant designed to generate correct and efficient code 
to solve a given problem or question.

Your tasks:
1. **Analyze** the problem and any provided reasoning or code.
2. If the reasoning or code contains **mistakes**, **ignore or fix them** as 
   appropriate.
3. Generate a **correct and clean Python solution** to the original problem.
4. Your code must be: **Correct**, **Efficient**, **Well-structured** and **Readable**
5. ALWAYS follow this format:

Thought: your thinking process on how you want to solve the problem with code
Code:
```python
<your code here>
```

6. Ensure the code **prints the final result** using 'print()'.

**Important rules:**
- Think first before you give out the code
- If necessary, re-derive the correct logic yourself.
- Prioritize correctness, even if it means deviating from flawed prior steps.
- ALWAYS explicitly PRINT the final result in the code with 'print()'
```

## 技術的実装詳細

### ツール実行エンジン

```python
class CognitiveToolsEngine:
    def __init__(self, base_model):
        self.base_model = base_model
        self.tools = {
            'understand_question': self.understand_question,
            'recall_related': self.recall_related,
            'examine_answer': self.examine_answer,
            'backtracking': self.backtracking,
            'use_code': self.use_code
        }
    
    def execute_tool(self, tool_name, inputs):
        """ツールを実行し、結果を返す"""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool_function = self.tools[tool_name]
        return tool_function(inputs)
    
    def understand_question(self, inputs):
        """問題理解ツールの実行"""
        prompt = self.get_understand_question_prompt()
        context = f"Problem: {inputs['question']}\nModel: {inputs.get('model', 'general')}"
        
        response = self.base_model.generate(
            prompt + "\n\n" + context,
            max_tokens=1000,
            temperature=0.1
        )
        return response
    
    def recall_related(self, inputs):
        """関連知識想起ツールの実行"""
        prompt = self.get_recall_related_prompt()
        context = f"Current Problem: {inputs['question']}"
        
        response = self.base_model.generate(
            prompt + "\n\n" + context,
            max_tokens=1500,
            temperature=0.3
        )
        return response
    
    def examine_answer(self, inputs):
        """解答検証ツールの実行"""
        prompt = self.get_examine_answer_prompt()
        context = f"""
        Question: {inputs['question']}
        Current Proposed Answer: {inputs['current_proposed_answer']}
        """
        
        response = self.base_model.generate(
            prompt + "\n\n" + context,
            max_tokens=2000,
            temperature=0.1
        )
        return response
    
    def backtracking(self, inputs):
        """バックトラッキングツールの実行"""
        prompt = self.get_backtracking_prompt()
        context = f"""
        Problem: {inputs['question']}
        Current Reasoning Trace: {inputs['reasoning_trace']}
        """
        
        response = self.base_model.generate(
            prompt + "\n\n" + context,
            max_tokens=1500,
            temperature=0.2
        )
        return response
    
    def use_code(self, inputs):
        """コード実行ツールの実行"""
        prompt = self.get_use_code_prompt()
        context = f"""
        Problem: {inputs['problem']}
        Previous Reasoning: {inputs.get('reasoning', '')}
        """
        
        response = self.base_model.generate(
            prompt + "\n\n" + context,
            max_tokens=1000,
            temperature=0.1
        )
        
        # コード抽出と実行
        code = self.extract_code_from_response(response)
        if code:
            execution_result = self.execute_code_safely(code)
            return f"{response}\n\nExecution Output: {execution_result}"
        
        return response
```

### ツール選択機構

```python
class ToolSelector:
    def __init__(self):
        self.tool_usage_patterns = {
            'understand_question': ['unclear', 'complex', 'ambiguous'],
            'recall_related': ['similar', 'example', 'analogous'],
            'examine_answer': ['verify', 'check', 'validate'],
            'backtracking': ['error', 'mistake', 'wrong', 'incorrect'],
            'use_code': ['calculate', 'compute', 'algorithm']
        }
    
    def suggest_tools(self, current_context, problem_type):
        """現在の文脈に基づいてツールを提案"""
        suggestions = []
        
        # 問題の複雑さに基づく提案
        if self.is_complex_problem(problem_type):
            suggestions.append('understand_question')
        
        # エラー検出時の提案
        if self.detect_potential_error(current_context):
            suggestions.extend(['examine_answer', 'backtracking'])
        
        # 計算が必要な場合の提案
        if self.needs_computation(current_context):
            suggestions.append('use_code')
        
        return suggestions
```

### 実行制御フロー

```python
class CognitiveReasoningPipeline:
    def __init__(self, base_model):
        self.engine = CognitiveToolsEngine(base_model)
        self.selector = ToolSelector()
        self.conversation_history = []
    
    def solve_problem(self, problem):
        """メインの問題解決ループ"""
        # 初期化
        context = {
            'problem': problem,
            'reasoning_trace': '',
            'tool_calls': [],
            'intermediate_results': []
        }
        
        # システムプロンプトで開始
        initial_prompt = self.get_system_prompt() + f"\n\nProblem: {problem}"
        
        max_iterations = 10  # 無限ループ防止
        iteration = 0
        
        while iteration < max_iterations:
            # LLMによる推論ステップ
            response = self.base_model.generate(
                self.build_conversation_context(context),
                max_tokens=1500,
                stop_sequences=['ANSWER:', 'print(']
            )
            
            # ツール呼び出しの検出
            tool_call = self.detect_tool_call(response)
            
            if tool_call:
                # ツール実行
                tool_result = self.engine.execute_tool(
                    tool_call['name'], 
                    tool_call['inputs']
                )
                
                # 結果を文脈に統合
                context['tool_calls'].append(tool_call)
                context['intermediate_results'].append(tool_result)
                context['reasoning_trace'] += f"\n{response}\n\nTool Result:\n{tool_result}\n"
                
            elif 'ANSWER:' in response:
                # 最終答案の検出
                final_answer = self.extract_final_answer(response)
                return {
                    'answer': final_answer,
                    'reasoning_trace': context['reasoning_trace'] + response,
                    'tool_usage': context['tool_calls']
                }
            
            else:
                # 通常の推論継続
                context['reasoning_trace'] += response
            
            iteration += 1
        
        return {'error': 'Maximum iterations reached'}
    
    def detect_tool_call(self, response):
        """レスポンスからツール呼び出しを検出"""
        import re
        
        # Python関数呼び出しパターンの検出
        pattern = r'(\w+)\(\{([^}]+)\}\)'
        matches = re.findall(pattern, response)
        
        for match in matches:
            tool_name, params_str = match
            if tool_name in self.engine.tools:
                try:
                    # パラメータの解析
                    params = eval(f'{{{params_str}}}')
                    return {
                        'name': tool_name,
                        'inputs': params
                    }
                except:
                    continue
        
        return None
```

## 評価システムの実装

### 自動評価パイプライン

```python
class EvaluationSystem:
    def __init__(self, judge_model):
        self.judge_model = judge_model
    
    def evaluate_mathematical_answer(self, predicted, ground_truth, problem_type):
        """数学問題の解答を評価"""
        if problem_type in ['AIME', 'AMC']:
            # 数値解答の直接比較
            return self.numerical_comparison(predicted, ground_truth)
        
        elif problem_type == 'MATH500':
            # LLM判定による評価
            return self.llm_judge_evaluation(predicted, ground_truth)
    
    def numerical_comparison(self, predicted, ground_truth):
        """数値解答の比較"""
        try:
            pred_num = float(self.extract_number(predicted))
            true_num = float(ground_truth)
            return abs(pred_num - true_num) < 1e-6
        except:
            return False
    
    def llm_judge_evaluation(self, predicted, ground_truth):
        """LLM判定による評価"""
        judge_prompt = f"""
        The following two expressions are answers to a math problem. 
        Judge whether they are equivalent.
        
        Expression 1: {predicted}
        Expression 2: {ground_truth}
        
        Respond with only "Yes" or "No".
        """
        
        response = self.judge_model.generate(judge_prompt, max_tokens=5)
        return 'yes' in response.lower()
```

### パフォーマンス測定

```python
class PerformanceMetrics:
    def __init__(self):
        self.results = []
    
    def run_benchmark(self, model, dataset, num_runs=1):
        """ベンチマーク実行"""
        all_results = []
        
        for run in range(num_runs):
            run_results = []
            
            for problem in dataset:
                result = model.solve_problem(problem['question'])
                
                is_correct = self.evaluate_answer(
                    result['answer'], 
                    problem['ground_truth'],
                    problem['type']
                )
                
                run_results.append({
                    'problem_id': problem['id'],
                    'correct': is_correct,
                    'reasoning_trace': result['reasoning_trace'],
                    'tool_usage': result.get('tool_usage', [])
                })
            
            all_results.append(run_results)
        
        return self.compute_statistics(all_results)
    
    def compute_statistics(self, all_results):
        """統計情報の計算"""
        accuracies = []
        
        for run_results in all_results:
            correct_count = sum(1 for r in run_results if r['correct'])
            accuracy = correct_count / len(run_results)
            accuracies.append(accuracy)
        
        mean_accuracy = np.mean(accuracies)
        std_error = np.std(accuracies) / np.sqrt(len(accuracies))
        
        return {
            'mean_accuracy': mean_accuracy,
            'std_error': std_error,
            'individual_runs': accuracies,
            'detailed_results': all_results
        }
```

## 実装上の注意点

### 1. トークン管理
- **文脈長制限**: 各ツールは独立した文脈で動作するため、長い推論履歴の管理が重要
- **効率的なプロンプト**: 必要最小限の情報のみをツールに渡す

### 2. エラーハンドリング
- **ツール実行失敗**: ツールが適切な出力を生成しない場合の対処
- **無限ループ防止**: 同じツールの繰り返し呼び出しの制限

### 3. 拡張性
- **新ツール追加**: モジュラー設計により容易に新しい認知ツールを追加可能
- **ドメイン適応**: 数学以外の領域への適用のための設計考慮

### 4. 最適化
- **並列実行**: 独立性を活用したツールの並列実行
- **キャッシュ機能**: 類似問題に対する結果の再利用

この実装により、認知心理学の理論に基づいた構造化された推論支援システムが構築され、従来の単一プロンプト approach よりも柔軟で効果的な問題解決が可能となります。