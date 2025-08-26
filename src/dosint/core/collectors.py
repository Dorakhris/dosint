# src/dosint/core/collectors.py

import configparser
import requests
import whois
import os
import re
import time
import random
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from ddgs import DDGS
from termcolor import colored

def _get_api_key(key_name):
    """Reads an API key from the config.ini file."""
    config = configparser.ConfigParser()
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.ini')
        config.read(config_path)
        return config['API_KEYS'].get(key_name)
    except Exception:
        return None

def robust_google_search(query, num_results=5, pause=5.0):
    """A more 'human-like' Google search function using requests and BeautifulSoup."""
    print(f"  -> (Using Google) Searching: {query}")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    headers = {"User-Agent": user_agent}
    encoded_query = quote_plus(query)
    search_url = f"https://www.google.com/search?q={encoded_query}&num={num_results}&hl=en"
    
    results = []
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        link_elements = soup.find_all('div', class_='g')
        for element in link_elements:
            link_tag = element.find('a')
            if link_tag and link_tag.get('href'):
                url = link_tag.get('href')
                if url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&sa=')[0]
                if url.startswith("http"):
                    results.append(url)
        
        random_delay = pause + random.uniform(1, 4)
        print(f"     (Pausing for {random_delay:.1f}s to avoid rate-limiting...)")
        time.sleep(random_delay)
        return results[:num_results]
    except requests.RequestException as e:
        return {"error": str(e)}

def robust_ddg_search(query, num_results=5):
    """Performs a search using DuckDuckGo, which is more resilient to blocking."""
    print(f"  -> (Using DuckDuckGo) Searching: {query}")
    results = []
    try:
        with DDGS(timeout=10) as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append(r['href'])
        return results
    except Exception as e:
        return {"error": str(e)}

def get_virustotal_report(domain):
    """Gets domain reputation from VirusTotal."""
    api_key = _get_api-key("VIRUSTOTAL_API_KEY")
    if not api_key: return {"error": "VIRUSTOTAL_API_KEY not set in config.ini"}
    url = f'https://www.virustotal.com/api/v3/domains/{domain}'
    try:
        r = requests.get(url, headers={'x-apikey': api_key}, timeout=10)
        return r.json()['data']['attributes']['last_analysis_stats'] if r.status_code == 200 else {"error": f"API Error {r.status_code}"}
    except requests.RequestException: return {"error": "Network error"}

def get_virustotal_hash_report(file_hash):
    """Gets file hash reputation from VirusTotal."""
    api_key = _get_api_key("VIRUSTOTAL_API_KEY")
    if not api_key: return {"error": "VIRUSTOTAL_API_KEY not set in config.ini"}
    url = f'https://www.virustotal.com/api/v3/files/{file_hash}'
    try:
        r = requests.get(url, headers={'x-apikey': api_key}, timeout=10)
        return r.json()['data']['attributes'] if r.status_code == 200 else {"error": "Hash not found"}
    except requests.RequestException: return {"error": "Network error"}

def get_domain_info(domain):
    """Gets domain registration details via WHOIS."""
    try:
        w = whois.whois(domain)
        return {"creation_date": w.creation_date, "registrar": w.registrar}
    except Exception as e: return {"error": f"WHOIS failed: {e}"}

def get_phone_info(phone_number_str):
    """Gets basic info about a phone number."""
    try:
        p = phonenumbers.parse(phone_number_str)
        if not phonenumbers.is_valid_number(p): return {"error": "Invalid phone format."}
        return {"country": geocoder.description_for_number(p, "en"), "carrier": carrier.name_for_number(p, "en") or "N/A"}
    except Exception as e: return {"error": f"Could not parse phone: {e}"}

def get_username_hits(username):
    """Checks a predefined list of popular sites for a username."""
    sites = {"GitHub": f"https://github.com/{username}", "Twitter": f"https://twitter.com/{username}", "Instagram": f"https://www.instagram.com/{username}/"}
    found = []
    print(colored(f"[*] Checking {len(sites)} sites for '{username}'...", 'cyan'))
    for site, url in sites.items():
        try:
            r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                print(colored(f"[+] Found {site}: {url}", 'green'))
                found.append({"site": site, "url": url})
        except requests.RequestException: continue
    return found

def scrape_page_for_emails(domain):
    """Scrapes the homepage of a domain to find email addresses."""
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
