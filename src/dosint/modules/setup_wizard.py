import configparser
import os
from termcolor import colored

CONFIG_FILE = 'config.ini'

def run():
    print(colored("--- DOSINT API Key Setup Wizard ---", 'cyan'))
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if 'API_KEYS' not in config:
        config['API_KEYS'] = {}

    # VirusTotal Setup
    print("\nEnter your VirusTotal API Key (used for domain/file reputation checks).")
    vt_key = input("VirusTotal API Key (press Enter to skip): ").strip()
    if vt_key:
        config['API_KEYS']['VIRUSTOTAL_API_KEY'] = vt_key
        print(colored("✅ VirusTotal key updated.", 'green'))

    # DeHashed Setup
    print("\nEnter your DeHashed credentials (used for credential breach lookups).")
    dh_email = input("DeHashed Email (press Enter to skip): ").strip()
    dh_key = input("DeHashed API Key (press Enter to skip): ").strip()
    if dh_email:
        config['API_KEYS']['DEHASHED_EMAIL'] = dh_email
    if dh_key:
        config['API_KEYS']['DEHASHED_API_KEY'] = dh_key
    if dh_email or dh_key:
        print(colored("✅ DeHashed credentials updated.", 'green'))

    # Epieos Setup
    print("\nEnter your Epieos API Key (used for advanced email profiling).")
    ep_key = input("Epieos API Key (press Enter to skip): ").strip()
    if ep_key:
        config['API_KEYS']['EPIEOS_API_KEY'] = ep_key
        print(colored("✅ Epieos key updated.", 'green'))

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    
    print(colored("\nConfiguration saved successfully inside 'config.ini'.", 'cyan'))
