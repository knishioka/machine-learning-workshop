from agent import graph
from langchain_core.messages import (
    HumanMessage,
)

events = graph.stream(
    {
        "messages": [
            HumanMessage(
                content="直近10年のS&P500の株価の１年ごとのデータを取得して描画",
            )
        ],
    },
    # Maximum number of steps to take in the graph
    {"recursion_limit": 10},
    stream_mode="values",
)
for s in events:
    s["messages"][-1].pretty_print()
