import os
from typing import TypedDict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from supabase import create_client

load_dotenv()

from nodes.decision import execute_post_interview_decision


class DecisionState(TypedDict):
    candidate_id: str
    decision: str  # 'hire' or 'reject'
    result: Any


supabase = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)


def process_decision_node(state: DecisionState) -> dict:
    cand_id = state["candidate_id"]
    decision = state["decision"]

    success = execute_post_interview_decision(
        candidate_id=cand_id,
        decision=decision,
        supabase=supabase
    )
    return {"result": success}


builder = StateGraph(DecisionState)
builder.add_node("process_decision", process_decision_node)

builder.add_edge(START, "process_decision")
builder.add_edge("process_decision", END)

decision_graph = builder.compile()
