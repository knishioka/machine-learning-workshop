---
marp: true
theme: default
paginate: true
---

# LangChainの永続性: なぜ必要で、どう実現するか

---

## LangChainとは

- 大規模言語モデル（LLM）を使用したアプリケーションを構築するためのフレームワーク
- 複雑なAIタスクを簡単に実装できるようにする
- さまざまなコンポーネントやツールを提供

---

## LangGraphとは

- LangChainの一部として開発されたライブラリ
- 状態を持つマルチアクターアプリケーションを構築するためのツール
- エージェントやマルチエージェントのワークフローを作成可能

---

## なぜ永続性（Persistence）が必要か？

1. **文脈の維持**
   - 複数の対話にわたって会話の文脈を保持
   - ユーザーとの長期的な対話を可能に

2. **状態の管理**
   - アプリケーションの現在の状態を保存
   - 必要に応じて以前の状態に戻る能力

3. **エラーからの回復**
   - 障害発生時に最後の正常な状態から再開可能

---

## 永続性の実現方法：状態保存機能

LangGraphでは、「状態保存機能」を通じて永続性を実現します。

**状態保存機能とは：**
アプリケーションの状態を定期的に保存し、必要に応じて復元する機能

---

## 状態保存機能の主な特徴

1. **セッションメモリ**
   - ユーザーとのやり取りの履歴を保存
   - 保存された状態から会話を再開可能

2. **エラー回復**
   - 最後に成功した保存状態から継続可能
   - システム障害時の影響を最小限に

3. **ヒューマンインザループ**
   - 人間の介入や承認を要する処理の実装
   - AIと人間の協調作業をスムーズに

---

## 状態保存機能の実装

LangGraph v0.2で導入された新しいライブラリ：

- `langgraph_checkpoint`: 基本インターフェース
- `langgraph_checkpoint_sqlite`: 開発・テスト用
- `langgraph_checkpoint_postgres`: 本番環境用

---

## 状態保存機能の使用例

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver

# グラフの構築
builder = StateGraph(...)

# 状態保存機能の初期化
memory = AsyncSqliteSaver.from_conn_string(":memory:")

# グラフのコンパイルと状態保存機能の適用
graph = builder.compile(checkpointer=memory)
```
---
## 状態保存機能の仕組み

<div class="mermaid">
sequenceDiagram
    participant App as LangGraphアプリ
    participant CP as Checkpointer
    participant DB as データベース

    App->>CP: 状態更新
    CP->>DB: シリアライズされた状態を保存

    Note over App,DB: 後で状態を復元する場合

    App->>CP: 状態復元要求
    CP->>DB: 保存された状態を取得
    DB-->>CP: シリアライズされた状態
    CP-->>App: 復元された状態
</div>

<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.0.0/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: true });
window.addEventListener('vscode.markdown.updateContent', function() { mermaid.init() });
</script>

---

## 状態保存機能がもたらす利点

1. **一貫性のある長期的な対話**
   - ユーザーとの会話履歴を保持し、文脈に応じた応答が可能

2. **堅牢なアプリケーション**
   - エラーや中断からの回復が容易

3. **複雑なワークフローの実現**
   - 人間の介入を含む高度な処理フローを構築可能

4. **開発の柔軟性**
   - 様々なデータベースに対応可能
   - カスタム実装の作成が容易

---

## 考慮事項

1. パフォーマンスへの影響
   - 履歴が増えるとLLM呼び出しに時間がかかる可能性

2. カスタマイズの制限
   - 履歴の動的な操作に一部制限あり

3. 実装の選択
   - 使用環境に適した状態保存機能の選択が重要

---

## まとめ

- LangGraphの状態保存機能は、永続性を実現する強力なツール
- 長期的な対話、エラー回復、複雑なワークフローを可能に
- 適切に使用することで、より洗練されたAIアプリケーションの開発が可能

---

## 参考文献

1. [LangGraph公式ドキュメント](https://langchain-ai.github.io/langgraph/)
2. [LangGraph v0.2リリースブログ](https://blog.langchain.dev/langgraph-v0-2/)
3. [LangGraph Persistence How-to](https://langchain-ai.github.io/langgraph/how-tos/persistence/)