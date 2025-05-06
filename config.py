import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (DO NOT hardcode these values — keep them in your .env file)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
WKHTMLTOPDF_PATH = os.getenv("WKHTMLTOPDF_PATH")

# Email config
EMAIL_FROM = f"LeadSiphon <leads@{MAILGUN_DOMAIN}>"

# Lead pricing tiers
TIERS = {
    5: 9.99,
    25: 19.99,
    50: 29.99,
    100: 49.99
}
