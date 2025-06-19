# LangGraph ToolNode の詳細説明

## ToolNode とは

`ToolNode` は LangGraph の事前構築されたコンポーネントで、AIMessage 内の tool_calls を自動的に実行するノードです。

## 主な特徴

1. **自動ツール実行**: 最後の AIMessage に含まれる tool_calls を検出して実行
2. **並列実行**: 複数のツール呼び出しがある場合、並列で実行
3. **メッセージ管理**: ツールの実行結果を ToolMessage として state の messages に追加

## 現在の実装での使用方法

```python
# reasoning_graph.py での使用例
from langgraph.prebuilt import ToolNode

class CognitiveReasoningGraph:
    def _build_graph(self) -> StateGraph:
        graph = StateGraph(CognitiveReasoningState)
        
        # ToolNode を作成してグラフに追加
        graph.add_node("tools", ToolNode(self.tools))
        
        # 条件付きエッジでツール実行を制御
        graph.add_conditional_edges(
            "reason",
            self._should_continue,
            {
                "tools": "tools",  # tool_calls がある場合
                "check": "check_solution",
                "end": END
            }
        )
```

## 動作フロー

1. **LLM がツールを呼び出し決定**
   ```python
   response = self.llm.bind_tools(self.tools).invoke(messages)
   ```

2. **tool_calls の検出**
   ```python
   if hasattr(last_message, "tool_calls") and last_message.tool_calls:
       return "tools"  # ToolNode へルーティング
   ```

3. **ToolNode が自動実行**
   - tool_calls から関数名と引数を抽出
   - 対応するツールを実行
   - 結果を ToolMessage として返す

4. **結果の統合**
   - ToolMessage が state.messages に追加される
   - グラフは次のノード（通常は reason ノード）へ遷移

## メリット

1. **簡潔な実装**: ツール実行のボイラープレートコードが不要
2. **エラーハンドリング**: ツール実行エラーを自動的に処理
3. **型安全性**: Pydantic スキーマによる引数検証
4. **並列実行**: 複数ツールの効率的な実行

## 注意点

1. **メッセージ形式**: AIMessage に tool_calls が必要
2. **状態管理**: messages キーが state に必要
3. **ツールバインディング**: LLM に tools を bind_tools() で事前バインド必要

## カスタマイズが必要な場合

ToolNode のデフォルト動作で不十分な場合は、カスタムノードを実装：

```python
def custom_tool_node(state):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls"):
        for tool_call in last_message.tool_calls:
            # カスタムロジック
            tool_result = execute_tool_custom(tool_call)
            # 状態の更新
            state["custom_field"] = process_result(tool_result)
    return state
```