import openai
import json
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def analyze_business_with_gpt(business: dict, user_service: str) -> dict:
    """Generate a GPT-powered outreach analysis for a specific business."""
    
    prompt = f"""
You are an AI marketing strategist assisting a freelancer who offers '{user_service}' services.

Review the following business and create a tailored outreach summary from the freelancer’s perspective.

Business:
- Name: {business.get('name', 'N/A')}
- Website: {business.get('website', 'N/A')}
- Address: {business.get('address', 'N/A')}

Respond strictly in JSON with the following keys:

{{
  "opportunities": "Specific areas where '{user_service}' services could help this business.",
  "pitch": "A direct, personalized 1–2 sentence pitch to the business owner.",
  "why_now": "Why this moment is ideal to offer your services.",
  "growth": "Any visible signs of momentum or risk from their public presence or market."
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        raw_text = response.choices[0].message.content.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text.strip("```json").strip("```").strip()

        result = json.loads(raw_text)

        expected_keys = ["opportunities", "pitch", "why_now", "growth"]
        if not all(key in result for key in expected_keys):
            missing = [key for key in expected_keys if key not in result]
            raise ValueError(f"Incomplete GPT response — missing: {missing}")

        return result

    except Exception as error:
        print(f"⚠️ GPT analysis error for {business.get('name')}: {error}")
        return {
            "opportunities": "No insights available. Consider manual review.",
            "pitch": "GPT analysis failed. A manual pitch is recommended.",
            "why_now": "Unable to assess timing.",
            "growth": "No signals detected."
        }
