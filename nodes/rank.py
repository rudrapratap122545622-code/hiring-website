from supabase import Client


def rank_candidates_for_job(job_id: str, supabase: Client) -> list[dict]:
    """
    Queries all evaluated candidates for a job, sorts them by score descending,
    updates their rank in Supabase, and returns the ranked list.
    """
    # Fetch all candidates with valid scores for this job
    response = (
        supabase.table("candidates")
        .select("id, name, email, score, rationale, status")
        .eq("job_id", job_id)
        .not_.is_("score", "null")
        .order("score", desc=True)
        .execute()
    )

    candidates = response.data or []
    if not candidates:
        return []

    ranked_results = []
    for rank_idx, candidate in enumerate(candidates, start=1):
        cand_id = candidate["id"]

        # Persist rank index in Supabase
        supabase.table("candidates").update({"rank": rank_idx}).eq("id", cand_id).execute()

        candidate["rank"] = rank_idx
        ranked_results.append(candidate)

    return ranked_results
