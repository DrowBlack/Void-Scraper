
# 🛡️ Advanced Proxy Scraper & Checker

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Releases](https://img.shields.io/github/v/release/DrowBlack/Void-Scraper?display_name=release&labelColor=gray&color=green)](https://github.com/DrowBlack/Void-Scraper/releases/latest)
[![Code Size](https://img.shields.io/github/languages/code-size/DrowBlack/Void-Scraper?style=flat&color=blue)](https://github.com/DrowBlack/Void-Scraper)
[![Forks](https://img.shields.io/github/forks/DrowBlack/Void-Scraper?style=flat&color=purple)](https://github.com/DrowBlack/Void-Scraper/network/members)

A high-performance, automated network utility designed to scrape, validate, and analyze public proxies.

This tool aggregates proxies from various public sources and performs real-time connectivity tests across multiple protocols (**HTTP, SOCKS4, SOCKS5**). It provides detailed metrics such as latency (ms) and server geolocation, ensuring only reliable proxies are exported for your workflow.

[![Discord](https://img.shields.io/badge/Contact-%20onDiscord-5865F2?logo=discord&logoColor=white)](https://discordapp.com/users/672371899225079848)

Portfolio: [DrowBlack.lol](https://drowblack.lol/)

---

## 🚀 Key Features

* **Multi-Protocol Support:** Seamlessly handles `HTTP`, `SOCKS4`, and `SOCKS5` protocols.
* **Intelligent Scraping:** Aggregates proxy lists from pre-defined public repositories automatically.
* **Deep Analysis:** Validates each proxy with precision:
    * ⚡ **Latency Measurement:** Calculates the response time (in ms) to ensure speed.
    * 🌍 **Geo-Location:** Identifies the hosting country/city of the proxy server.
* **Clean Output:** Automatically exports valid proxies to a structured `.txt` file for immediate integration.
* **Live CLI Dashboard:** Provides a real-time, color-coded command-line interface monitoring the checking process.

---

## 🛠️ Installation

Clone the repository and install the required dependencies to get started.

```bash
# Clone the repository
git clone https://github.com/DrowBlack/Void-Scraper.git

# Navigate to the project directory
cd Void-Scraper

# Install dependencies
pip install -r requirements.txt

```

---

## 💻 Usage

Run the main script via your terminal. You will be prompted to select the target protocol.

```bash
python main.py

```

You can go to Void-Scraper > proxy-checker for check your proxies (NOT SCRAPES JUST CHECKS)

**Workflow:**

1. **Launch:** Start the application.
2. **Select Protocol:** Choose the desired proxy type from the menu:
* `[1] HTTP/HTTPS`
* `[2] SOCKS4`
* `[3] SOCKS5`


3. **Process:** The tool scrapes fresh lists and initiates the validation engine.
4. **Results:** Live feedback is displayed in the console:
> `┃ 184.181.217.206:4145 │ US      │ 929ms  ┃`


5. **Export:** Working proxies are saved to `working_proxies.txt` (or a timestamped file).

---

## 📷 CLI Preview

```text
╭──────────────────────────────────────────────── VOID SYSTEM ────────────────────────────────────────────────╮
│                                                                                                             │
│                                          ██╗   ██╗ ██████╗ ██╗██████╗                                       │
│                                          ██║   ██║██╔═══██╗██║██╔══██╗                                      │
│                                          ██║   ██║██║   ██║██║██║  ██║                                      │
│                                          ╚██╗ ██╔╝██║   ██║██║██║  ██║                                      │
│                                           ╚████╔╝ ╚██████╔╝██║██████╔╝                                      │
│                                            ╚═══╝   ╚═════╝ ╚═╝╚═════╝                                       │
│                                            U N I V E R S A L   V 5 . 0                                      │
│                                                                                                             │
╰──────────────────────────────────────── Protocol Selection Enabled ─────────────────────────────────────────╯
Select Protocol:
1. HTTP / HTTPS
2. SOCKS4
3. SOCKS5
Choose:  [1/2/3]: 2

➜ Scraping SOCKS5 sources... (7 sites)
Harvesting Sources... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ (7/7)
✔ Total 1771 candidates found for socks5.
⠼ Testing Void SOCKS5... ━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━  43%

            Working SOCKS5 List            
┏━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━┯━━━━━━━━┓
┃ Proxy Address        │ Country │ Ping   ┃
┠──────────────────────┼─────────┼────────┨
┃ 68.71.249.153:48606  │ US      │ 892ms  ┃
┃ 72.37.216.68:4145    │ US      │ 905ms  ┃
┃ 184.181.217.206:4145 │ US      │ 929ms  ┃
┃ 70.166.167.55:57745  │ US      │ 934ms  ┃
┃ 184.178.172.13:15311 │ US      │ 942ms  ┃
┃ 98.170.57.241:4145   │ US      │ 946ms  ┃
┃ 192.252.208.67:14287 │ US      │ 826ms  ┃
┗━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━┛
╭─────────────────────────────────────────╮
│ Total Working: 102                      │
│ Saved to: working_socks5.txt            │
╰─────────────────────────────────────────╯
```


---

## ⚠️ Legal Disclaimer

This software is developed for **educational purposes** and **personal network testing** only. The developer assumes no liability for any misuse of this tool. Users are responsible for adhering to the Terms of Service of the target servers and complying with applicable laws and regulations regarding network scraping and proxy usage.

---

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE). You are free to use, modify, and distribute this software, provided that the original license and copyright notice are included.

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request.
