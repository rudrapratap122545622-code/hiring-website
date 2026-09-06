import json
import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


def extract_email_with_regex(text: str) -> str | None:
    """Fallback regex extractor for standard email addresses in raw text."""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def score_and_extract_candidate(
    candidate_id: str,
    job_description: str,
    resume_text: str,
    provided_name: str | None,
    provided_email: str | None,
    supabase
) -> dict:
    """
    Scores qualifications against job requirements, respects provided contact info, 
    and updates Supabase.
    """
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an automated hiring extraction and scoring assistant.
Analyze the provided candidate resume and job description.

Evaluate qualifications and extract contact details if not already provided:
1. Candidate Full Name
2. Candidate Email / Gmail address
3. Qualification Score (0 to 100 based on job requirements match)
4. Structured Evaluation Rationale (2-3 concise sentences)

STRICT OUTPUT FORMAT: Return ONLY a raw JSON object with no markdown formatting:
{{
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "score": 88,
    "rationale": "Candidate has strong hands-on experience in Python, FastAPI, and Supabase..."
}}"""),
        ("user", "JOB DESCRIPTION:\n{job_description}\n\nRESUME TEXT:\n{resume_text}")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "job_description": job_description,
        "resume_text": resume_text
    })

    # Clean JSON output from LLM
    content = response.content.strip()
    if content.startswith("```json"):
        content = content.replace("```json", "", 1).replace("```", "", 1).strip()
    elif content.startswith("```"):
        content = content.replace("```", "", 1).strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {
            "name": "Applicant",
            "email": None,
            "score": 50,
            "rationale": "Could not parse detailed scoring response."
        }

    # Resolve Name & Email (User Input > LLM Extraction > Regex Fallback)
    cand_name = provided_name if provided_name else data.get("name", "Applicant")
    cand_email = provided_email if provided_email else data.get("email")

    if not cand_email or "@" not in str(cand_email):
        cand_email = extract_email_with_regex(resume_text)

    score = int(data.get("score", 0))
    rationale = data.get("rationale", "")

    # Update candidate record in Supabase with resolved details
    supabase.table("candidates").update({
        "name": cand_name,
        "email": cand_email,
        "score": score,
        "rationale": rationale,
        "status": "scored"
    }).eq("id", candidate_id).execute()

    print(f"Candidate Processed: {cand_name} | Email: {cand_email} | Score: {score}/100")
    return {
        "name": cand_name,
        "email": cand_email,
        "score": score,
        "rationale": rationale
    }


# Backward-compatible alias
score_candidate = score_and_extract_candidate
