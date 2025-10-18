# /tos-check - 利用規約検証

## コマンド概要
法的要件とコンプライアンスの検証

## 使用方法
```
/tos-check [--file <path>] [--compliance <standards>] [--depth <level>]
```

## オプション
- `--file`: 検証する利用規約ファイルのパス
- `--compliance`: 検証する規制 (gdpr, ccpa, pci-dss, hipaa)
- `--depth`: 検証の深さ (basic, standard, comprehensive)

## リスク評価 Agent

### 法的リスク特定 (`legal-risk-identifier`)
**機能:**
- 潜在的な法的リスクの特定
- 執行可能性の評価
- 管轄地域別のリスク分析
- 罰則・制裁金リスクの算定

**チェック項目:**
- 必須開示事項の欠落
- 違法または執行不能な条項
- 消費者保護法との矛盾
- 国際取引における問題点

### コンプライアンス検証 (`compliance-validator`)
**機能:**
- GDPR準拠性（データ主体の権利、法的根拠など）
- CCPA準拠性（消費者権利、オプトアウトなど）
- 業界固有規制の準拠性
- アクセシビリティ基準の確認

### リスクスコアリング (`risk-scorer`)
**機能:**
- リスクレベルの数値化（低・中・高）
- 優先順位付き改善提案
- コスト対効果分析
- 実装難易度の評価

## 検証プロセス
1. **構造分析**: 必要なセクションの有無
2. **内容検証**: 各条項の適法性と完全性
3. **整合性チェック**: 内部矛盾の検出
4. **比較分析**: 業界標準との比較
5. **リスク評価**: 総合的なリスクスコア

## 出力レポート
```yaml
summary:
  overall_score: 85/100
  compliance_level: "High"
  critical_issues: 3
  recommendations: 12

critical_issues:
  - missing_cookie_policy
  - inadequate_data_retention
  - no_age_verification

risk_matrix:
  legal: "Medium"
  financial: "Low"
  reputational: "Medium"
  operational: "Low"
```

## アラート機能
- 🔴 **重大**: 即座に対処が必要
- 🟡 **警告**: 30日以内に対処推奨
- 🟢 **情報**: 改善の余地あり