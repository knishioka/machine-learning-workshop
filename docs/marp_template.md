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
    font-size: calc(var(--area-height) * 0.7);
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
# タイトル
## SubTitle

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
  - CDPのスタートアップ (Sr. PdM)・株式会社データインフォームド (CEO)・株式会社ディースタッツ (CTO)
  - 自社および他社のプロダクト開発チーム・データサイエンスチームの立ち上げ経験

---
# 本日の発表

---

# お問い合わせ
- お仕事の依頼・機械学習・LLMの実装のご相談は、X, LinkedIn, FacebookなどでDMをください
- 機械学習を社会実装する仲間も募集中!!
