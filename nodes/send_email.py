import os
import requests
from langchain_groq import ChatGroq
from prompts.email_prompt import DECLINE_EMAIL_PROMPT, OFFER_EMAIL_PROMPT


def wrap_in_black_html_template(subject: str, content: str) -> str:
    """Wraps text in a dark-mode / black background HTML email template."""
    paragraphs = "".join(
        [
            f"<p style='margin-bottom: 16px;'>{p.strip()}</p>"
            for p in content.split("\n\n")
            if p.strip()
        ]
    )

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #000000; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #ffffff;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #000000; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table role="presentation" width="100%" style="max-width: 600px; background-color: #121212; border: 1px solid #2a2a2a; border-radius: 12px; padding: 32px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
                    <!-- Header Bar -->
                    <tr>
                        <td style="border-bottom: 1px solid #2a2a2a; padding-bottom: 20px; margin-bottom: 20px;">
                            <h2 style="margin: 0; color: #ffffff; font-size: 20px; font-weight: 600; letter-spacing: -0.5px;">
                                Hiring Team
                            </h2>
                        </td>
                    </tr>
                    <!-- Main Content -->
                    <tr>
                        <td style="padding-top: 24px; color: #d1d5db; font-size: 15px; line-height: 1.6;">
                            {paragraphs}
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="border-top: 1px solid #2a2a2a; padding-top: 24px; margin-top: 32px; text-align: center; color: #6b7280; font-size: 12px;">
                            <p style="margin: 0;">This is an automated notification regarding your job application.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def draft_and_send_email(to_email: str, subject: str, plain_body: str):
    """Triggers Make.com Webhook with dark HTML payload."""
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")

    html_content = wrap_in_black_html_template(subject, plain_body)

    if not webhook_url:
        print(f"--- [EMAIL DRY-RUN] To: {to_email} ---")
        print(
            f"Subject: {subject}\nHTML Payload Generated ({len(html_content)} chars)\n"
        )
        return

    # Payload keys matched to your Make.com mapping (2. recipient, 2. subject, 2. email)
    payload = {
        "recipient": to_email,
        "to_email": to_email,
        "subject": subject,
        "email": html_content,
        "html_body": html_content,
        "body": plain_body,
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in [200, 201, 202]:
            print(
                f"Successfully triggered Make.com HTML email webhook for {to_email}"
            )
        else:
            print(
                f"Failed to trigger Make.com webhook: {response.status_code} - {response.text}"
            )
    except Exception as e:
        print(f"Error calling Make.com Webhook: {e}")


def send_decline_email(
    candidate_name: str, candidate_email: str, job_title: str, rationale: str
):
    """Generates rejection email via Groq and dispatches HTML email via Make.com."""
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    prompt = DECLINE_EMAIL_PROMPT.format(
        candidate_name=candidate_name,
        job_title=job_title,
        rationale=rationale,
    )
    email_body = llm.invoke(prompt).content
    draft_and_send_email(
        to_email=candidate_email,
        subject=f"Update on your application for {job_title}",
        plain_body=str(email_body),
    )


def send_offer_email(candidate_name: str, candidate_email: str, job_title: str):
    """Generates job offer email via Groq and dispatches HTML email via Make.com."""
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    prompt = OFFER_EMAIL_PROMPT.format(
        candidate_name=candidate_name,
        job_title=job_title,
    )
    email_body = llm.invoke(prompt).content
    draft_and_send_email(
        to_email=candidate_email,
        subject=f"Job Offer: {job_title}",
        plain_body=str(email_body),
    )
