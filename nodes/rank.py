def rank_candidates_for_job(*args, **kwargs):
    """
    Ranks candidates for a specific job, enforces a 60/100 score threshold,
    and handles flexible graph/direct call signatures.
    """
    state = kwargs.get("state")
    job_id = kwargs.get("job_id")
    supabase = kwargs.get("supabase")

    if args:
        if isinstance(args[0], dict):
            state = args[0]
        else:
            job_id = args[0]
            if len(args) > 1:
                supabase = args[1]

    if isinstance(state, dict):
        job_id = state.get("job_id") or job_id
        supabase = state.get("supabase") or supabase

    if not job_id or not supabase:
        return []

    # Fetch all scored candidates for this specific job
    res = supabase.table("candidates").select("id, score, name, email").eq("job_id", job_id).execute()
    candidates = res.data or []

    # Sort candidates by score descending
    sorted_candidates = sorted(candidates, key=lambda x: x.get("score", 0) or 0, reverse=True)

    booked_ids = []
    declined_ids = []

    for rank, cand in enumerate(sorted_candidates, start=1):
        cand_id = cand["id"]
        score = cand.get("score", 0) or 0

        # Enforce Minimum Threshold of 60/100 AND Top 5 Rank
        if score >= 60 and rank <= 5:
            supabase.table("candidates").update({"status": "booked"}).eq("id", cand_id).execute()
            booked_ids.append(cand_id)
        else:
            supabase.table("candidates").update({"status": "declined"}).eq("id", cand_id).execute()
            declined_ids.append(cand_id)

    return sorted_candidates
