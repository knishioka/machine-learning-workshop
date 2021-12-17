# 機械学習の社会実装勉強会第6回(https://machine-learning-workshop.connpass.com/event/233814/)のスクリプト
from h2o_wave import main, site, ui

page = site["/hello"]

page["quote"] = ui.markdown_card(
    box="1 1 1 1",
    title="Hello World",
    content="ここに **本文**",
)


# for j in range(1, 5):
#     for i in range(1, 5):
#         print(j, i)
#         page[f"quote{i}_{j}"] = ui.markdown_card(
#             box=f"{j} {i} 1 1",
#             title="Hello World",
#             content=f"{j} {i} 1 1",
#         )

# for j in range(3):
#     for i in range(3):
#         print(j, i)
#         page[f"quote{i}_{j}"] = ui.markdown_card(
#             box=f"{j * 2 + 1} {i * 2 + 1} 2 2",
#             title="Hello World",
#             content=f"{j * 2 + 1} {i * 2 + 1} 2 2",
#         )


page.save()
