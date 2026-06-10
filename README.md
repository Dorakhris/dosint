<div align="center">

```
   ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗
   ██╔══██╗██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
   ██║  ██║██║   ██║███████╗██║██╔██╗ ██║   ██║   
   ██║  ██║██║   ██║╚════██║██║██║╚██╗██║   ██║   
   ██████╔╝╚██████╔╝███████║██║██║ ╚████║   ██║   
   ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
```

**The Intelligent OSINT, CTF, & Forensics Assistant**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dorakhris/dosint/pulls)

</div>


DOSINT is a command-line framework built to be a **force multiplier for investigators**. Most security tools are just single-purpose utilities, forcing you to manually copy-paste clues between a dozen different terminals. This breaks your focus and kills your momentum.

DOSINT fixes this. It's an investigative partner designed to keep you in the flow, automating tedious work and helping you decide what to do next.

##  Why DOSINT?

Most tools are like encyclopedias; they dump data on you. DOSINT is an analyst; it turns that data into a decision.

*   **The Interactive Pivot Engine:** Don't just get a list of results. DOSINT automatically finds new leads (emails, subdomains, usernames) and asks if you want to investigate them *right now*. Go from a domain, to an employee's email, to their GitHub profile without ever leaving the tool.
*   **Unified Investigation Cockpit:** Stop juggling tools. DOSINT combines workflows for different security disciplines into one cohesive interface.
    *   **Reconnaissance:** Discover subdomains and live web servers.
    *   **OSINT:** Investigate businesses and people.
    *   **CTF/Forensics:** Hunt for flags, strings, and metadata in local files and disk images.
    *   **Log Analysis:** Triage log files for Indicators of Compromise.
*   **Smart Automation:** Automate powerful Google Dorks to find exposed files and hidden pages. Orchestrate best-in-class external tools like `subfinder` and `httpx` to build a comprehensive picture of your target's attack surface.
*   **Built-in Memory:** Use the `report` command to add malicious indicators to a local intelligence database. DOSINT checks this database on every run, getting smarter and more customized to your needs over time.

<img width="1016" height="577" alt="Screenshot 2026-02-17 105627" src="https://github.com/user-attachments/assets/6736aff9-2552-4ba8-88f0-ec3dde8c28cf" />

<img width="1260" height="567" alt="image" src="https://github.com/user-attachments/assets/b3f2df65-e044-4e6f-885b-73d6017ccff3" />


##  Installation & Setup

DOSINT is designed for easy installation on any Linux system (like Kali or Ubuntu) with Python 3.9+ installed.

#### Step 1: Install Dependencies

DOSINT orchestrates several powerful open-source tools. You need to install them first.

**For Kali Linux:**
```bash
sudo apt update && sudo apt install -y subfinder httpx ffuf golang-go
```

**For Ubuntu / Debian:**
```bash
# Install core dependencies
sudo apt update && sudo apt install -y golang-go git python3-pip python3-venv

# Install Go-based tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/ffuf/ffuf/v2@latest

# Add Go's binary path to your shell (run this once)
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc && source ~/.bashrc
```

#### Step 2: Install DOSINT

```bash
# Clone the repository
git clone https://github.com/dorakhris/dosint.git
cd dosint

# Set up and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the tool in editable mode
pip install -e .
```

#### Step 3: First-Time Configuration

Run the interactive setup wizard to configure your API keys (e.g., for VirusTotal). This is required for some features to work.

```bash
dosint setup
```


##  Command Showcase

For detailed options on any command, use the `--help` flag (e.g., `dosint investigate person --help`).

| Command | Description | Example Usage |
| :--- | :--- | :--- |
| `dosint` | Displays the startup banner and basic info. | `dosint` |
| `dosint setup` | Runs the interactive wizard to configure API keys. | `dosint setup` |
| `dosint recon` | **[Recon]** Discovers live subdomains for a target. | `dosint recon example.com` |
| `dosint dork` | **[Recon]** Automates Google Dorking to find sensitive info. | `dosint dork --target example.com --dorks files,login` |
| `dosint investigate biz` | **[OSINT]** Gets a full report on a business domain. | `dosint investigate biz example.com` |
| `dosint investigate person` | **[OSINT]** Finds the online footprint of a person. | `dosint investigate person --username "johndoe"` |
| `dosint local` | **[CTF/Forensics]** Analyzes a local file for flags & metadata. | `dosint local evidence.dd --explain` |
| `dosint hash` | **[Threat Intel]** Checks a file hash against VirusTotal. | `dosint hash <sha256_hash>` |
| `dosint report` | **[Intelligence]** Adds a malicious indicator to your local DB. | `dosint report --domain "bad-site.net"` |
| `dosint analyze-log`| **[Triage]** Parses log files for Indicators of Compromise. | `dosint analyze-log auth.log --type ssh_debian` |

##  Contributing

Contributions, issues, and feature requests are welcome! Please check the [issues page](https://github.com/dorakhris/dosint/issues) to see if your idea has already been discussed.


##  License

Distributed under the MIT License. See the `LICENSE` file for more information.

## ⚠️ Disclaimer

DOSINT is a tool created for educational purposes, security research, and legal investigations. Users are responsible for their own actions and must comply with all applicable laws. Do not use this tool for any malicious activities.
```
