# 基本編: Agent SDK の基礎

Agent SDK の最も基本的な使い方を学ぶための2つのデモです。

## 📚 このセクションで学べること

- Agent SDK の基本的な使い方
- `query()` インターフェースの理解
- メッセージタイプとストリーミング
- エージェントの思考過程の可視化

## 🎯 デモ一覧

### 1. hello_agent.py - 最もシンプルな例

**所要時間: 2-3分**

```bash
python examples/01_basic/hello_agent.py
```

**何を学ぶか:**
- Agent SDK の最もシンプルな使い方
- `query()` 関数の基本
- 結果の取得方法

**期待される出力:**
```
==========================================================
Claude Agent SDK - Hello Agent デモ
==========================================================

エージェントに簡単な計算タスクを依頼します...

🎯 エージェントの回答:
------------------------------------------------------------
2 + 2 = 4

この計算は基本的な算術演算です...
------------------------------------------------------------

✅ デモ完了!
```

**コードのポイント:**
```python
# 最もシンプルなエージェント呼び出し
async for message in query(prompt="What is 2 + 2?"):
    if message.type == "result":
        print(message.result)
```

---

### 2. streaming_demo.py - ストリーミングの可視化

**所要時間: 3-5分**

```bash
python examples/01_basic/streaming_demo.py
```

**何を学ぶか:**
- ストリーミング動作の理解
- エージェントの思考過程の観察
- メッセージタイプの種類と活用
- リアルタイム処理

**期待される出力:**
```
┌─ Claude Agent SDK - Streaming Demo ─┐
│ エージェントの思考過程をリアルタイムで観察します │
└─────────────────────────────────────┘

📝 タスク: 以下の計算を順番に実行してください:
    1. 15 × 7 を計算
    2. その結果に 23 を足す
    3. 最終結果を2で割る

💭 思考: まず15 × 7を計算します...
🔧 ツール使用: calculator
💭 思考: 105に23を足します...
🔧 ツール使用: calculator
💭 思考: 128を2で割ります...

┌─ 🎯 最終結果 ─┐
│ 64 │
└───────────────┘
```

**コードのポイント:**
```python
# メッセージタイプごとに異なる処理
async for message in query(prompt=task):
    if message.type == "result":
        print(f"結果: {message.result}")
    elif message.type == "thinking":
        print(f"思考: {message.content}")
    elif message.type == "tool_use":
        print(f"ツール: {message.tool_name}")
```

---

## 🔑 重要な概念

### 1. query() インターフェース

`query()` は Agent SDK の最もシンプルなインターフェースです:

```python
from claude_agent_sdk import query

async for message in query(prompt="タスクの内容"):
    # メッセージを処理
    pass
```

### 2. メッセージタイプ

エージェントは様々なタイプのメッセージを返します:

| タイプ | 説明 | 使い方 |
|--------|------|--------|
| `result` | 最終結果 | `message.result` で内容を取得 |
| `thinking` | 思考過程 | `message.content` で内容を取得 |
| `tool_use` | ツール使用 | `message.tool_name` でツール名を取得 |
| `error` | エラー | `message.error` でエラー内容を取得 |

### 3. 非同期処理

Agent SDK は非同期処理を使用します:

```python
import asyncio

async def main():
    async for message in query(prompt="..."):
        # 処理
        pass

asyncio.run(main())
```

---

## 💡 「すごさ」のポイント

### 1. シンプルなインターフェース

わずか数行のコードでAIエージェントを呼び出せます:

```python
async for message in query(prompt="2 + 2 を計算"):
    if message.type == "result":
        print(message.result)  # → "4"
```

### 2. リアルタイムストリーミング

エージェントの思考過程をリアルタイムで観察できます:
- 何を考えているか
- どのツールを使っているか
- どのように問題を解決しているか

### 3. 自律的な実行

複数ステップのタスクも自律的に実行:
1. タスクを理解
2. 必要な計算を実行
3. 結果を統合して返却

---

## 🚀 次のステップ

基本編を理解したら、次は実用編に進みましょう:

```bash
cd ../02_practical
python project_analyzer.py
```

実用編では、ファイル操作を伴う実践的なタスクに挑戦します。

---

## ❓ トラブルシューティング

### API キーのエラー

```
❌ エラー: ANTHROPIC_API_KEY が設定されていません
```

**解決方法:**
1. `.env.example` を `.env` にコピー
2. `.env` ファイルで `ANTHROPIC_API_KEY=your_key` を設定
3. APIキーは https://console.anthropic.com/ から取得

### インポートエラー

```
ModuleNotFoundError: No module named 'claude_agent_sdk'
```

**解決方法:**
```bash
pip install -r requirements.txt
```

### 環境変数が読み込まれない

**解決方法:**
```bash
# 環境変数を直接設定
export ANTHROPIC_API_KEY="your_api_key_here"

# または .env ファイルのパスを確認
ls -la .env
```

---

## 📖 参考資料

- [Claude Agent SDK 公式ドキュメント](https://docs.claude.com/en/api/agent-sdk/overview)
- [Python SDK リファレンス](https://docs.claude.com/en/api/agent-sdk/python)
- メインREADME: [../../README.md](../../README.md)
