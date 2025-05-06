from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from services.maps_scraper import scrape_businesses
from services.gpt_analysis import analyze_leads
from services.html_report import build_html_report, save_report_as_pdf
from services.email_sender import send_email_with_attachment
import datetime

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "✅ LeadSiphon API is running!", 200

@app.route("/generate", methods=["POST"])
def generate_leads():
    try:
        data = request.json
        required_fields = ["niche", "location", "service", "email", "count"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        niche = data["niche"]
        location = data["location"]
        service = data["service"]
        email = data["email"]
        count = int(data["count"])

        print(f"🔎 Scraping {count} businesses for '{niche}' in '{location}'...")
        businesses = scrape_businesses(niche, location, count)

        if not businesses:
            return jsonify({"error": "No businesses found."}), 404

        print(f"🤖 Running GPT analysis...")
        analyzed = analyze_leads(businesses, service)

        if not analyzed:
            return jsonify({"error": "GPT analysis failed"}), 500

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"leads_{niche}_{location}_{count}_{timestamp}"
        html = build_html_report(analyzed, niche, location, service)
        pdf_path = save_report_as_pdf(html, filename)

        send_email_with_attachment(
            to=email,
            subject=f"Your {count} LeadSiphon leads: {niche} in {location}",
            html_content=html,
            attachment_path=pdf_path
        )

        return jsonify({"message": f"✅ Report sent to {email}!"}), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
