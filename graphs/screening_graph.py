import os
from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from supabase import create_client

load_dotenv()

from nodes.parse import extract_text_from_file
from nodes.score import score_and_extract_candidate
from nodes.rank import rank_candidates_for_job
from nodes.book_interview import book_interview_slot
from nodes.send_email import send_decline_email


class ScreeningState(TypedDict):
    job_id: str
    job_title: str
    job_description: str
    candidate_name: str
    candidate_email: str
    resume_paths: List[str]
    candidate_ids: List[str]
    ranked_candidates: List[Dict[str, Any]]


supabase = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)


def parse_and_score_node(state: ScreeningState) -> dict:
    """Parses resume file, inserts candidate with provided contact info, and scores via LLM."""
    job_id = state["job_id"]
    job_desc = state["job_description"]
    provided_name = state.get("candidate_name")
    provided_email = state.get("candidate_email")
    created_candidate_ids = []

    for file_path in state["resume_paths"]:
        raw_text = extract_text_from_file(file_path)

        # Insert initial record into Supabase with provided Name and Email
        db_res = supabase.table("candidates").insert({
            "job_id": job_id,
            "name": provided_name if provided_name else "Applicant",
            "email": provided_email,
            "resume_text": raw_text,
            "status": "parsed"
        }).execute()

        cand_id = db_res.data[0]["id"]

        # Score resume with Groq LLM
        score_and_extract_candidate(
            candidate_id=cand_id,
            job_description=job_desc,
            resume_text=raw_text,
            provided_name=provided_name,
            provided_email=provided_email,
            supabase=supabase
        )
        created_candidate_ids.append(cand_id)

    return {"candidate_ids": created_candidate_ids}


def rank_node(state: ScreeningState) -> dict:
    """Queries scored candidates for the job and computes their rank."""
    job_id = state["job_id"]
    ranked_list = rank_candidates_for_job(job_id=job_id, supabase=supabase)
    return {"ranked_candidates": ranked_list}


def book_top_candidates_node(state: ScreeningState) -> dict:
    """Books interviews for top ranked candidates (rank <= 5)."""
    ranked = state.get("ranked_candidates", [])
    top_candidates = [c for c in ranked if c.get("rank", 999) <= 5]
    job_title = state.get("job_title", "Position")

    for candidate in top_candidates:
        cand_id = candidate["id"]
        cand_name = candidate.get("name", "Applicant")
        cand_email = candidate.get("email")
        if cand_email:
            book_interview_slot(
                candidate_id=cand_id,
                candidate_name=cand_name,
                candidate_email=cand_email,
                job_title=job_title,
                supabase=supabase
            )

    return {}


def decline_remaining_candidates_node(state: ScreeningState) -> dict:
    """Sends personalized decline emails via Make.com to lower-ranked candidates."""
    ranked = state.get("ranked_candidates", [])
    lower_candidates = [c for c in ranked if c.get("rank", 0) > 5]
    job_title = state.get("job_title", "Position")

    for candidate in lower_candidates:
        cand_id = candidate["id"]
        cand_name = candidate.get("name", "Applicant")
        cand_email = candidate.get("email")
        rationale = candidate.get("rationale", "Qualifications did not align closely with role requirements.")

        if cand_email:
            send_decline_email(
                candidate_name=cand_name,
                candidate_email=cand_email,
                job_title=job_title,
                rationale=rationale
            )

        supabase.table("candidates").update({"status": "declined"}).eq("id", cand_id).execute()

    return {}


builder = StateGraph(ScreeningState)

builder.add_node("parse_and_score", parse_and_score_node)
builder.add_node("rank", rank_node)
builder.add_node("book_top_candidates", book_top_candidates_node)
builder.add_node("decline_remaining", decline_remaining_candidates_node)

builder.add_edge(START, "parse_and_score")
builder.add_edge("parse_and_score", "rank")
builder.add_edge("rank", "book_top_candidates")
builder.add_edge("book_top_candidates", "decline_remaining")
builder.add_edge("decline_remaining", END)

# Compiled graph variable expected by graphs/__init__.py
screening_graph = builder.compile()
