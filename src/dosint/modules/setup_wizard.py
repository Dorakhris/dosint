import configparser
from termcolor import colored

CONFIG_FILE = 'config.ini'

def run():
    print(colored("--- DOSINT API Key Setup Wizard ---", 'cyan'))
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if 'API_KEYS' not in config:
        config['API_KEYS'] = {}

    print("\nEnter your VirusTotal API Key. You can get this from the VirusTotal website.")
    vt_key = input("VirusTotal API Key (press Enter to skip): ")
    if vt_key:
        config['API_KEYS']['VIRUSTOTAL_API_KEY'] = vt_key
        print(colored("✅ VirusTotal key saved.", 'green'))

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    
    print(colored("\nSetup complete. Your keys are saved in config.ini.", 'cyan'))
