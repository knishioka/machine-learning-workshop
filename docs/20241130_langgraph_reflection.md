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
  font-size: 22px;
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
# 本日の課題認識

1. **通常のAIの課題**
   - 単一の応答に依存
   - 回答の修正に人間が介入

2. **解決の方向性**
   - 人間の学習プロセスからヒントを得る
   - 振り返り（Reflection）の重要性
   - システマティックな改善プロセス

---
# 人間の学習プロセスに学ぶ

1. **行動のみする人の特徴**  
   - とにかく行動するが、振り返りをしないタイプ
   - 結果：アウトプットは早いが品質が低い
   
2. **自己反省をして改善する人の特徴**  
   - 行動後に結果を振り返り、次に活かすタイプ
   - 結果：徐々に改善・成長を実現
   - **AIにもこの能力を実装することが重要**

---
# なぜAIにReflectionが必要か？

- AIの自己評価による品質向上
  - AIが自信の生成した回答を評価し，それを元に修正
  - **人間が介入せずに回答を修正することができる**
- 回答に応じて評価を柔軟に修正可能
  - 初期プロンプトにすべての条件を書く必要がない
  - 生成された回答に応じて評価・修正が可能

---
# Reflection Agentのアーキテクチャ

生成された回答をLLMに評価させ修正する

![width:900px center](images/202411_reflection_flow.png)


---
# エッセイ改善の例

**初期エッセイ（抜粋）**
```text
環境保護は私たちの未来にとって重要です。
地球温暖化は深刻な問題です。
私たちは行動を起こす必要があります。
```

**Reflectionプロセス**
1. 評価：具体性不足、データ欠如
2. 改善案：統計データ追加、具体例提示

**改善後**
```text
環境保護は、人類の持続可能な未来に不可欠です。
IPCCの2023年報告によると、過去10年で世界の平均気温は1.1℃上昇し、生態系に深刻な影響を及ぼしています。
例えば、北極圏の氷床面積は年間約13%の割合で減少し...
```

---
# デモ: ビジネスアイディア生成Agent
- Reflection Agentのやること
  - テーマに沿ってビジネスアイティアを生成
  - 投資家目線で批評・修正点の提示
  - 投資家からのフィードバックを元にビジネスアイディアを修正
- ソースコード
  https://github.com/knishioka/machine-learning-workshop/blob/main/langchain/reflection_agent.ipynb

---
<style scoped>
ul {
  font-size: 22px;
}
</style>
# Reflection Agentの実務活用例

### 1. カスタマーサポート
- **Before**: 一般的な応答
- **After**: 過去の類似ケース参照による最適解提示

### 2. 技術文書作成
- **Before**: 基本的な仕様書
- **After**: エッジケースを考慮した包括的文書

### 3. コードレビュー
- **Before**: 表面的なチェック
- **After**: セキュリティ面も含めた多角的レビュー
 
---
<style scoped>
ul {
  font-size: 22px;
}
</style>
# 今後の展望：Reflectionの進化

1. **現在のReflection（反省者型）**
   - 行動後の振り返りと改善
   - エラー検出と修正
   - 品質向上の実現

2. **将来の発展（戦略的行動者型）**
   - 事前の仮説設定と計画立案
   - 結果予測に基づく最適化
   - 自律的な意思決定と改善

---
# 結論：ReflectionがもたらすAIの進化

1. **品質向上**
  エラー率の低減や一貫性の向上や文脈理解の深化が期待できる

2. **効率化**
  人間が介入する必要がなくなり，作業時間の短縮ができる

3. **発展の可能性**
  戦略を練る高度な自己改善能力などを設けることにより，より人間に近いシステムとなる

---
# お問い合わせ
- お仕事の依頼・機械学習・LLMの実装のご相談は、X, LinkedIn, FacebookなどでDMをください
- 機械学習を社会実装する仲間も募集中!!