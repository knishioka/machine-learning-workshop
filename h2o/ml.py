# 機械学習の社会実装勉強会第6回(https://machine-learning-workshop.connpass.com/event/233814/)のスクリプト
from h2o_wave import main, app, Q, ui
import pandas as pd


@app("/ml")
async def serve(q: Q):
    print(q.args)
    header(q)
    file_uploader(q)
    table_view(q)
    pie_chart(q)
    if "start_ml" in q.args:
        ml_result(q)
    await q.page.save()


def header(q):
    q.page["title"] = ui.header_card(
        box="1 1 11 1",
        title="AIアプリケーション",
        subtitle="AIアプリを作る",
        icon_color="#ffe600",
    )


def file_uploader(q):
    if "file_upload" in q.args:
        q.page["example"] = ui.form_card(
            box="1 2 4 5",
            items=[
                ui.text(f"file_upload={q.args.file_upload}"),
                ui.button(name="show_upload", label="Back", primary=True),
            ],
        )
    else:
        q.page["example"] = ui.form_card(
            box="1 2 4 5",
            items=[
                ui.file_upload(
                    name="file_upload",
                    label="Upload",
                    multiple=True,
                    file_extensions=["csv", "gz"],
                )
            ],
        )


def load_data():
    return pd.read_csv("../titanic.csv")


def table_view(q):
    df = load_data()
    q.page["table_view"] = ui.form_card(
        box="5 2 5 5",
        items=[
            ui.text_xl("Table View"),
            ui.button(name="start_ml", label="Start ML"),
            ui.table(
                name="Uploaded Data",
                columns=[ui.table_column(name=col, label=col) for col in df.columns],
                rows=[
                    ui.table_row(
                        name=str(idx), cells=row.astype(str).tolist()  # 必ずstrにする必要がある
                    )
                    for idx, row in df.iterrows()
                ],
            ),
            ui.dropdown("カラム一覧", values=df.columns.tolist()),
        ],
    )


def pie_chart(q):
    df = load_data()
    survived = df.survived.value_counts()
    survived_rate = float((survived[0] / survived.sum()).round(2))
    q.page["pie_chart"] = ui.wide_pie_stat_card(
        box="1 7 2 2",
        title="Survived",
        pies=[
            ui.pie(
                label="True",
                value=str(survived_rate),
                fraction=survived_rate,
                color="#ff0000",
            ),
            ui.pie(
                label="False",
                value=str((1 - survived_rate)),
                fraction=(1 - survived_rate),
                color="#00ff00",
            ),
        ],
    )


def ml_result(q):
    # ここで機械学習の処理を行っていく
    q.page["ml_result"] = ui.markdown_card(box="3 7 2 2", title="ML", content="学習完了！")
