from scraper import scrape_businesses
from ai_analysis import analyze_business_with_gpt
from html_report import create_report_html, save_report_as_pdf
from email_sender import send_email
from config import TIERS

import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)


def run_lead_generation(niche, location, email, lead_count, service):
    try:
        print("🔍 Starting business scraping...")
        leads = scrape_businesses(niche, location, lead_count)
        print(f"✅ Scraped {len(leads)} businesses.")

        if len(leads) < lead_count:
            print("⚠️ Not enough leads found, proceeding with fallback mechanism.")

        analyzed_leads = []
        print("🤖 Starting GPT analysis...")
        for index, lead in enumerate(leads):
            print(f"🔎 ({index + 1}/{len(leads)}) Analyzing: {lead.get('name')}")
            try:
                gpt_analysis = analyze_business_with_gpt(lead, service)

                required_fields = ["pitch", "opportunities", "why_now", "growth"]
                if not all(key in gpt_analysis for key in required_fields):
                    print(f"⚠️ Incomplete GPT analysis for {lead.get('name')}, skipping.")
                    continue

                analyzed_leads.append({**lead, **gpt_analysis})
            except Exception as gpt_err:
                print(f"⚠️ GPT analysis failed for {lead.get('name')}: {gpt_err}")

        if not analyzed_leads:
            print("❌ No valid leads after analysis, terminating.")
            return False

        print("📄 Generating HTML and PDF reports...")
        price = TIERS.get(lead_count, 0.0)
        html_report = create_report_html(analyzed_leads, niche, location, service, price)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"LeadSiphon_{niche}_{location}_{lead_count}_{timestamp}.pdf"
        pdf_path = save_report_as_pdf(html_report, pdf_filename)

        print("📬 Sending email...")
        subject = f"Your LeadSiphon Report for {niche.capitalize()} Leads in {location.capitalize()}"
        email_body = (
            f"Hello,\n\nYour LeadSiphon lead report is ready.\n\n"
            f"Details:\n- Niche: {niche}\n- Location: {location}\n- Service: {service}\n"
            f"- Leads Count: {lead_count}\n- Total Cost: ${price:.2f}\n\n"
            "The report is attached as a PDF document.\n\nThank you for using LeadSiphon!"
        )

        send_success = send_email(email, subject, email_body, pdf_path)
        if send_success:
            print(f"✅ Report successfully sent to {email}")
        else:
            print("❌ Failed to send email.")

        return send_success

    except Exception as e:
        print("❌ Critical error during lead generation:", e)
        return False


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    required_fields = ['niche', 'location', 'service', 'email', 'lead_count']
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    success = run_lead_generation(
        niche=data['niche'],
        location=data['location'],
        email=data['email'],
        lead_count=int(data['lead_count']),
        service=data['service']
    )

    if success:
        return jsonify({"status": "success", "message": "Leads generated and emailed."}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to generate leads."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)