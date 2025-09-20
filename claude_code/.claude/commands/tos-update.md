# /tos-update - 利用規約アップデート

## コマンド概要
法改正に合わせた規約の自動アップデート

## 使用方法
```
/tos-update [--file <path>] [--regulations <list>] [--auto-apply]
```

## オプション
- `--file`: 更新する利用規約ファイル
- `--regulations`: 対応する法規制の更新
- `--auto-apply`: 自動適用（確認プロンプトなし）

## 競合分析 Agent

### 業界標準調査 (`industry-standards-researcher`)
**機能:**
- 業界のベストプラクティス収集
- 最新の法規制動向の把握
- 競合他社の規約更新追跡
- 市場トレンドの分析

**データソース:**
- 主要SaaS企業の規約変更履歴
- 規制当局のガイドライン
- 業界団体の推奨事項
- 法律事務所のアドバイザリー

### ベンチマーク分析 (`benchmark-analyzer`)
**機能:**
- 競合10社との条項比較
- ユーザーフレンドリー度の評価
- 保護レベルのバランス分析
- 独自性と差別化ポイント

**評価指標:**
```yaml
metrics:
  readability_score: "8th grade"
  user_protection: 85%
  company_protection: 90%
  transparency: 95%
  accessibility: "WCAG 2.1 AA"
```

### 改善提案生成 (`improvement-generator`)
**機能:**
- 具体的な文言の提案
- 新条項の追加推奨
- 削除・統合すべき条項
- 表現の簡素化案

## 更新プロセス

### 1. 変更検出
```yaml
regulatory_changes:
  - gdpr_updates: "Schrems III対応"
  - ccpa_amendments: "CPRA施行対応"
  - ai_act: "EU AI規制対応"
```

### 2. 影響分析
```yaml
impact_assessment:
  affected_sections:
    - data_protection
    - international_transfers
    - automated_decisions
  urgency: "High"
  deadline: "2024-03-01"
```

### 3. 更新案作成
- 変更箇所のハイライト
- 新旧対照表の生成
- 理由説明の付記
- 代替案の提示

### 4. レビュー＆承認
- 法務専門家レビュー用サマリー
- ステークホルダー向け説明資料
- ユーザー通知文案
- 移行スケジュール

## 自動化機能

### 定期監視
```yaml
monitoring:
  frequency: "weekly"
  sources:
    - regulatory_databases
    - competitor_sites
    - legal_news_feeds
  alerts:
    - email_notification
    - slack_integration
    - dashboard_update
```

### バージョン管理
```yaml
versioning:
  current: "2.3.1"
  changes:
    - date: "2024-01-15"
      type: "regulatory"
      description: "GDPR enforcement update"
    - date: "2024-02-01"
      type: "feature"
      description: "AI features disclosure"
```

## 統合機能

### Git連携
- 変更履歴の自動コミット
- プルリクエストの作成
- レビュープロセスの管理
- タグ付けとリリース

### 通知システム
- ユーザーへの変更通知
- 事前告知スケジュール
- 同意再取得フロー
- FAQ更新提案

## 出力形式

### 更新レポート
```markdown
# Terms of Service Update Report

## Executive Summary
- 3 critical updates required
- 5 recommended improvements
- Compliance deadline: March 1, 2024

## Critical Updates
1. **CPRA Compliance**
   - Add "Correct" and "Limit Use" rights
   - Update opt-out mechanisms

2. **AI Transparency**
   - Disclose automated decision-making
   - Provide explanation rights

## Implementation Timeline
- Week 1: Legal review
- Week 2: Technical implementation
- Week 3: User notification
- Week 4: Go-live
```

### コンプライアンスダッシュボード
- リアルタイム準拠状況
- 更新履歴グラフ
- 次回更新予定
- リスクヒートマップ