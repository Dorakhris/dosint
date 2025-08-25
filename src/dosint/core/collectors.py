import configparser
import requests
import whois
import os
import re
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier
from bs4 import BeautifulSoup

def _get_api_key(key_name):
    config = configparser.ConfigParser()
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.ini')
        config.read(config_path)
        return config['API_KEYS'].get(key_name)
    except Exception: return None

def get_virustotal_report(domain):
    api_key = _get_api_key("VIRUSTOTAL_API_KEY")
    if not api_key: return {"error": "VIRUSTOTAL_API_KEY not set in config.ini"}
    url = f'https://www.virustotal.com/api/v3/domains/{domain}'
    try:
        r = requests.get(url, headers={'x-apikey': api_key}, timeout=10)
        return r.json()['data']['attributes']['last_analysis_stats'] if r.status_code == 200 else {"error": f"API Error {r.status_code}"}
    except requests.RequestException: return {"error": "Network error"}

def get_virustotal_hash_report(file_hash):
    api_key = _get_api_key("VIRUSTOTAL_API_KEY")
    if not api_key: return {"error": "VIRUSTOTAL_API_KEY not set in config.ini"}
    url = f'https://www.virustotal.com/api/v3/files/{file_hash}'
    try:
        r = requests.get(url, headers={'x-apikey': api_key}, timeout=10)
        return r.json()['data']['attributes'] if r.status_code == 200 else {"error": "Hash not found"}
    except requests.RequestException: return {"error": "Network error"}

def get_domain_info(domain):
    try:
        w = whois.whois(domain)
        return {"creation_date": w.creation_date, "registrar": w.registrar}
    except Exception as e: return {"error": f"WHOIS failed: {e}"}

def get_phone_info(phone_number_str):
    try:
        p = phonenumbers.parse(phone_number_str)
        if not phonenumbers.is_valid_number(p): return {"error": "Invalid phone format."}
        return {"country": geocoder.description_for_number(p, "en"), "carrier": carrier.name_for_number(p, "en") or "N/A"}
    except Exception as e: return {"error": f"Could not parse phone: {e}"}

def get_username_hits(username):
    sites = {"GitHub": f"https://github.com/{username}", "Twitter": f"https://twitter.com/{username}", "Instagram": f"https://www.instagram.com/{username}/"}
    found = []
    print(f"[*] Checking {len(sites)} sites for '{username}'...")
    for site, url in sites.items():
        try:
            if requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'}).status_code == 200:
                found.append({"site": site, "url": url})
        except requests.RequestException: continue
    return found

def scrape_page_for_emails(domain):
    emails = set()
    try:
        r = requests.get(f"https://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        emails.update(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text))
    except requests.RequestException:
        try:
            r = requests.get(f"http://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            emails.update(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text))
        except requests.RequestException: return []
    return list(emails)
