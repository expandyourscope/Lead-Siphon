import requests
from config import MAILGUN_API_KEY, MAILGUN_DOMAIN, EMAIL_FROM
import os

def send_email(to_email, subject, body_text, attachment_path):
    print("📤 Preparing to send email via Mailgun...")

    if not os.path.exists(attachment_path):
        print(f"❌ Attachment not found: {attachment_path}")
        return False

    with open(attachment_path, "rb") as f:
        files = [("attachment", (os.path.basename(attachment_path), f.read()))]

    html_body = f"""
    <html>
        <body style='font-family: Arial, sans-serif; background: #f9f9f9; padding: 30px;'>
            <div style='max-width: 600px; background: white; padding: 30px; margin: auto; border: 1px solid #ddd; border-radius: 8px;'>
                <h2 style='color: #2c3e50;'>📄 Your LeadSiphon Report is Ready</h2>
                <p>Hi there,</p>
                <p>Thanks for using <strong>LeadSiphon</strong> to generate leads. Your custom PDF report is attached, containing:</p>
                <ul>
                    <li>Qualified leads in your chosen niche & location</li>
                    <li>GPT-analyzed insights and sales strategies</li>
                    <li>Growth indicators and timing tips</li>
                </ul>
                <p><strong>Need more leads?</strong></p>
                <a href='https://www.expandyourscope.com/coming-soon-03' style='background: #007BFF; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>➕ Get More Leads</a>
                <p style='margin-top: 40px;'>Best,<br><strong>The LeadSiphon Team</strong></p>
                <hr>
                <p style='font-size: 12px; color: #999;'>LeadSiphon • AI-powered outreach<br>{MAILGUN_DOMAIN}</p>
            </div>
        </body>
    </html>
    """

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            files=files,
            data={
                "from": EMAIL_FROM,
                "to": [to_email],
                "subject": subject,
                "text": body_text,
                "html": html_body
            }
        )

        if response.status_code == 200:
            print(f"✅ Email successfully sent to {to_email}")
            return True
        else:
            print(f"❌ Mailgun API error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
