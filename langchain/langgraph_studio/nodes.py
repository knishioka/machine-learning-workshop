import functools
from typing import Annotated

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import (
    AIMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode


def create_agent(llm, tools, system_message: str):
    """Create an agent."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたは他の専門的なアシスタントとチームを組んで働く有能なAIアシスタントです。"
                "あなたの役割は、利用可能なツールを使って与えられたタスクを解決することに貢献することです。"
                "もしタスクを完全に完了できない場合でも、それで問題ありません。"
                "あなたの仕事は、できるだけ進めたうえで次のアシスタントにタスクを引き継ぐことです。"
                "タスクを引き継ぐ際には、達成した内容と次のアシスタントが必要とする可能性のあるコンテキストを提供してください。"
                "ツールはその目的に沿ってのみ使用し、不要に使用しないようにしてください。"
                "最終的な答えや成果物に達した場合は、チームにタスクが完了したことがわかるように、回答の冒頭に『FINAL ANSWER』と明記してください。"
                "成功のためには協力と明確なコミュニケーションが重要です。"
                "あなたは次のツールにアクセスできます: {tool_names}。\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_tools(tools)


tavily_tool = TavilySearchResults(
    max_results=5
)  # インターネットからデータを取得するためのツール


@tool
def python_repl(
    code: Annotated[str, "グラフを描画するためのPythonコード"],
):
    """
    データを視覚化するためにPythonコードを実行するにはこれを使用します。
    値の出力を確認したい場合は、`print(...)`を使用して出力してください。
    """
    repl = PythonREPL()  # Pythonコードを実行するクラス
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (
        result_str
        + "\n\nすべてのタスクが完了した場合は、FINAL ANSWERと応答してください。"
    )


def agent_node(state, agent, name):
    """
    エージェントノードで実行されるタスク。
    Args:
        state (StateType): エージェントに渡される状態オブジェクト。
        agent (AgentType): invokeメソッドを持つエージェントオブジェクト。
        name (str): メッセージの送信者の名前。
    Returns:
        dict: 処理されたメッセージと送信者情報を含む辞書。
            - messages (list): 処理されたメッセージのリスト。
            - sender (str): メッセージの送信者の名前。
    """

    result = agent.invoke(state)
    # 状態を更新できるようにフォーマットを変更
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],  # メッセージが追加される
        "sender": name,  # senderが更新される
    }


llm = ChatOpenAI(model="gpt-4o")

# Research agent and node
research_agent = create_agent(
    llm,
    [tavily_tool],
    system_message=(
        "You should provide accurate data for the chart_generator to use."
        "When you already have data, you can finish the flow."
    ),
)
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

# chart_generator
chart_agent = create_agent(
    llm,
    [python_repl],
    system_message="描画したチャートはユーザに表示されます。",
)
chart_node = functools.partial(agent_node, agent=chart_agent, name="chart_generator")


tool_node = ToolNode([tavily_tool, python_repl])
