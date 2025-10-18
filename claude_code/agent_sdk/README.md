# Claude Agent SDK デモプロジェクト

Claude Agent SDK の能力を段階的に理解し、そのポテンシャルを実感できる包括的なデモ集です。

## 🎯 このプロジェクトについて

2025年9月29日にリリースされた **Claude Agent SDK**（旧 Claude Code SDK）は、Anthropic が自社製品（Claude Code 等）を構築するために使用しているエージェントインフラを開発者に提供するフレームワークです。コーディング支援だけでなく、リサーチ、分析、自動化など、幅広いタスクで自律的なAIエージェントを構築できます。このデモプロジェクトでは、基本から応用まで段階的にAgent SDKの「すごさ」を体験できます。

## ✨ Agent SDK の主な特徴

1. **エージェントループ**: コンテキスト収集 → アクション実行 → 検証 → 繰り返し
2. **自動コンテキスト管理**: 長期実行でもコンテキスト上限を自動回避
3. **豊富なツールセット**: ファイル操作、Web検索、コード実行など
4. **MCP連携**: 外部サービスとの拡張可能な統合
5. **ストリーミング対応**: リアルタイムでエージェントの思考過程を可視化

## 📁 プロジェクト構成

```
agent_sdk/
├── examples/
│   ├── 01_basic/          # 基本編: Agent SDKの基礎を理解
│   ├── 02_practical/      # 実用編: ファイル操作の威力を体験
│   ├── 03_advanced/       # 応用編: 自律的マルチステップ実行
│   └── 04_mcp/           # MCP連携編: 拡張性を実証
├── demo/                  # 全デモを一括実行
└── docs/                  # プレゼン資料とアーキテクチャ解説
```

## 🚀 セットアップ

### 1. Python環境の準備

Python 3.8以上が必要です。

```bash
# 仮想環境の作成（推奨）
python -m venv venv

# 仮想環境の有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. API キーの設定

```bash
# .env.example をコピー
cp .env.example .env

# .envファイルを編集して、ANTHROPIC_API_KEYを設定
# APIキーは https://console.anthropic.com/ から取得
```

### 3. 動作確認

```bash
# 基本編の最初のデモを実行
python examples/01_basic/hello_agent.py
```

## 📚 デモの進め方

### レベル1: 基本編（examples/01_basic/）

**所要時間: 5-10分**

- `hello_agent.py`: 最もシンプルなエージェント
- `streaming_demo.py`: ストリーミング動作の可視化

**学べること:**
- Agent SDKの基本的な使い方
- queryインターフェースの理解
- メッセージタイプとストリーミング

**実行例:**
```bash
python examples/01_basic/hello_agent.py
```

**期待される動作:**
```
🎯 エージェントの回答:
------------------------------------------------------------
2 + 2 = 4

This is a basic arithmetic addition operation...
------------------------------------------------------------
✅ デモ完了！
```

### レベル2: 実用編（examples/02_practical/）

**所要時間: 10-15分**

- `project_analyzer.py`: プロジェクト構造の自動分析
- `readme_generator.py`: コードから自動README生成

**学べること:**
- ファイル操作ツール（Glob, Read, Write）の活用
- 複雑なタスクの自動化
- ツール権限管理

**実行例:**
```bash
python examples/02_practical/project_analyzer.py examples/01_basic
```

**期待される動作:**
```
💬 プロジェクト構造の分析を開始します...
🔧 Glob を使用中...（ファイル検索）
🔧 Read を使用中...（ファイル読取）
🔧 Bash を使用中...（統計取得）

📊 分析レポート:
- Python ファイル: 2つ（合計234行）
- 高品質なドキュメント
- 優れたコード品質
✅ 分析完了！
```

エージェントが自律的に必要なツールを選択し、プロジェクト全体を分析します。

### レベル3: 応用編（examples/03_advanced/）

**所要時間: 15-20分**

- `research_agent.py`: Web検索→分析→レポート生成
- `code_reviewer.py`: コード分析→改善提案→実装

**学べること:**
- マルチステップの自律的実行
- エージェントループの威力
- 複数ツールの組み合わせ

**実行例:**
```bash
python examples/03_advanced/research_agent.py "2025年のAI技術トレンド"
```

**期待される動作:**
```
🔍 リサーチを開始します...
🌐 Web検索を実行中...（WebSearchツール）
💭 検索結果を分析しています...
🌐 追加のWeb検索を実行中...（必要に応じて）
💭 情報を統合しています...
📝 レポートを作成中...（Writeツール）
✅ レポートが保存されました: research_report_20251018.md
```

エージェントが自律的に情報収集→分析→レポート作成を実行します。

### レベル4: MCP連携編（examples/04_mcp/）

**所要時間: 15-20分**

- `mcp_example.py`: 外部サービス連携の実例

**学べること:**
- MCPの基本概念
- 拡張性の高いエージェント設計
- カスタムツールの追加方法

## 🎬 デモ実行

### 個別実行

各ディレクトリのREADME.mdを参照して、個別にデモを実行できます。

### 一括実行

全デモを順番に実行するには:

```bash
python demo/run_all_demos.py
```

## 📖 追加資料

- [PRESENTATION.md](docs/PRESENTATION.md): プレゼン用資料（各デモの「すごさ」解説）
- [ARCHITECTURE.md](docs/ARCHITECTURE.md): Agent SDKのアーキテクチャ詳細

## 🔗 参考リンク

- [Claude Agent SDK 公式ドキュメント](https://docs.claude.com/en/api/agent-sdk/overview)
- [Python SDK リポジトリ](https://github.com/anthropics/claude-agent-sdk-python)
- [Anthropic API コンソール](https://console.anthropic.com/)

## 💡 ヒント

- 各デモは独立しているので、興味のある部分から試せます
- コード内のコメントを読むと、動作原理が理解できます
- エラーが出た場合は、APIキーの設定を確認してください
- デモ・プレゼンで使う場合は、docs/PRESENTATION.mdを参照してください

## 📝 ライセンス

このデモプロジェクトは学習・デモ目的で自由に使用できます。

---

**作成日**: 2025年10月
**Agent SDK バージョン**: 0.1.x（検証済み: 0.1.4）
**公式発表**: 2025年9月29日（Claude Sonnet 4.5と同時リリース）
