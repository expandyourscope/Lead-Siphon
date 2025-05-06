import requests
from config import GOOGLE_API_KEY


def scrape_businesses(niche, location, limit=25):
    query = f"{niche} in {location}"
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": GOOGLE_API_KEY}

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    data = response.json()
    businesses = []

    for place in data.get("results", []):
        if len(businesses) >= limit:
            break

        if place.get("business_status") != "OPERATIONAL":
            continue

        business = {
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "place_id": place.get("place_id"),
            "website": fetch_website(place.get("place_id")),
            "source": "primary"
        }
        businesses.append(business)

    return businesses


def fetch_website(place_id):
    endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "website", "key": GOOGLE_API_KEY}

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    result = response.json().get("result", {})
    return result.get("website", "")


def suggest_fallback_niches(primary_niche):
    niche_map = {
        "yoga": ["pilates", "fitness studio", "massage therapy"],
        "horse riding": ["equestrian center", "outdoor adventure", "farm tours"],
        "dentist": ["orthodontist", "dental clinic", "oral surgeon"],
        "marketing agency": ["branding agency", "seo company", "creative consultant"],
        "web design": ["digital agency", "IT consulting", "graphic design"],
    }
    return niche_map.get(primary_niche.lower(), ["consulting", "freelancer", "local service"])


def scrape_with_fallback(niche, location, limit=25):
    print(f"🔍 Scraping primary niche: '{niche}'")
    primary_leads = scrape_businesses(niche, location, limit)

    if len(primary_leads) >= limit:
        print(f"✅ Sufficient primary leads found: {len(primary_leads)}")
        return primary_leads[:limit]

    print(f"⚠️ Only {len(primary_leads)} primary leads found. Initiating fallback...")

    fallback_niches = suggest_fallback_niches(niche)
    additional_leads = []

    for fallback_niche in fallback_niches:
        remaining_needed = limit - len(primary_leads) - len(additional_leads)
        if remaining_needed <= 0:
            break

        print(f"🔄 Scraping fallback niche: '{fallback_niche}'")
        fallback_results = scrape_businesses(fallback_niche, location, remaining_needed)

        for lead in fallback_results:
            lead["source"] = "secondary"

        additional_leads.extend(fallback_results)

    combined_leads = primary_leads + additional_leads
    print(f"✅ Total leads gathered: {len(combined_leads)}")

    return combined_leads[:limit]
