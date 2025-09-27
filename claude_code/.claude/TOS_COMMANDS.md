# TOS_COMMANDS.md - SaaS利用規約自動生成システム専用コマンド

## コマンド一覧

### /tos-wizard - 対話型利用規約作成ウィザード
**Purpose**: インタラクティブな質問形式でSaaS利用規約を段階的に生成
**Category**: Document Generation
**Complexity**: High
**Sub-Agent Strategy**: Multi-agent orchestration with specialized legal experts

### /tos-check - コンプライアンスチェック
**Purpose**: 既存の利用規約を法的要件と照合し、問題点を自動検出
**Category**: Compliance Analysis
**Complexity**: High
**Sub-Agent Strategy**: Parallel validation with legal compliance experts

### /tos-update - 法改正対応アップデート
**Purpose**: 最新の法規制に基づいて既存の利用規約を自動更新
**Category**: Document Maintenance
**Complexity**: High
**Sub-Agent Strategy**: Sequential update with change tracking

## コマンド詳細実装

### /tos-wizard

```yaml
command: "/tos-wizard"
description: "対話型SaaS利用規約作成ウィザード"
activation:
  manual: true
  flags:
    - --lang [ja|en] (言語選択)
    - --industry [saas|fintech|healthcare|ecommerce] (業界特化)
    - --compliance [gdpr|ccpa|appi|all] (準拠法選択)
workflow:
  phase1_discovery:
    agent: "business-analyzer"
    tasks:
      - サービス概要の収集
      - ビジネスモデルの分析
      - リスク要因の特定
  phase2_legal_framework:
    agent: "legal-compliance-reviewer"
    tasks:
      - 適用法規の特定
      - 必須条項の抽出
      - 業界固有要件の確認
  phase3_generation:
    agent: "legal-writer"
    tasks:
      - 条項の生成
      - カスタマイズ
      - 整合性チェック
  phase4_review:
    agent: "risk-assessor"
    tasks:
      - リスク評価
      - 免責条項の最適化
      - 最終レビュー
```

### /tos-check

```yaml
command: "/tos-check"
description: "利用規約コンプライアンスチェック"
activation:
  manual: true
  auto: on_document_change
  flags:
    - --strict (厳格モード)
    - --report [summary|detailed|matrix] (レポート形式)
    - --fix (自動修正提案)
workflow:
  parallel_analysis:
    agents:
      - legal-compliance-reviewer:
          focus: "法的要件チェック"
          checks:
            - GDPR準拠
            - 個人情報保護法
            - 消費者契約法
      - risk-assessor:
          focus: "リスク評価"
          checks:
            - 責任制限条項
            - 免責事項
            - 紛争解決条項
      - competitor-analyzer:
          focus: "業界標準比較"
          checks:
            - ベストプラクティス
            - 競合比較
            - 市場標準
  synthesis:
    coordinator: "general-purpose"
    outputs:
      - コンプライアンススコア
      - 問題点リスト
      - 改善提案
      - 優先順位マトリクス
```

### /tos-update

```yaml
command: "/tos-update"
description: "法改正対応自動アップデート"
activation:
  manual: true
  scheduled: monthly
  trigger: legal_update_detected
  flags:
    - --preview (プレビューモード)
    - --track-changes (変更履歴追跡)
    - --notify (ステークホルダー通知)
workflow:
  phase1_analysis:
    agent: "legal-compliance-reviewer"
    tasks:
      - 現行文書の解析
      - 法改正内容の特定
      - 影響範囲の評価
  phase2_update_planning:
    agent: "general-purpose"
    tasks:
      - 更新計画の策定
      - リスク評価
      - タイムライン設定
  phase3_implementation:
    agents:
      - legal-writer:
          task: "条項の更新"
      - risk-assessor:
          task: "新リスクの評価"
  phase4_validation:
    agent: "legal-compliance-reviewer"
    tasks:
      - 更新内容の検証
      - 整合性チェック
      - 最終承認準備
```

## Sub-Agent連携パターン

### 並列処理パターン
```
/tos-check実行時:
┌─────────────────┐
│  Coordinator    │
└────────┬────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    ▼         ▼         ▼          ▼
[Legal]  [Risk]  [Competitor]  [Security]
    │         │         │          │
    └────┬────┴─────────┴──────────┘
         ▼
   [統合レポート生成]
```

### シーケンシャルパターン
```
/tos-wizard実行時:
[収集] → [分析] → [生成] → [検証] → [最適化]
  ↓        ↓        ↓        ↓         ↓
Agent1   Agent2   Agent3   Agent4    Agent5
```

### ハイブリッドパターン
```
/tos-update実行時:
[分析フェーズ]
     ↓
[並列更新] ← 複数エージェント同時実行
     ↓
[統合・検証]
     ↓
[最終出力]
```

## エージェント特性

### business-analyzer
- サービス分析専門
- ビジネスモデル理解
- リスク特定能力

### legal-compliance-reviewer
- 法的要件の専門家
- コンプライアンス検証
- 規制動向の把握

### legal-writer
- 法的文書作成
- 平易な表現への変換
- 多言語対応

### risk-assessor
- リスク評価
- 責任範囲の最適化
- 保険条項の設計

### competitor-analyzer
- 業界ベストプラクティス
- 競合分析
- 市場標準の把握

## パフォーマンス指標

- **処理時間**:
  - /tos-wizard: 3-5分
  - /tos-check: 30-60秒
  - /tos-update: 2-3分

- **精度**:
  - コンプライアンス検出率: 95%+
  - 法改正カバー率: 98%+
  - 誤検出率: <2%

- **効率化**:
  - 手動作成比: 10倍高速
  - コスト削減: 80%
  - 品質向上: 3倍