import os
import datetime
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()


def get_env(key: str, default: str = None, required: bool = True):
    """Safely fetch an environment variable with optional fallback."""
    value = os.getenv(key, default)
    if required and not value:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value


def generate_timestamp():
    """Returns a current timestamp string for filenames."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def deduplicate_leads(leads: list, key: str = "website") -> list:
    """Remove duplicate leads based on a specific key (e.g., website)."""
    seen = set()
    unique = []
    for lead in leads:
        val = lead.get(key)
        if val and val not in seen:
            unique.append(lead)
            seen.add(val)
    return unique


def log(message: str, prefix: str = "🔹"):
    """Standardized print logging."""
    print(f"{prefix} {message}")
