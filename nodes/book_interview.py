import os
import requests


def generate_booking_html(candidate_name: str, job_title: str) -> str:
    """Generates a professional >300 word HTML email template for interview scheduling."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interview Invitation - Agentic Employees</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #f8fafc;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0f172a; padding: 40px 10px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color: #1e293b; border-radius: 12px; overflow: hidden; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                    
                    <!-- BRAND HEADER -->
                    <tr>
                        <td align="center" style="background: linear-gradient(135deg, #0284c7 0%, #0f172a 100%); padding: 30px 20px; border-bottom: 2px solid #0284c7;">
                            <h1 style="margin: 0; font-size: 26px; font-weight: 800; letter-spacing: 1.5px; color: #ffffff; text-transform: uppercase;">
                                AGENTIC <span style="color: #38bdf8;">EMPLOYEES</span>
                            </h1>
                            <p style="margin: 5px 0 0 0; font-size: 13px; color: #94a3b8; letter-spacing: 1px;">AI-Driven Autonomous Workforce Platform</p>
                        </td>
                    </tr>

                    <!-- MAIN CONTENT -->
                    <tr>
                        <td style="padding: 35px 30px;">
                            <h2 style="margin-top: 0; color: #f8fafc; font-size: 22px;">Interview Invitation: {job_title}</h2>
                            
                            <p style="font-size: 15px; line-height: 1.7; color: #cbd5e1;">
                                Dear <strong>{candidate_name}</strong>,
                            </p>

                            <p style="font-size: 15px; line-height: 1.7; color: #cbd5e1;">
                                Thank you for applying to join the engineering core at <strong>Agentic Employees</strong>. Our automated recruitment system evaluated your technical profile, background, and practical experience against our core requirements for the <strong>{job_title}</strong> role.
                            </p>

                            <p style="font-size: 15px; line-height: 1.7; color: #cbd5e1;">
                                Based on your high match score across candidate technical criteria—specifically in backend system design, LLM integration, and agentic framework orchestration—our team is excited to invite you to the formal interview stage.
                            </p>

                            <!-- HIGHLIGHT BOX -->
                            <div style="background-color: #0f172a; border-left: 4px solid #38bdf8; border-radius: 6px; padding: 20px; margin: 25px 0;">
                                <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #38bdf8;">Interview Agenda & Structure</h3>
                                <ul style="margin: 0; padding-left: 20px; color: #94a3b8; font-size: 14px; line-height: 1.8;">
                                    <li><strong style="color: #e2e8f0;">Phase 1 (20 Mins):</strong> Technical Architecture & LangGraph Design Strategy</li>
                                    <li><strong style="color: #e2e8f0;">Phase 2 (20 Mins):</strong> Live Problem Solving: Supabase, Python Async & Webhook Integration</li>
                                    <li><strong style="color: #e2e8f0;">Phase 3 (10 Mins):</strong> Candidate Q&A & Cultural Fit Assessment</li>
                                </ul>
                            </div>

                            <!-- PREPARATION ADVICE -->
                            <h3 style="color: #f8fafc; font-size: 16px; margin-top: 25px;">How to Prepare</h3>
                            <p style="font-size: 14px; line-height: 1.7; color: #94a3b8;">
                                We recommend reviewing stateful graph orchestration (LangGraph), vector search database indexing, multi-agent communication patterns, and resilient asynchronous pipeline execution. Please ensure you have a stable network connection and standard development environment prepared for code walkthroughs.
                            </p>

                            <!-- CALL TO ACTION BUTTON -->
                            <table role="presentation" cellspacing="0" cellpadding="0" style="margin: 30px auto;">
                                <tr>
                                    <td align="center" style="border-radius: 8px; background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);">
                                        <a href="https://calendly.com" target="_blank" style="display: inline-block; padding: 14px 32px; font-size: 15px; color: #ffffff; text-decoration: none; font-weight: 700; border-radius: 8px; letter-spacing: 0.5px;">
                                            Confirm Your Interview Slot &rarr;
                                        </a>
                                    </td>
                                </tr>
                            </table>

                            <p style="font-size: 14px; line-height: 1.7; color: #cbd5e1; text-align: center;">
                                Alternatively, simply reply to this email with 2–3 time slots that suit your availability over the next three business days.
                            </p>

                            <hr style="border: none; border-top: 1px solid #334155; margin: 30px 0;" />

                            <!-- SIGN-OFF -->
                            <p style="font-size: 14px; line-height: 1.6; color: #94a3b8; margin-bottom: 0;">
                                Warm regards,<br>
                                <strong style="color: #f8fafc;">Talent Acquisition Team</strong><br>
                                <span style="color: #38bdf8;">Agentic Employees Systems Inc.</span><br>
                                <a href="mailto:careers@agenticemployees.ai" style="color: #64748b; text-decoration: none; font-size: 12px;">careers@agenticemployees.ai</a>
                            </p>
                        </td>
                    </tr>

                    <!-- FOOTER -->
                    <tr>
                        <td align="center" style="background-color: #0f172a; padding: 20px; font-size: 11px; color: #64748b; border-top: 1px solid #334155;">
                            This is an automated operational transmission from the Agentic Employees AI Recruitment Engine.<br>
                            &copy; 2026 Agentic Employees Inc. All rights reserved. Confidential.
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def book_interview_slot(
    candidate_id: str,
    candidate_name: str,
    candidate_email: str,
    job_title: str,
    supabase
) -> bool:
    """Updates candidate status in Supabase and dispatches full HTML payload to Make.com."""
    # Update status in database
    supabase.table("candidates").update({"status": "booked"}).eq("id", candidate_id).execute()

    webhook_url = os.getenv("MAKE_WEBHOOK_URL")
    if not webhook_url:
        print("[Warning] MAKE_WEBHOOK_URL missing in .env.")
        return False

    subject = f"Interview Invitation: {job_title} | Agentic Employees"
    html_body = generate_booking_html(candidate_name, job_title)

    payload = {
        "event": "book_interview",
        "action": "send_booking_email",
        "candidate_id": candidate_id,
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "job_title": job_title,
        "subject": subject,
        "content": html_body
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        print(f"Make.com Webhook Fired: HTTP {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"[Error] Webhook failed: {e}")
        return False
