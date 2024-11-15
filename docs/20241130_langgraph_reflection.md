---
marp: true
theme: default

size: 16:9
paginate: true

style: |
 /* タイトル */
  section.title {
    --title-height: 130px;
    --subtitle-height: 70px;
    overflow: visible;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr var(--title-height) var(--subtitle-height) 1fr;
    grid-template-areas: "." "title" "subtitle" ".";
  }

  section.title h1,
  section.title h2 {
    margin: 0;
    padding: 0;
    text-align: center;
    height: var(--area-height);
    line-height: var(--area-height);
    font-size: calc(var(--area-height) * 0.35);
    border: 1px dashed gray; /* debug */
  }

  section.title h1 {
    grid-area: title;
    --area-height: var(--title-height);
  }

  section.title h2 {
    grid-area: subtitle;
    --area-height: var(--subtitle-height);
  }

  section {
    justify-content: start;
  }

  /* 2段組み */
  section.split {
    overflow: visible;
    display: grid;
    grid-template-columns: 500px 500px;
    grid-template-rows: 100px auto;
    grid-template-areas: 
      "slideheading slideheading"
     "leftpanel rightpanel";
  }
  /* debug */
  section.split h3, 
  section.split .ldiv, 
  section.split .rdiv { border: 1.5pt dashed dimgray; }
  section.split h3 {
    grid-area: slideheading;
    font-size: 50px;
  }
  section.split .ldiv { grid-area: leftpanel; }
  section.split .rdiv { grid-area: rightpanel; }

  /* 画像をcenterに持ってくる */
  img.center {
    display: block;
    margin: 0 auto;
  }

---
<!-- _class: title -->

# AIシステムの品質と成功率を向上させるReflection
## 機械学習の社会実装勉強会 第41回 (2024/11/30)

---
<style scoped>
ul {
  font-size: 22px; /* このスライドのリストのみフォントサイズを小さく */
}
</style>
# 自己紹介
- 名前: 西岡 賢一郎
  - X: @ken_nishi
  - LinkedIn: https://www.linkedin.com/in/kenichiro-nishioka/
  - Facebook: https://www.facebook.com/kenichiro.nishioka
  - note: https://note.com/kenichiro
  - YouTube: https://www.youtube.com/@kenichiro-nishioka
- 経歴
  - 東京大学で位置予測アルゴリズムを研究し博士 (学術) を取得
  - 東京大学の博士課程在学中にデータサイエンスをもとにしたサービスを提供する株式会社トライディアを設立
  - トライディアを別のIT会社に売却し、CTOとして3年半務め、2021年10月末にCTOを退職
  - 株式会社データインフォームド (CEO)・株式会社ディースタッツ (CTO)・CDPのスタートアップ (Sr. CSM)
  - 自社および他社のプロダクト開発チーム・データサイエンスチームの立ち上げ経験

---
# はじめに

- AI活用が進む中、課題となる「精度」と「信頼性」
- Reflection（振り返り）の導入がAIの進化に不可欠
- **本プレゼンのポイント**
  1. Reflectionの意義
  2. Reflectionのデモ
  3. 未来の展望

---
# 人間の行動タイプ

1. **行動者**  
   - とにかく行動するが、振り返りをしないタイプ
2. **反省者**  
   - 行動後に結果を振り返り、次に活かすタイプ
3. **戦略的行動者**  
   - 行動前に仮説を立て、結果を評価し次の行動に反映するタイプ

**比喩: 運転**
- 地図を見ずに運転 → 振り返りながら運転 → 計画的に最適ルートを選ぶ

---

# AIと人間の比較

| 人間の特徴                     | AIの課題                     |
|-------------------------------|-----------------------------|
| 自然に行動タイプを切り替え可能 | 過去の結果を活かせない       |
| 振り返りを通じて成長           | 同じエラーを繰り返す         |
| 戦略的思考ができる             | 一貫性に欠ける場合がある     |

- Reflectionを導入することで、AIも「反省者」や「戦略的行動者」に近づける。

---
# Reflection Agentの仕組み

1. **行動:** 質問に基づくタスクを実行
2. **振り返り:** 結果をレビューし、改善点を特定
3. **改善:** 改良した結果を提供
4. **学習:** 次のタスクに学びを反映

---
# デモ: Reflection Agentによるエッセイ改善

## ステップ1: 初期エッセイ生成
**プロンプト:**  
あなたは優れたエッセイを書くアシスタントです。  
- ユーザーのリクエストに応じて、5段落のエッセイを生成してください。  
- ユーザーがフィードバックを提供した場合、以前の試みを改訂してください。

**初期生成エッセイ:**  
- テーマ: 「環境保護の重要性」
- 生成結果: 内容は浅く、具体例が不足

---

## ステップ2: 振り返り（Reflectionプロセス）

**Reflectionプロンプト:**  
あなたはエッセイ提出物を採点する教師です。  
- 提出されたエッセイに対して詳細なフィードバックと改善提案を生成してください。  
- 長さ、深さ、スタイルなどを含めた具体的な提案を行ってください。

**フィードバック例:**  
- 「具体例が不足しており、説得力に欠ける」
- 「結論部分に論理的なつながりを追加すべき」
- 「2段落目の説明を深掘りする必要がある」

---

## ステップ3: 改善後のエッセイ

**改善されたエッセイ:**  
- テーマ: 「環境保護の重要性」  
- 改善点:  
  - 具体例として「プラスチック廃棄物問題」を追加  
  - データを引用し、説得力を向上  
  - 結論に論理的な流れを追加

**結果:**  
- Reflectionによって、内容の深さと説得力が大幅に向上

---

# Reflectionの効果: エッセイ改善の例

## ビフォー & アフター

| **Before**                     | **After**                     |
|--------------------------------|--------------------------------|
| 浅い内容で具体例が不足          | 深い分析と具体例の追加          |
| データや証拠の欠如             | 事実やデータに基づいた主張       |
| 結論が弱く説得力に欠ける        | 明確で論理的な結論              |

---

# Reflection Agentの活用例

## 1. 学習支援
- エッセイ作成時の内容改善

## 2. カスタマーサポート
- 顧客のフィードバックを振り返り、応答精度を向上

## 3. コンテンツ生成
- 初期提案を振り返り、修正版を迅速に作成

---

# 未来の展望 - 戦略的行動者としてのAI
1. **リスク評価と仮説検証**  
2. **計画的な意思決定**  
3. **自律的な行動の最適化**

AIが「戦略的行動者」として進化すれば、医療やビジネス戦略の分野での価値提供が可能に。

---

# 結論と次のステップ

- ReflectionはAIの精度を高め、未来の進化を支える鍵
- 現在の課題:
  1. Reflectionの標準化
  2. 実運用への適用
- **メッセージ:**  
  人間とAIが共に成長する未来を築くために、Reflectionを活用しよう！

---

# お問い合わせ
- お仕事の依頼・機械学習・LLMの実装のご相談は、X, LinkedIn, FacebookなどでDMをください
- 機械学習を社会実装する仲間も募集中!!
