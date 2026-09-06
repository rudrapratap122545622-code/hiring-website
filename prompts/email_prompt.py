DECLINE_EMAIL_PROMPT = """You are an HR representative. Write a professional, empathetic rejection email to a job applicant.
Use the provided rationale to explain the decision respectfully without disclosing raw numerical scores.

Candidate Name: {candidate_name}
Rationale: {rationale}
Job Title: {job_title}
"""

OFFER_EMAIL_PROMPT = """You are an HR representative. Write an enthusiastic job offer email to a successful candidate.

Candidate Name: {candidate_name}
Job Title: {job_title}
Next Steps: Reply to this email to confirm acceptance and discuss start dates.
"""
