import os
from dotenv import load_dotenv

# MUST load environment variables FIRST before importing graph modules
load_dotenv()

from supabase import create_client
from graphs import screening_graph, decision_graph


def main():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be configured in your .env file.")
        return

    supabase = create_client(supabase_url, supabase_key)

    # 1. Fetch or create a test job in Supabase
    job_res = supabase.table("jobs").select("id, title, description").limit(1).execute()

    if not job_res.data:
        print("Creating default job posting in Supabase...")
        job_res = supabase.table("jobs").insert({
            "title": "Senior AI / Backend Engineer",
            "description": "Looking for an engineer proficient in Python, LangGraph, LLM integration, and Postgres databases."
        }).execute()

    active_job = job_res.data[0]
    job_id = active_job["id"]
    job_title = active_job.get("title", "Senior AI / Backend Engineer")
    job_description = active_job.get("description", "")

    print(f"\n--- Target Job Loaded: {job_title} ---")

    # 2. Collect Candidate Details Interactively from Terminal
    print("\n--- Enter Candidate Details ---")
    candidate_name = input("Candidate Name: ").strip()
    candidate_email = input("Candidate Gmail/Email: ").strip()
    resume_path_or_url = input("Google Drive Resume Link or Local File Path: ").strip()

    if not resume_path_or_url:
        print("Error: Resume link or file path is required.")
        return

    # 3. Assemble Payload for Screening Graph
    screening_input = {
        "job_id": job_id,
        "job_title": job_title,
        "job_description": job_description,
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "resume_paths": [resume_path_or_url],
        "candidate_ids": [],
        "ranked_candidates": []
    }

    print("\n=== Executing Screening Graph ===")
    screening_result = screening_graph.invoke(screening_input)
    print("Screening Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()
