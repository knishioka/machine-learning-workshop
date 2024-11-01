---
marp: true
theme: default
paginate: true
---

# LangGraph Templatesによる<br />効率的なワークフロー構築
### 2024/10/26 機械学習の社会実装勉強会 第40回
<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>

---
# LangGraph Studio Template

---
## LangGraph Template

- LangGraph Templateは、PythonとJavaScriptで利用可能なテンプレートレポジトリ
- 実体はGitHub上のリポジトリ: (langgraph:///template?githubUrl=https%3A%2F%2Fgithub.com%2Flangchain-ai%2Freact-agent)
![width:400px center](images/langgraph_studio_template.png)



---
## なぜLangGraph Templateが必要か？

- **簡単な導入とカスタマイズ**: テンプレートは、リポジトリをクローンすることで内部の機能を簡単に修正できるため、プロンプトやロジックの変更が容易
- **デバッグと展開のしやすさ**: テンプレートはLangGraph Studioでデバッグし、ワンクリックでLangGraph Cloudに展開できる構造
- **高いカスタマイズ性**: エージェントの内部コードを自由に変更できるため、開発者が自分のニーズに合わせた詳細な制御可能

---
## 現在提供されているTemplate

- New LangGraph Project: https://github.com/langchain-ai/new-langgraph-project
- Langchain Memory Agent: https://github.com/langchain-ai/memory-agent
- Data Enrichment: https://github.com/langchain-ai/data-enrichment
- React Agent: https://github.com/langchain-ai/react-agent
- Retrieval Agent Template: https://github.com/langchain-ai/retrieval-agent-template

---
## New LangGraph Project
**概要**:  
LangGraph Studio用にデザインされたChatBot。永続的なチャットメモリを保持。

**機能**:
- ノードとエッジで表現されるデータフローの可視化
- 複雑なワークフローを細かく制御できるカスタマイズ性
- エージェントの組織化と管理

**利点**:
- テンプレートを活用した迅速な開発
- Studioでのデバッグとクラウドへのワンクリック展開

---
## Langchain Memory Agent
**概要**:  
過去のやり取りや状態を記憶し、長期タスクや対話の継続を可能にするエージェント

**機能**:
- 会話やタスクの履歴を記憶するメモリ機能
- 過去の情報を利用してインタラクションを最適化
- 長期タスクや複雑な対話の管理

**利点**:
- パーソナライズされたやり取りの実現
- タスクの進行状況に応じた応答の提供
- 長期的な対話に適した設計

---
## Data Enrichment
**概要**:  
外部情報を使って既存データを補完・強化するエージェント

**機能**:
- 外部APIやデータソースからの情報取得
- 取得データの分析と統合
- 自動的なデータ補完プロセス

**利点**:
- データの価値と精度の向上
- 研究やデータ収集に適した設計
- 複数のデータソースを活用した情報の強化

---
## React Agent
**概要**:  
リアルタイムで環境の変化に反応し、動的に行動するエージェント

**機能**:
- 状況に応じたリアルタイム応答
- 環境変化に基づく動的な意思決定
- タスクを繰り返し実行し、適切なツールを選択

**利点**:
- リアルタイム処理が必要なアプリケーションに最適
- 環境に即応するインタラクティブなエージェント設計
- 高い応答性

---
## Retrieval Agent Template
**概要**:  
情報取得に特化したエージェントのテンプレート

**機能**:
- クエリに基づくデータ検索と取得
- 外部ソースや特定のデータセットからの情報抽出
- 検索結果の最適化と自動化

**利点**:
- カスタマイズ可能な情報取得エージェントの作成
- データ検索と取得プロセスの効率化
- 特定データソースに簡単に適応