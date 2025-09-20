# 🚀 クイックスタートガイド

## 5分で始める利用規約自動生成

### 1️⃣ 基本コマンド（1分）
```bash
# SaaS向け利用規約を即座に生成
/terms-of-service create --type saas --compliance gdpr,ccpa
```

### 2️⃣ コンプライアンスチェック（1分）
```bash
# 生成された規約を検証
/tos-check --file ./terms-of-service.md --compliance gdpr
```

### 3️⃣ エージェント活用（2分）
```bash
# リスク評価
"risk-assessorで責任制限条項を評価"

# 競合分析
"competitor-analyzerで業界標準と比較"

# 法的レビュー
"legal-compliance-reviewerでGDPR準拠を確認"
```

### 4️⃣ 改善と最適化（1分）
```bash
# 自動更新で最新規制対応
/tos-update --file ./terms-of-service.md --regulations gdpr-2024
```

---

## 📝 重要なコマンド一覧

| コマンド | 用途 | 実行時間 |
|---------|------|----------|
| `/terms-of-service create` | 新規作成 | 30秒 |
| `/tos-wizard` | 対話型作成 | 3-5分 |
| `/tos-check` | 検証 | 20秒 |
| `/tos-update` | 更新 | 15秒 |

---

## 🎯 エージェントの役割

### legal-compliance-reviewer
- **スコア算出**: GDPR/CCPA準拠度
- **問題特定**: 重大な法的リスク
- **改善提案**: 具体的な修正案

### risk-assessor
- **リスク評価**: 0-100のスコアリング
- **財務影響**: 潜在的損失額の算定
- **優先順位**: 対応の緊急度判定

### competitor-analyzer
- **市場調査**: 業界リーダーの分析
- **差別化**: 競合優位性の提案
- **トレンド**: 最新動向の把握

---

## ⚡ トラブルシューティング

**Q: コマンドが動作しない**
```bash
# ヘルプを表示
/help

# エージェント一覧確認
ls .claude/agents/
```

**Q: エラーが発生する**
```bash
# Claude Codeを再起動
# プロジェクトディレクトリを再確認
pwd
```

**Q: カスタマイズしたい**
```bash
# エージェント定義を編集
vi .claude/agents/legal-compliance-reviewer.md
```

---

## 📚 詳細ドキュメント

- **README.md** - 完全なシステム説明
- **DEMO_FLOW.md** - デモ実演手順
- **agent-architecture.md** - 技術仕様

---

*5分で利用規約作成を自動化 - Claude Code Workshop*