import os
from dotenv import load_dotenv

load_dotenv()

from supabase import create_client
from graphs.decision_graph import decision_graph


def main():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in your .env file.")
        return

    supabase = create_client(supabase_url, supabase_key)

    print("\n=== Stage 2: Post-Interview Decision Execution ===")

    # Fetch recent candidate records
    res = (
        supabase.table("candidates")
        .select("id, name, email, status")
        .order("created_at", desc=True)
        .limit(5)
        .execute()
    )

    candidates = res.data or []
    if not candidates:
        print("No candidates found in Supabase database.")
        return

    print("\nRecent Candidates:")
    for idx, c in enumerate(candidates, start=1):
        print(
            f"{idx}. Name: {c.get('name')} | Email: {c.get('email')} | Status: {c.get('status')} | ID: {c.get('id')}"
        )

    candidate_id = input("\nEnter Candidate ID to process decision for: ").strip()
    decision = input("Enter Decision (hire / reject): ").strip().lower()

    if decision not in ["hire", "reject"]:
        print("Invalid decision option. Please enter either 'hire' or 'reject'.")
        return

    print(f"\nProcessing '{decision.upper()}' decision...")
    decision_graph.invoke({
        "candidate_id": candidate_id,
        "decision": decision,
        "result": None
    })
    print(f"\nStage 2 execution completed! Updated status to '{decision}'.")


if __name__ == "__main__":
    main()
