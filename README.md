<img width="843" height="310" alt="DOSINT" src="https://github.com/user-attachments/assets/47ddf587-e99d-45d8-8dc8-8759bc04b5be" />

# DOSINT - An Intelligent OSINT, CTF, & Forensics Assistant

<p align="center">
  <img src="https://user-images.githubusercontent.com/assets/dosint-logo-placeholder.png" alt="DOSINT Logo" width="200"/>
</p>

DOSINT is a command-line tool designed to be a "force multiplier" for investigators. It automates tedious reconnaissance and actively helps you decide what to do next with its interactive **Pivot Engine**. It combines OSINT, local file forensics, and CTF utilities into a single, cohesive toolkit.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

##  Key Features

- **Intelligent Pivot Engine:** Automatically discovers new leads (emails, domains) during an investigation and lets you instantly launch a new scan on them.
- **Unified Cockpit:** One tool for OSINT (people, businesses), file forensics (EXIF, flags), and log analysis.
- **Automated Google Dorking:** Finds exposed files, hidden login pages, and sensitive information.
- **Local Intelligence Database:** Flag bad actors with the `report` command and DOSINT will remember them in future scans.

---

##  Quick Start

### 1. Installation

This tool can be installed on any system with Python 3.9+ and Git.

```bash
# Clone the repository
git clone https://github.com/dorakhris/dosint.git

# Navigate into the directory
cd dosint

# Set up and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the tool and its dependencies
pip install -e .
```

### 2. First-Time Setup

Run the interactive setup wizard to configure your API keys (e.g., for VirusTotal).

```bash
dosint setup
```

---

##  Usage Examples

For detailed options on any command, use the `--help` flag (e.g., `dosint investigate person --help`).

- **Investigate a business and pivot on its contacts:**
  ```bash
  dosint investigate biz example.com
  ```

- **Find a person's social media footprint:**
  ```bash
  dosint investigate person --username "johndoe"
  ```

- **Hunt for sensitive files on a website:**
  ```bash
  dosint dork --target example.com --dorks files
  ```

- **Analyze a downloaded CTF file for flags and metadata:**
  ```bash
  dosint local /path/to/evidence.jpg
  ```

- **Check a file hash against 70+ AV vendors:**
  ```bash
  dosint hash 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f
  ```

---

##  Contributing

Contributions, issues, and feature requests are welcome! Please check the [issues page](https://github.com/dorakhris/dosint/issues).

##  License

Distributed under the MIT License.

##  Disclaimer

DOSINT should only be used for ethical and legal purposes. The user is responsible for their own actions.

```

