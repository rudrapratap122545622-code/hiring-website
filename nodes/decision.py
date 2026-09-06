import os
import requests


def generate_offer_html(candidate_name: str, job_title: str) -> str:
    """Generates a dark-mode HTML Offer Letter email."""
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background-color:#0f172a; font-family:'Segoe UI', Tahoma, sans-serif; color:#f8fafc;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#0f172a; padding:40px 10px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color:#1e293b; border-radius:12px; border:1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                    <tr>
                        <td align="center" style="background:linear-gradient(135deg, #10b981 0%, #0f172a 100%); padding:30px 20px; border-bottom:2px solid #10b981;">
                            <h1 style="margin:0; font-size:26px; color:#ffffff; letter-spacing:1px; text-transform:uppercase;">AGENTIC <span style="color:#34d399;">EMPLOYEES</span></h1>
                            <p style="margin:5px 0 0 0; font-size:13px; color:#94a3b8; letter-spacing:1px;">Official Offer of Employment</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:35px 30px;">
                            <h2 style="margin-top:0; color:#34d399; font-size:22px;">Congratulations, {candidate_name}!</h2>
                            <p style="font-size:15px; line-height:1.7; color:#cbd5e1;">
                                Following your recent interview performance with our engineering panel, we are thrilled to formally extend an offer for the position of <strong>{job_title}</strong> at <strong>Agentic Employees</strong>.
                            </p>
                            <p style="font-size:15px; line-height:1.7; color:#cbd5e1;">
                                Your technical depth, proficiency in backend systems, and experience with AI graph workflows stood out throughout our assessment.
                            </p>
                            <div style="background-color:#0f172a; border-left:4px solid #34d399; padding:20px; margin:25px 0; border-radius:6px;">
                                <h3 style="margin:0 0 8px 0; font-size:15px; color:#34d399;">Next Steps</h3>
                                <p style="margin:0; font-size:14px; color:#94a3b8; line-height:1.6;">
                                    Please reply directly to this email to confirm your acceptance. Our onboarding team will send over your compensation framework and formal agreement shortly.
                                </p>
                            </div>
                            <p style="font-size:15px; line-height:1.7; color:#cbd5e1;">We are excited about the prospect of having you join our core engineering unit!</p>
                            <hr style="border:none; border-top:1px solid #334155; margin:30px 0;" />
                            <p style="font-size:14px; color:#94a3b8; margin-bottom:0;">
                                Warm regards,<br>
                                <strong style="color:#f8fafc;">Engineering Hiring Committee</strong><br>
                                <span style="color:#34d399;">Agentic Employees Systems Inc.</span><br>
                                <a href="mailto:careers@agenticemployees.ai" style="color:#64748b; text-decoration:none; font-size:12px;">careers@agenticemployees.ai</a>
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="background-color:#0f172a; padding:20px; font-size:11px; color:#64748b; border-top:1px solid #334155;">
                            Confidential Employment Transmission &bull; &copy; 2026 Agentic Employees Inc.
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def generate_post_interview_rejection_html(candidate_name: str, job_title: str) -> str:
    """Generates a respectful post-interview rejection HTML email."""
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background-color:#0f172a; font-family:'Segoe UI', Tahoma, sans-serif; color:#f8fafc;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#0f172a; padding:40px 10px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color:#1e293b; border-radius:12px; border:1px solid #334155;">
                    <tr>
                        <td align="center" style="background-color:#1e293b; padding:30px 20px; border-bottom:1px solid #334155;">
                            <h1 style="margin:0; font-size:24px; color:#ffffff; text-transform:uppercase;">AGENTIC <span style="color:#38bdf8;">EMPLOYEES</span></h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:35px 30px;">
                            <h2 style="margin-top:0; color:#f8fafc; font-size:20px;">Update on Your Application: {job_title}</h2>
                            <p style="font-size:15px; line-height:1.7; color:#cbd5e1;">
                                Dear <strong>{candidate_name}</strong>,
                            </p>
                            <p style="font-size:15px; line-height:1.7; color:#cbd5e1;">
                                Thank you for taking the time to interview with our engineering team for the <strong>{job_title}</strong> position.
                            </p>
                            <p style="font-size:15px; line-height:1.7; color:#cbd5e1;">
                                While our interviewers were impressed by your background, we have decided to move forward with another candidate whose technical experience aligns more closely with our immediate platform needs.
                            </p>
                            <p style="font-size:15px; line-height:1.7; color:#cbd5e1;">
                                We sincerely appreciate your time and effort throughout our recruitment process and wish you all the best in your professional journey.
                            </p>
                            <hr style="border:none; border-top:1px solid #334155; margin:30px 0;" />
                            <p style="font-size:14px; color:#94a3b8; margin-bottom:0;">
                                Best regards,<br>
                                <strong style="color:#f8fafc;">Talent Acquisition Team</strong><br>
                                <span style="color:#38bdf8;">Agentic Employees Inc.</span>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def execute_post_interview_decision(candidate_id: str, decision: str, supabase) -> bool:
    """Updates candidate status in Supabase and dispatches decision HTML payload to Make.com."""
    res = supabase.table("candidates").select("name, email, job_id").eq("id", candidate_id).execute()
    if not res.data:
        print(f"Error: Candidate ID '{candidate_id}' not found in Supabase.")
        return False

    candidate = res.data[0]
    cand_name = candidate.get("name", "Applicant")
    cand_email = candidate.get("email")

    # Fetch Job Title
    job_res = supabase.table("jobs").select("title").eq("id", candidate["job_id"]).execute()
    job_title = job_res.data[0]["title"] if job_res.data else "Senior AI / Backend Engineer"

    is_hire = decision.strip().lower() == "hire"
    final_status = "hired" if is_hire else "rejected"

    # Update status in database
    supabase.table("candidates").update({"status": final_status}).eq("id", candidate_id).execute()

    # Fire Webhook to Make.com
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")
    if not webhook_url or not cand_email:
        print("Missing MAKE_WEBHOOK_URL or candidate email. Email notification skipped.")
        return False

    if is_hire:
        subject = f"Official Job Offer: {job_title} | Agentic Employees"
        html_body = generate_offer_html(cand_name, job_title)
    else:
        subject = f"Interview Status Update: {job_title} | Agentic Employees"
        html_body = generate_post_interview_rejection_html(cand_name, job_title)

    payload = {
        "event": "hiring_decision",
        "action": f"send_{final_status}_email",
        "candidate_id": candidate_id,
        "candidate_name": cand_name,
        "candidate_email": cand_email,
        "job_title": job_title,
        "subject": subject,
        "content": html_body,
        "html_content": html_body
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        print(f"Decision Webhook Fired ({final_status.upper()}): HTTP {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"[Error] Failed to send decision webhook: {e}")
        return False
