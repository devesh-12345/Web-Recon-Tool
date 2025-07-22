# Web Recon Tool — Website Reconnaissance Report Generator

**Web Recon Tool** is a cybersecurity reconnaissance tool built with Python and PyQt5.  
It automates common information-gathering tasks like WHOIS lookup, Nmap scanning, Curl header capture, NSLookup, and Traceroute — and exports professional-grade reports in **PDF and TXT formats**.

Designed for:
- Cybersecurity students
- Ethical hackers & bug bounty hunters
- Red teamers & pentesting interns

---

## Features
- WHOIS information extraction (domain registrant data)
- Curl header retrieval (content-type, cookies, cache info)
- NSLookup with IPv4 and IPv6 support
- Network path tracing via Traceroute/Tracert
- (Optional) Nmap scanning for open ports
- PyQt5 GUI with modern UI
- Exports well-formatted PDF and TXT reports
- Icon support in executable and window
- Runs on other systems (no Python required on Windows)
- Modern PyQt5 GUI with responsive layout
- Compatible with Windows 10/11

---

## Screenshots

![UI](https://github.com/user-attachments/assets/3b609966-f7d2-4ac5-8717-c00b994c6e59)
![RUN](https://github.com/user-attachments/assets/1e498a52-8e15-48c9-9752-c4e84dfbf829)

---

## Example Reports

You can find ready-made scan reports in the [`example-reports/`](./example-reports/) folder:

- [✔ example-scan-report-2025-07-22.pdf](./Example_Reports/example-scan-report-2025-07-22.pdf)
- [✔ example-scan-report-2025-07-22.txt](./Example_Reports/example-scan-report-2025-07-22.txt)

---

## Installation

### Windows
1. Download the latest release `.exe` from [Releases](https://github.com/devesh-12345/Web-Recon-Tool/releases/tag/v1.0.0)
2. Run it directly — no Python required
3. WHOIS and other system tools work out-of-the-box

---

## Usage Tips & Notes

- **Input URL Format**:
    - The input must follow this format:
      ```
      https://www.example.com
      ```
    - Do **not** include:
        - Path segments like `/login`, `/index.html`
        - Query strings like `?id=123`
        - Subdomains (e.g., `blog.example.com`) — only use main domain with `www.`

- **Network Path Tracing**:
    - When running `traceroute` or `tracert`, you may see a small pop-up system window (especially on Windows).
    - **Do not close this window manually** — it will interrupt the scan and cause incomplete results.

- **Report Format**:
    - TXT and PDF exports are saved in the `output/` folder by default (Created automatically after running your first scan).
    - You can open the exported `.pdf` with any standard viewer.

- **Internet Access**:
    - WHOIS lookups and header scans require an active internet connection.

---

## System Required

The following command-line tools must be available on your system's `PATH` for the tool to function correctly:
- `whois`
- `curl`
- `nslookup`
- `tracert` for Windows operating systems
- `nmap` (optional, but recommended)

### Nmap Setup (Required for Port Scanning)

If you want to use the Nmap scanning feature:
1. Download Nmap from [https://nmap.org/download.html]
2. During installation, ensure the **“Add Nmap to PATH”** option is checked. Or add it manually to the path.
3. Verify installation by running:
   ```bash
    nmap --version

If not installed or not added to PATH, the Nmap scan will be skipped silently.

---

## Build Instructions Used (PyInstaller)

### Windows Build
pyinstaller --onefile --windowed --icon="src/icon.ico" --add-data="src/icon.ico;src" --add-data="path/to/public_suffix_list.dat;whois/data" src/Web_Recon_Tool.py

---

## Python Modules Used

This project internally uses the following Python modules:

- Python 3.8+
- Python Module: 
    - whois
    - subprocess
    - json
    - requests
    - bs4
    - platform
    - shutil
    - os
    - PyQt5
    - datetime
    - time
    - fpdf
    - re
    - socket
    - sys

No need to install Python or these modules when using the Windows `.exe` version — they're bundled via PyInstaller.

## System Tools used

This project internally uses the following system tools.

- CLI Tools (preinstalled on most systems):
    1. whois
    2. curl
    3. nslookup
    4. traceroute for UNIX or tracert for Windows operating systems 
    5. nmap (optional)

---

## Acknowledgements

- [PyQt5](https://pypi.org/project/PyQt5/)
- [Python-Whois](https://pypi.org/project/whois/)
- [FPDF](https://py-pdf.github.io/fpdf2/)

--

## Author

Devesh Bhangale
[LinkedIn Profile](https://www.linkedin.com/in/devesh-bhangale-b15913211/)
