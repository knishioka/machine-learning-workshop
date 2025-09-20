# 📚 Claude Code で利用規約を自動生成する - ワークショップ教材

## 🎯 概要

このワークショップでは、Claude Codeのサブエージェントとスラッシュコマンドを活用して、法的に準拠した利用規約（Terms of Service）を自動生成する方法を学びます。

### 学習目標
- Claude Codeのサブエージェント機能の理解
- スラッシュコマンドの実装と活用
- 専門分野別AIエージェントの設計
- 複雑な文書生成タスクの自動化

---

## 🏗️ システムアーキテクチャ

```
┌─────────────────────┐         ┌──────────────────────┐
│  Slash Commands     │  ──►    │  Specialized Agents  │
├─────────────────────┤         ├──────────────────────┤
│ /terms-of-service   │         │ legal-compliance     │
│ /tos-wizard         │         │ risk-assessor        │
│ /tos-check          │         │ competitor-analyzer  │
│ /tos-update         │         └──────────────────────┘
└─────────────────────┘
```

---

## 📁 プロジェクト構造

```
claude_code/
├── README.md                     # このファイル
├── DEMO_FLOW.md                 # デモ実演の手順
├── terms-of-service.md          # 生成された利用規約サンプル
├── improved-terms-of-service.md # 改善版利用規約
└── .claude/
    ├── agent-architecture.md    # システム設計書
    ├── commands/
    │   ├── terms-of-service.md # メインコマンド
    │   ├── tos-wizard.md       # ウィザードコマンド
    │   ├── tos-check.md        # 検証コマンド
    │   └── tos-update.md       # 更新コマンド
    └── agents/
        ├── legal-compliance-reviewer.md # 法的準拠エージェント
        ├── risk-assessor.md            # リスク評価エージェント
        └── competitor-analyzer.md      # 競合分析エージェント
```

---

## 🤖 サブエージェント詳細

### 1. legal-compliance-reviewer
**目的**: 法的コンプライアンスの確保

**主な機能**:
- GDPR/CCPA準拠チェック
- 必須開示事項の検証
- 管轄地域別の法的要件確認
- コンプライアンススコアの算出

**使用例**:
```bash
# エージェントが自動的に法的リスクを特定
"legal-compliance-reviewerを使用して規約をレビューしてください"
```

### 2. risk-assessor
**目的**: リスク評価と責任制限の最適化

**主な機能**:
- 責任上限の適切性評価
- 補償条項のバランス分析
- 執行可能性の検証
- 財務影響の算定

**使用例**:
```bash
# リスクスコアと改善提案を生成
"risk-assessorでリスク評価を実行"
```

### 3. competitor-analyzer
**目的**: 業界標準とベストプラクティスの調査

**主な機能**:
- 競合他社の規約分析
- 業界標準の特定
- 差別化ポイントの提案
- 市場トレンドの把握

**使用例**:
```bash
# 市場分析と推奨事項を提供
"competitor-analyzerで競合分析を実施"
```

---

## 💻 スラッシュコマンド使用方法

### /terms-of-service
**完全な利用規約生成コマンド**

```bash
/terms-of-service create --type saas --compliance gdpr,ccpa

# オプション:
--type: サービスタイプ (saas, mobile-app, ecommerce)
--compliance: 準拠する規制 (gdpr, ccpa, coppa)
--jurisdiction: 管轄地域 (us, eu, jp, global)
```

### /tos-wizard
**対話型ウィザードで段階的に作成**

```bash
/tos-wizard --type saas --lang ja

# インタラクティブな質問形式で情報収集
# 各セクションを段階的に構築
```

### /tos-check
**既存規約のコンプライアンスチェック**

```bash
/tos-check --file ./terms.md --compliance gdpr,ccpa

# 出力:
- コンプライアンススコア
- 重大な問題の特定
- 改善提案
```

### /tos-update
**法改正に対応した自動更新**

```bash
/tos-update --file ./terms.md --regulations gdpr-2024

# 最新の規制変更を反映
# 変更箇所のハイライト
```

---

## 🎬 デモの実行方法

### Step 1: 基本的な利用規約生成
```bash
# SaaS向けの利用規約を生成
/terms-of-service create --type saas --compliance gdpr,ccpa
```

### Step 2: コンプライアンスチェック
```bash
# 生成された規約を検証
/tos-check --file ./terms-of-service.md --compliance gdpr
```

### Step 3: 競合分析による改善
```bash
# 業界標準と比較
"competitor-analyzerを使用して市場分析を実施"
```

### Step 4: リスク評価
```bash
# リスクスコアリング
"risk-assessorで責任制限条項を評価"
```

---

## 📊 期待される成果物

### 1. 利用規約文書 (terms-of-service.md)
- 14セクション構成
- GDPR/CCPA準拠
- プレースホルダー付きテンプレート

### 2. コンプライアンスレポート
- 規制準拠スコア
- リスクマトリックス
- 改善提案リスト

### 3. 実装チェックリスト
- 必要な技術実装
- 法的レビュー項目
- 運用プロセス

---

## 🚀 実装のポイント

### サブエージェントの定義
```yaml
---
name: agent-name
description: エージェントの説明
tools: Read, Grep, Edit, Write
model: inherit
---

# システムプロンプト
エージェントの詳細な指示...
```

### コマンドの実装
```markdown
# コマンド名
説明と使用方法

## 呼び出すエージェント
- agent-1
- agent-2

## 実行フロー
1. データ収集
2. 分析
3. 生成
```

---

## 🔧 カスタマイズ方法

### 新しいエージェントの追加
1. `.claude/agents/`に新規ファイル作成
2. YAMLフロントマター追加
3. システムプロンプト記述
4. ツール権限設定

### コマンドの拡張
1. `.claude/commands/`に新規ファイル作成
2. エージェント呼び出しロジック定義
3. パラメータ処理追加

---

## 📚 参考資料

### Claude Code ドキュメント
- [サブエージェント機能](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [スラッシュコマンド](https://docs.claude.com/en/docs/claude-code/commands)

### 法的リソース
- GDPR公式ガイダンス
- CCPA/CPRA要件
- FTC Click-to-Cancel規則

---

## 🎯 ワークショップ目標達成チェックリスト

- [ ] サブエージェントの動作理解
- [ ] スラッシュコマンドの実行
- [ ] 利用規約の生成
- [ ] コンプライアンスチェック実施
- [ ] リスク評価の理解
- [ ] カスタマイズ方法の習得

---

## 📧 サポート

質問や問題がある場合は、以下の方法でサポートを受けられます：

1. **Claude Codeヘルプ**: `/help`コマンド
2. **フィードバック**: [GitHub Issues](https://github.com/anthropics/claude-code/issues)
3. **ドキュメント**: [公式ドキュメント](https://docs.claude.com)

---

*このワークショップ教材は、Claude Codeの高度な機能を活用した実践的な学習を目的として作成されました。*

**バージョン**: 1.0
**最終更新**: 2025年1月20日
**作成者**: Claude Code Workshop Team