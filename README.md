
```markdown
<div align="left">

```
   ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗
   ██╔══██╗██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
   ██║  ██║██║   ██║███████╗██║██╔██╗ ██║   ██║   
   ██║  ██║██║   ██║╚════██║██║██║╚██╗██║   ██║   
   ██████╔╝╚██████╔╝███████║██║██║ ╚████║   ██║   
   ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
```

**An Intelligent OSINT, CTF, & Forensics Assistant**

</div>

<div align="left">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dorakhris/dosint/pulls)

</div>




DOSINT is a command-line framework built to be a force multiplier for investigators. Most OSINT tools are like encyclopedias; they dump a huge amount of raw data on you and expect you to do the hard work of connecting the dots.

**DOSINT is different. It's an investigative partner.** It's designed to work *with* you, automating tedious reconnaissance while actively helping you decide what to do next with its interactive **Pivot Engine**.

##  Key Features

*   **Intelligent Pivot Engine:** Automatically discovers new indicators (emails, domains, usernames) during an investigation and lets you instantly launch a new scan on them with a single keypress.
*   **Unified Investigation Cockpit:** Seamlessly bridges the gap between different security disciplines. Use one tool for:
*   **Open-Source Intelligence (OSINT):** Investigate businesses and people.
*   **Capture The Flag (CTF):** Hunt for flags and metadata in local files.
*   **Digital Forensics:** Perform EXIF analysis on images and documents.
*   **Log Analysis:** Triage log files for Indicators of Compromise (IOCs).
*   **Automated Google Dorking:** Unleash the power of advanced Google searching to find exposed files, hidden login pages, and sensitive information.
*   **Real-Time Feedback:** Get immediate results for long-running tasks like username searches, making the tool feel responsive and alive.
*   **Local Intelligence Database:** Use the `report` command to build your own private database of bad actors. DOSINT automatically checks this database during every investigation.

##  Demo

*(This is where you would place a GIF showing the Pivot Engine in action. A tool like `asciinema` is perfect for creating terminal recording GIFs.)*

![DOSINT Demo Placeholder](https://user-images.githubusercontent.com/assets/placeholder.gif)

##  Installation

DOSINT is designed for easy installation on any system with Python 3.9+ and pip.

1.  **Clone or Download:** For development, it's best to clone the repository.

    ```bash
    git clone https://github.com/dorakhris/dosint.git
    cd dosint
    ```

2.  **Set up Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    
3. **Install Dependencies & Tool:**

    ```bash
    pip install -e .
    ```


##  First-Time Setup

Before you can use modules that rely on external services, you need to configure your API keys. DOSINT includes an interactive setup wizard to make this easy.

Run the following command and follow the prompts:

```bash
dosint setup
```

This will create a `config.ini` file where your keys are securely stored, separate from the source code.

##  Usage & Command Reference

Here are the main commands and how to use them. For detailed options on any command, use the `--help` flag (e.g., `dosint investigate person --help`).

### `investigate`
The core command for running a full OSINT investigation.

*   **Investigate a Business Domain:**
    ```bash
    dosint investigate biz nmap.org
    ```
    *(Checks local DB, WHOIS, VirusTotal, and scrapes for emails.)*

*   **Investigate a Person:**
    ```bash
    dosint investigate person --username "torvalds"
    dosint investigate person --email "example@gmail.com"
    ```
    *(Checks social media, phone info, and (with API key) data breaches.)*

### `dork`
Automate Google Dorking to find sensitive information.

*   **Run All Dorks Against a Target:**
    ```bash
    dosint dork --target "tesla.com"
    ```
*   **Run Specific Dork Categories:**
    ```bash
    dosint dork --target "tesla.com" --dorks "files,login"
    ```
    *(Available categories: `files`, `login`, `subdomains`, `directory_listing`, `public_exposure`)*

### `local`
Analyze a local file for CTF flags and forensic data.

*   **Check a File:**
    ```bash
    dosint local /path/to/evidence.jpg
    ```
    *(Automatically checks file type, size, EXIF metadata, and greps for flag patterns.)*

### `hash`
Check a file hash against the VirusTotal database.
```bash
dosint hash 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f
```

### `analyze-log`
Perform a quick triage and analysis of a log file.
```bash
dosint analyze-log /var/log/auth.log --type ssh_debian
```

### `report`
Add an indicator to your local intelligence database.
```bash
dosint report --domain "suspicious-site.net" --phone "+15551234567"
```

##  Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/dorakhris/dosint/issues).

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

##  License

Distributed under the MIT License. See the `LICENSE` file for more information.

##  Disclaimer

DOSINT is a tool designed for professional security researchers, CTF players, and those in the security industry. It should only be used for ethical and legal purposes. The user is responsible for their own actions.
```
