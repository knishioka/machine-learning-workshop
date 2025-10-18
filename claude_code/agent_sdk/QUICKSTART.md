# クイックスタートガイド

このガイドに従えば、5分でAgent SDKデモを実行できます。

## ステップ1: 環境準備 (2分)

### 1-1. 仮想環境の作成（推奨）

```bash
# 現在のディレクトリで実行
python -m venv venv

# 仮想環境の有効化
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

### 1-2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

**期待される出力:**
```
Successfully installed claude-agent-sdk-0.1.4 python-dotenv-1.0.0 rich-13.x.x ...
```

## ステップ2: APIキーの設定 (1分)

### 2-1. .envファイルの作成

```bash
cp .env.example .env
```

### 2-2. APIキーの取得と設定

1. https://console.anthropic.com/ にアクセス
2. APIキーを取得（無料トライアルあり）
3. `.env`ファイルを編集:

```bash
# macOS/Linux:
nano .env

# または好きなエディタで開く
code .env
```

`.env`の内容:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
```

**重要:** `your_api_key_here`を実際のAPIキーに置き換えてください。

## ステップ3: 動作確認 (2分)

### 3-1. 最もシンプルなデモを実行

```bash
python examples/01_basic/hello_agent.py
```

**期待される出力:**
```
============================================================
Claude Agent SDK - Hello Agent デモ
============================================================

エージェントに簡単な計算タスクを依頼します...

🎯 エージェントの回答:
------------------------------------------------------------
2 + 2 = 4

2 + 2 は基本的な算術演算で、結果は 4 です。
------------------------------------------------------------

✅ デモ完了！
```

### 3-2. ストリーミングデモを試す

```bash
python examples/01_basic/streaming_demo.py
```

エージェントの思考過程がリアルタイムで表示されます！

## 成功！🎉

これでAgent SDKデモが動作しています。次は：

### 次のステップ

1. **他のデモを試す**
   ```bash
   # プロジェクト分析
   python examples/02_practical/project_analyzer.py .

   # README生成
   python examples/02_practical/readme_generator.py examples/01_basic
   ```

2. **ドキュメントを読む**
   - 各ディレクトリの`README.md`で詳細を学ぶ
   - `docs/PRESENTATION.md`でプレゼン方法を確認
   - `docs/ARCHITECTURE.md`で技術詳細を理解

3. **独自のエージェントを作成**
   - 基本編のコードをベースに改造
   - 自分のユースケースに適用

## トラブルシューティング

### ❌ エラー: `ModuleNotFoundError: No module named 'claude_agent_sdk'`

**原因:** パッケージがインストールされていない

**解決策:**
```bash
pip install -r requirements.txt
```

### ❌ エラー: `ANTHROPIC_API_KEY が設定されていません`

**原因:** APIキーが未設定

**解決策:**
1. `.env`ファイルが存在するか確認: `ls -la .env`
2. `.env`の内容を確認: `cat .env`
3. APIキーが正しく設定されているか確認

### ❌ エラー: `AuthenticationError`

**原因:** APIキーが無効または期限切れ

**解決策:**
1. https://console.anthropic.com/ で新しいキーを取得
2. `.env`を更新

### ⚠️ 警告: `DeprecationWarning`

通常は問題ありません。デモは動作します。

### 🐌 動作が遅い

**原因:** ネットワーク接続やAPI応答の遅延

**対処:**
- インターネット接続を確認
- 数秒待ってから再試行
- 応用編のデモは10-30秒かかる場合があります

## 実行環境の確認

以下のコマンドで環境を確認できます:

```bash
# Pythonバージョン（3.8以上が必要）
python --version

# インストールされたパッケージ
pip list | grep -E "claude|dotenv|rich"

# .envファイルの存在確認
ls -la .env

# 構文チェック
python -m py_compile examples/01_basic/hello_agent.py
```

## 詳細情報

- メインREADME: [README.md](README.md)
- プレゼン資料: [docs/PRESENTATION.md](docs/PRESENTATION.md)
- アーキテクチャ: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 公式ドキュメント: https://docs.claude.com/en/api/agent-sdk/overview

---

**楽しいAgent SDK体験を！ 🚀**
