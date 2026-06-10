import configparser, requests, whois, os, re, time, random, phonenumbers
from phonenumbers import geocoder, carrier
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from ddgs import DDGS
from termcolor import colored

def _get_api_key(k):
    c = configparser.ConfigParser()
    c.read(os.path.join(os.path.dirname(__file__), '../../../config.ini'))
    return c.get('API_KEYS', k, fallback=None)

def get_virustotal_report(d):
    k = _get_api_key("VIRUSTOTAL_API_KEY")
    if not k: return {"error": "API Key missing"}
    try:
        r = requests.get(f'https://www.virustotal.com/api/v3/domains/{d}', headers={'x-apikey': k}, timeout=10)
        return r.json()['data']['attributes']['last_analysis_stats'] if r.status_code == 200 else {"error": "API Error"}
    except: return {"error": "Network Error"}

def get_virustotal_hash_report(h):
    k = _get_api_key("VIRUSTOTAL_API_KEY")
    if not k: return {"error": "API Key missing"}
    try:
        r = requests.get(f'https://www.virustotal.com/api/v3/files/{h}', headers={'x-apikey': k}, timeout=10)
        return r.json()['data']['attributes'] if r.status_code == 200 else {"error": "Hash not found"}
    except: return {"error": "Network Error"}

def get_domain_info(d):
    try:
        w = whois.whois(d)
        return {"creation_date": w.creation_date, "registrar": w.registrar}
    except Exception as e: return {"error": str(e)}

def get_phone_info(p):
    try:
        num = phonenumbers.parse(p)
        return {"country": geocoder.description_for_number(num, "en"), "carrier": carrier.name_for_number(num, "en")}
    except: return {"error": "Invalid phone"}

def get_username_hits(u):
    sites = {"GitHub": f"https://github.com/{u}", "Twitter": f"https://twitter.com/{u}"}
    found =[]
    for s, url in sites.items():
        try:
            if requests.get(url, timeout=5).status_code == 200: found.append({"site": s, "url": url})
        except: pass
    return found

def scrape_page_for_emails(d):
    try:
        r = requests.get(f"https://{d}", timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        return list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)))
    except: return[]

def robust_google_search(query, num_results=5, pause=5.0):
    url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results}&hl=en"
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = [l.find('a')['href'] for l in soup.find_all('div', class_='g') if l.find('a')]
        time.sleep(pause + random.uniform(1, 4))
        return results[:num_results]
    except Exception as e: return {"error": str(e)}

def robust_ddg_search(query, num_results=5):
    try:
        with DDGS(timeout=10) as ddgs:
            return [r['href'] for r in ddgs.text(query, max_results=num_results)]
    except Exception as e: return {"error": str(e)}
