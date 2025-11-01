# 機械学習の社会実装勉強会
毎月開催している[機械学習の社会実装勉強会](https://machine-learning-workshop.connpass.com/)で利用したスクリプトなどを共有するレポジトリ。

## セットアップ

このプロジェクトでは[uv](https://github.com/astral-sh/uv)を使用してPythonパッケージを管理しています。

### 前提条件
- Python 3.10以上
- uvのインストール

### uvのインストール
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# または pipを使用
pip install uv
```

### 環境構築
```bash
# リポジトリのクローン
git clone https://github.com/your-username/machine-learning-workshop.git
cd machine-learning-workshop

# 仮想環境の作成
uv venv

# 仮想環境の有効化
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 依存関係のインストール
uv pip install -r <(sed -n '/dependencies = \[/,/\]/p' pyproject.toml | grep -E '^\s*"' | sed 's/.*"\(.*\)".*/\1/' | grep -v '^#')

# 開発用依存関係のインストール（オプション）
uv pip install 'pytest>=7.4.0' 'pytest-asyncio>=0.21.0' 'pytest-cov>=4.1.0' 'black>=24.0.0' 'ruff>=0.5.0' 'mypy>=1.5.0' 'isort>=5.12.0' 'pre-commit>=3.5.0'
```

### オプションの依存関係
プラットフォーム固有のパッケージは以下のようにインストールできます：
```bash
# MXNet（x86_64プラットフォームのみ）
uv pip install 'mxnet>=1.9.1'

# 完全なAutoGluon（MXNetが必要）
uv pip install 'autogluon>=1.1.1'

# CUDA対応パッケージ（GPUが必要）
uv pip install 'bitsandbytes>=0.43.0'
```

## Claude Skills

このプロジェクトには、機械学習ワークフローを効率化するためのClaude Codeスキルが含まれています。

### 利用可能なスキル

1. **ml-experiment-setup**: 機械学習実験のセットアップ支援
2. **model-evaluation-report**: モデル評価レポートの生成
3. **data-analysis-starter**: データ分析の開始テンプレート
4. **deployment-checklist**: モデルデプロイメントのチェックリストとコード生成
5. **ml-weekly-report**: 週次性能レポートの自動生成（定期レポート作成）
6. **stakeholder-presentation**: ステークホルダー向けプレゼンテーション自動生成（PowerPoint形式）

### 使い方

Claude Codeを使用している場合、これらのスキルは自動的に利用可能になります。タスクに応じてClaudeが適切なスキルを自動選択します。

詳細な使用方法とカスタマイズについては、[.claude/skills/README.md](.claude/skills/README.md)を参照してください。

### 例

```
# ml-experiment-setupスキルが自動起動
「PyTorchで画像分類の実験を始めたい」

# model-evaluation-reportスキルが自動起動
「訓練したモデルの性能評価レポートを作成して」

# data-analysis-starterスキルが自動起動
「新しいCSVファイルのデータ分析を始めたい」

# deployment-checklistスキルが自動起動
「このモデルを本番環境にデプロイしたい」

# ml-weekly-reportスキルが自動起動
「先週のモデル性能レポートを作成して」

# stakeholder-presentationスキルが自動起動
「経営会議用にプロジェクト進捗のプレゼンを作成して」
```

## 過去の勉強会のスクリプト
- [LangGraphを用いたAIアプリケーションにおけるメモリ永続化の実践 (機械学習の社会実装勉強会第38回)](https://speakerdeck.com/knishioka/langgraphwoyong-itaaiapurikesiyonniokerumemoriyong-sok-hua-noshi-jian)
    - [langchain/langchain_persistence.ipynb](langchain/langchain_persistence.ipynb)
- [Text-to-SQLをLangSmithで評価 (機械学習の社会実装勉強会第37回)](https://speakerdeck.com/knishioka/text-to-sqlwolangsmithdeping-jia)
    - [langchain/langsmith_text-to-sql.ipynb](langchain/langsmith_text-to-sql.ipynb)
- [効果的なLLM評価法 LangSmithの技術と実践 (機械学習の社会実装勉強会第36回)](https://speakerdeck.com/knishioka/xiao-guo-de-nallmping-jia-fa-langsmithnoji-shu-toshi-jian)
    - [langchain/langsmith_evaluation.ipynb](langchain/langsmith_evaluation.ipynb)
- [LangGraphのノード・エッジ・ルーティングを深堀り (機械学習の社会実装勉強会第35回)](https://speakerdeck.com/knishioka/langgraphnonodoetuziruteinguwoshen-ku-ri)
    - [langchain/LangGraph Node, Edge, Routing.ipynb](langchain/LangGraph%20Node,%20Edge,%20Routing.ipynb)
- [LangGraphでマルチエージェントワークフローを構築 (機械学習の社会実装勉強会第34回)](https://speakerdeck.com/knishioka/langgraphdemarutiezientowakuhurowogou-zhu)
    - [langchain/langgraph.ipynb](langchain/langgraph.ipynb)
- [LLMアプリケーションで使用するVector Databaseの比較 (機械学習の社会実装勉強会第33回)](https://speakerdeck.com/knishioka/llmapurikesiyondeshi-yong-suruvector-databasenobi-jiao)
    - [langchain/vector_databases.ipynb](langchain/vector_databases.ipynb)
- [LLMアプリケーションの デバッグ・テスト・評価・監視を楽にするLangSmith (機械学習の社会実装勉強会第32回)](https://speakerdeck.com/knishioka/llmapurikesiyonno-debatugutesutoping-jia-jian-shi-wole-nisurulangsmith)
    - [langchain/langsmith.ipynb](langchain/langsmith.ipynb)
- [LangChainから学ぶプロンプトエンジニアリングテクニック (機械学習の社会実装勉強会第31回)](https://speakerdeck.com/knishioka/langchainkaraxue-bupuronputoenziniaringutekunituku)
- [チャット履歴と質問を組み合わせLLMの回答精度を高めるLangChain Conversational Retrieval QA (機械学習の社会実装勉強会第30回)](https://speakerdeck.com/knishioka/tiyatutolu-li-tozhi-wen-wozu-mihe-wasellmnohui-da-jing-du-wogao-merulangchain-conversational-retrieval-qa)
    - [langchain/ConversationalRetrievalChain.ipynb](langchain/ConversationalRetrievalChain.ipynb)
- [LangChain RetrievalQAとChatGPTでQAツールを作る (機械学習の社会実装勉強会第29回)](https://speakerdeck.com/knishioka/langchain-retrievalqatochatgptdeqaturuwozuo-ru)
    - [langchain/RetrievalQA.ipynb](langchain/RetrievalQA.ipynb)
- [LangChainのDocument機能を使って文書処理を柔軟にする (機械学習の社会実装勉強会第28回)](https://speakerdeck.com/knishioka/langchainnodocumentji-neng-woshi-tutewen-shu-chu-li-worou-ruan-nisuru)
    - [langchain/question_and_summarize.ipynb](langchain/question_and_summarize.ipynb)
- [LangChain Agentを使って自社ツールとChatGPTを連携 (機械学習の社会実装勉強会第27回)](https://speakerdeck.com/knishioka/langchain-agentwoshi-tutezi-she-turutochatgptwolian-xi)
    - [langchain/langchain_agent_custom_tools.ipynb](langchain/langchain_agent_custom_tools.ipynb)
- [LLMを使ったサービス開発必須ライブリ 「LangChain」の基礎 (機械学習の社会実装勉強会第26回)](https://speakerdeck.com/knishioka/llmwoshi-tutasabisukai-fa-bi-xu-raiburi-langchain-noji-chu)
    - [langchain/langchain_agent.ipynb](langchain/langchain_agent.ipynb)
