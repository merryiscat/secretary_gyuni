# 필요 라이브러리 임포트
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from State import *
from Node import *

def simple_route(state: OverallState) -> str:
    return state["intent"]

def Project_Graph():
    builder = StateGraph(OverallState)

    builder.add_node("user_input_node", user_input_node)
    builder.add_node("intent_classify", intent_classify_node)
    builder.add_node("test_node", test_node)
    builder.add_node("intent_extract", intent_extract_node)
    builder.add_node("keywords_rank", keywords_rank_node)
    builder.add_node("query_make", query_make_node)
    builder.add_node("identity_node", identity_node)
    builder.add_node("talk_node", talk_node)
    builder.add_node("food_recommand_node", food_recommand_node)
    builder.add_node("run_mcp", run_mcp_node)
    builder.add_node("result_make", result_make_node)
    builder.add_node("exit_node", exit_node)

    builder.set_entry_point("user_input_node")
    builder.add_edge("user_input_node", "intent_classify")
    builder.add_conditional_edges(
    "intent_classify",
    simple_route,
    {"음식추천요청": "food_recommand_node", "식당검색요청": "intent_extract", "일상대화": "talk_node", "정체성 문의": "identity_node", "분류실패":"exit_node"}
    )
    builder.add_edge("intent_extract", "keywords_rank")
    builder.add_edge("keywords_rank", "query_make")
    builder.add_edge("query_make", "run_mcp")
    builder.add_edge("run_mcp", "result_make")    
    builder.set_finish_point("result_make")
    builder.set_finish_point("identity_node")
    builder.set_finish_point("exit_node")
    builder.set_finish_point("talk_node")

    memory = MemorySaver()
    app = builder.compile(checkpointer=None)

    return app 