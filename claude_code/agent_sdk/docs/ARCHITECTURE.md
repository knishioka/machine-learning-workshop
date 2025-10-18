# Claude Agent SDK アーキテクチャ詳解

Agent SDK の内部アーキテクチャと設計思想を深く理解するためのドキュメントです。

---

## 📐 全体アーキテクチャ

### システム構成

```
┌─────────────────────────────────────────────┐
│           User Application                   │
│  (あなたのPython/TypeScriptコード)           │
└────────────────┬────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────┐
│        Claude Agent SDK (Core)              │
├─────────────────────────────────────────────┤
│  • Query Interface                          │
│  • Message Streaming                        │
│  • Context Management                       │
│  • Tool Orchestration                       │
└────────┬─────────────────┬──────────────────┘
         │                 │
         v                 v
┌────────────────┐  ┌─────────────────────┐
│  Claude API    │  │  Built-in Tools     │
│  (Anthropic)   │  │  • Glob             │
│                │  │  • Read             │
│                │  │  • Write            │
│                │  │  • WebSearch        │
│                │  │  • Bash             │
└────────────────┘  └──────────┬──────────┘
                               │
                               v
                    ┌──────────────────────┐
                    │  MCP Servers         │
                    │  (External Tools)    │
                    │  • GitHub            │
                    │  • Slack             │
                    │  • Database          │
                    │  • Custom...         │
                    └──────────────────────┘
```

---

## 🔄 エージェントループ

Agent SDK の核心である「エージェントループ」の詳細。

### ループの4フェーズ

```
1. Plan (計画)
   ↓
2. Execute (実行)
   ↓
3. Observe (観察)
   ↓
4. Reflect (反省)
   ↓
   ループまたは終了
```

### 具体例: プロジェクト分析タスク

```python
task = "プロジェクトを分析してレポート生成"
```

**エージェントの内部思考:**

```
Iteration 1:
  Plan:    「まずPythonファイルを探そう」
  Execute: Glob("*.py")
  Observe: "10個のファイルが見つかった"
  Reflect: "主要なファイルの内容を読むべきだ"

Iteration 2:
  Plan:    「README.mdとmain.pyを読もう」
  Execute: Read("README.md"), Read("main.py")
  Observe: "プロジェクトの目的とメイン処理を理解した"
  Reflect: "統計情報も必要だ"

Iteration 3:
  Plan:    「ファイルサイズと行数を計算しよう」
  Execute: 各ファイルを分析
  Observe: "統計データが揃った"
  Reflect: "レポートをまとめられる"

Iteration 4:
  Plan:    "構造化されたレポートを生成"
  Execute: レポート作成
  Observe: "完成した"
  Reflect: "タスク完了"
  → 終了
```

### ループ制御のメカニズム

Agent SDK は以下の方法でループを制御:

1. **コンテキスト分析**: 現在の状況を評価
2. **目標との比較**: 目標達成度を判定
3. **次アクション決定**: 必要なツールと引数を決定
4. **終了判定**: 目標達成または制約達成で終了

---

## 💾 コンテキスト管理

長期実行でもコンテキスト上限を超えない仕組み。

### 問題: コンテキストウィンドウの制限

Claude APIには最大コンテキストサイズがあります（例: 200Kトークン）。
長期実行すると:
- 会話履歴が増加
- ツール出力が蓄積
- ファイル内容が追加
→ コンテキスト上限を超える

### 解決策: 自動コンテキスト管理

Agent SDK は自動的に:

1. **要約生成**: 古い会話を要約
2. **不要な削除**: 使われなくなった情報を削除
3. **優先順位付け**: 重要な情報を保持
4. **圧縮**: 類似情報をまとめる

**例:**

```
初期状態 (5K tokens):
  - User: "プロジェクトを分析"
  - Assistant: "承知しました"
  - Tool: Glob結果 (100ファイル)
  - Tool: Read("file1.py")
  - ...

中間状態 (50K tokens):
  - [要約] 最初の10ファイルの分析結果
  - Tool: Read("file11.py")
  - ...

後期状態 (180K tokens):
  - [要約] ファイル構造の概要
  - [要約] 主要な発見事項
  - 現在のタスク: レポート生成
  - ...
```

### コンテキスト最適化の戦略

```python
# SDK内部の疑似コード
def optimize_context(messages, max_tokens):
    if count_tokens(messages) < max_tokens * 0.8:
        return messages  # まだ余裕あり

    # 最適化が必要
    optimized = []

    # 1. システムプロンプトは保持
    optimized.append(messages[0])

    # 2. 最新のN個のメッセージは保持
    recent = messages[-10:]

    # 3. 中間部分を要約
    middle = messages[1:-10]
    summary = summarize(middle)
    optimized.append(summary)

    # 4. 最新メッセージを追加
    optimized.extend(recent)

    return optimized
```

---

## 🔧 ツールオーケストレーション

複数のツールを効率的に組み合わせる仕組み。

### ツールの種類

**1. ファイル操作系**
- `Glob`: パターンマッチングでファイル検索
- `Read`: ファイル内容の読み取り
- `Write`: ファイルの書き込み
- `Edit`: ファイルの編集

**2. 情報収集系**
- `WebSearch`: インターネット検索
- `WebFetch`: Webページ取得

**3. 実行系**
- `Bash`: シェルコマンド実行
- `Python`: Pythonコード実行

**4. MCP系**
- 外部MCPサーバーが提供するツール

### ツール実行のフロー

```
1. エージェントがツール使用を決定
   ↓
2. ツール名と引数を指定
   ↓
3. SDK がツール実行を検証
   • 権限チェック (allowedTools)
   • 引数バリデーション
   • レート制限チェック
   ↓
4. ツール実行
   ↓
5. 結果をコンテキストに追加
   ↓
6. エージェントに制御を返す
```

### ツール実行の並列化

Agent SDK は複数のツールを並列実行可能:

```python
# エージェントの内部判断（疑似コード）
if can_parallelize([tool1, tool2, tool3]):
    results = await asyncio.gather(
        execute_tool(tool1),
        execute_tool(tool2),
        execute_tool(tool3)
    )
else:
    # 依存関係がある場合は順次実行
    result1 = await execute_tool(tool1)
    result2 = await execute_tool(tool2, depends_on=result1)
```

**例: プロジェクト分析**

```
並列実行可能:
- Read("README.md")
- Read("setup.py")
- Read("requirements.txt")
→ 同時に実行して高速化

順次実行が必要:
- Glob("*.py")  ← まず実行
- Read(glob結果[0])  ← Globの結果が必要
```

---

## 🔐 セキュリティモデル

### 権限管理の階層

```
Level 1: allowedTools (ツールレベル制御)
  └→ どのツールを使えるか

Level 2: Tool Parameters (パラメータレベル制御)
  └→ ツールの使い方の制限

Level 3: Environment (環境レベル制御)
  └→ cwd, 環境変数など

Level 4: MCP Configuration (統合レベル制御)
  └→ 外部サービスの権限
```

### 安全な設定例

**読み取り専用エージェント:**
```python
options={
    "allowedTools": ["Glob", "Read", "WebSearch"],
    # Write, Edit, Bash は許可しない
    "cwd": "/safe/readonly/directory"
}
```

**制限付き書き込みエージェント:**
```python
options={
    "allowedTools": ["Glob", "Read", "Write"],
    "cwd": "/safe/output/directory",  # 出力先を制限
    # Bash は許可しない（コマンド実行防止）
}
```

**フル権限エージェント（注意）:**
```python
options={
    "allowedTools": ["*"],  # すべてのツール
    # 本番環境では非推奨
}
```

### サンドボックス実行

MCPサーバーは独立したプロセスで実行:
- Agent SDK とは別プロセス
- 通信はJSON-RPC over stdio
- クラッシュしてもSDKに影響なし
- リソース制限を設定可能

---

## 📊 メッセージプロトコル

Agent SDK とアプリケーション間のメッセージフォーマット。

### メッセージタイプ

**1. result (最終結果)**
```python
{
    "type": "result",
    "result": "タスク完了。レポートを生成しました。"
}
```

**2. thinking (思考過程)**
```python
{
    "type": "thinking",
    "content": "まずPythonファイルを検索します..."
}
```

**3. tool_use (ツール使用)**
```python
{
    "type": "tool_use",
    "tool_name": "Glob",
    "input": {"pattern": "*.py"},
    "id": "tool_call_123"
}
```

**4. tool_result (ツール結果)**
```python
{
    "type": "tool_result",
    "tool_use_id": "tool_call_123",
    "content": ["file1.py", "file2.py", ...]
}
```

**5. error (エラー)**
```python
{
    "type": "error",
    "error": "ファイルが見つかりません",
    "code": "FILE_NOT_FOUND"
}
```

### メッセージフロー例

```
User → SDK: query("プロジェクト分析")
  ↓
SDK → User: {"type": "thinking", ...}
  ↓
SDK → Tool: Glob("*.py")
  ↓
Tool → SDK: [ファイルリスト]
  ↓
SDK → User: {"type": "tool_use", "tool_name": "Glob", ...}
  ↓
SDK → User: {"type": "thinking", ...}
  ↓
SDK → Tool: Read("main.py")
  ↓
Tool → SDK: [ファイル内容]
  ↓
SDK → User: {"type": "tool_use", "tool_name": "Read", ...}
  ↓
SDK → User: {"type": "result", "result": "分析完了！"}
```

---

## 🚀 パフォーマンス最適化

### 1. ストリーミングの利点

**従来のバッチ処理:**
```
[待機...]  → 30秒後に全結果
```

**ストリーミング:**
```
0秒: "タスク開始"
2秒: "ファイル検索中"
5秒: "10ファイル発見"
8秒: "分析中..."
30秒: "完了"
```

ユーザー体験が劇的に向上。

### 2. キャッシング戦略

Agent SDK は以下をキャッシュ:
- ファイル内容（同じファイルを複数回読まない）
- Web検索結果（同じクエリを複数回実行しない）
- ツール出力（同じツール呼び出しを複数回実行しない）

### 3. バッチ処理の最適化

複数の類似操作をバッチ化:

```python
# 非効率
for file in files:
    read(file)

# 効率的（SDK内部）
batch_read(files)  # 一度に複数ファイル読み取り
```

---

## 🔮 将来の拡張性

Agent SDK のアーキテクチャは以下の拡張を想定:

### 1. マルチエージェント協調

```
┌─────────────┐
│ Main Agent  │
└──────┬──────┘
       │
       ├→ Research Agent (情報収集専門)
       ├→ Code Agent (コード生成専門)
       └→ Review Agent (品質チェック専門)
```

### 2. 永続的メモリ

```
Agent + Vector Database
  └→ 過去の実行履歴を学習
  └→ 類似タスクの効率化
  └→ ユーザー好みの学習
```

### 3. 高度なツールチェーン

```
Tool Composition:
  Glob → Read → Analyze → Write
                  ↓
              Custom Tool
```

---

## 📚 参考アーキテクチャパターン

Agent SDK は以下のパターンを採用:

1. **Chain of Responsibility**: ツール実行チェーン
2. **Strategy Pattern**: ツール選択戦略
3. **Observer Pattern**: メッセージストリーミング
4. **Adapter Pattern**: MCPプロトコル統合
5. **Circuit Breaker**: エラーハンドリング

---

## 🔍 デバッグとモニタリング

### ログレベル

```python
# 環境変数で設定
LOG_LEVEL=DEBUG python agent.py

# 出力例
[DEBUG] Tool selection: Glob
[DEBUG] Tool execution: Glob(pattern="*.py")
[DEBUG] Tool result: 10 files
[DEBUG] Next action: Read files
[INFO] Task completed
```

### メトリクス

監視すべき指標:
- ツール呼び出し回数
- コンテキストサイズ
- 実行時間
- エラー率
- トークン使用量

---

## まとめ

Agent SDK のアーキテクチャは:

✅ **モジュラー**: 各コンポーネントが独立
✅ **拡張可能**: MCPで無限に拡張
✅ **効率的**: キャッシング、並列化、ストリーミング
✅ **安全**: 多層の権限管理
✅ **透明**: すべてのアクションが可視化

この設計により、シンプルなAPIで強力なエージェントを構築できます。

---

**関連ドキュメント:**
- [README.md](../README.md): プロジェクト概要
- [PRESENTATION.md](PRESENTATION.md): プレゼン資料
- 各デモのREADME.md: 具体的な使用例
