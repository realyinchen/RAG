from langchain_community.utilities import SQLDatabase
from langchain import hub
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph import START, StateGraph
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_openai import ChatOpenAI
from db_connection import get_database_config
from dotenv import load_dotenv


load_dotenv()
llm = ChatOpenAI(model="qwen-max")
prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")


# Connect to the SQLite database
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    db: SQLDatabase


class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State) -> str:
    db_config = get_database_config()

    prompt = prompt_template.invoke(
        {
            "dialect": db_config["db"].dialect,
            "top_k": 5,
            "table_info": db_config["table_info"],
            "input": state["question"],
        }
    )

    result = llm.with_structured_output(QueryOutput).invoke(prompt)

    return {"query": result["query"], "db": db_config["db"]}


def execute_query(state: State):
    execute_query_tool = QuerySQLDatabaseTool(db=state["db"])
    return {"result": execute_query_tool.invoke(state["query"])}


def generate_answer(state: State):
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f"Question: {state['question']}\n"
        f"SQL Query: {state['query']}\n"
        f"SQL Result: {state['result']}"
    )
    response = llm.invoke(prompt)

    return {"answer": response.content}


def answer_question(question: str) -> str:
    """
    Given a question, return the answer.
    """
    graph_builder = StateGraph(State).add_sequence(
        [write_query, execute_query, generate_answer]
    )
    graph_builder.add_edge(START, "write_query")
    graph = graph_builder.compile()

    return graph.stream({"question": question})
