import requests
import concurrent.futures
import time
import os
import re
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich import box

MAX_THREADS = 100
TIMEOUT = 5

console = Console()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

SOURCES = {
    "http": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://www.freeproxy.world/?type=http&anonymity=&country=&speed=&port=&page=1",
        "https://www.sslproxies.org/"
    ],
    "socks4": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://www.freeproxy.world/?type=socks4&anonymity=&country=&speed=&port=&page=1",
        "https://www.socks-proxy.net/"
    ],
    "socks5": [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://www.freeproxy.world/?type=socks5&anonymity=&country=&speed=&port=&page=1",
        "https://spys.one/en/socks-proxy-list/",
        "https://www.freeproxy.world/?type=socks5"
    ]
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = """
   ██╗   ██╗ ██████╗ ██╗██████╗         
    ██║   ██║██╔═══██╗██║██╔══██╗        
    ██║   ██║██║   ██║██║██║  ██║        
    ╚██╗ ██╔╝██║   ██║██║██║  ██║        
     ╚████╔╝ ╚██████╔╝██║██████╔╝        
      ╚═══╝   ╚═════╝ ╚═╝╚═════╝         
      U N I V E R S A L   V 5 . 0
    """
    console.print(Panel(Text(banner, justify="center", style="bold green"), 
                        title="[bold magenta]VOID SYSTEM[/bold magenta]", 
                        subtitle="[italic]Protocol Selection Enabled[/italic]",
                        border_style="green"))

def select_protocol():
    console.print("\n[bold white]Select Proxy Type[/bold white]")
    console.print("[1] [cyan]HTTP / HTTPS[/cyan]")
    console.print("[2] [cyan]SOCKS4[/cyan]")
    console.print("[3] [magenta]SOCKS5[/magenta] (Recommended)\n")
    
    choice = Prompt.ask("[bold yellow]Choice[/bold yellow]", choices=["1", "2", "3"], default="3")
    
    if choice == "1": return "http"
    if choice == "2": return "socks4"
    if choice == "3": return "socks5"
    return "socks5"

def scrape_proxies(url):
    found_proxies = set()
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        regex_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}"
        matches = re.findall(regex_pattern, r.text)
        for proxy in matches:
            found_proxies.add(proxy)
    except:
        pass
    return found_proxies

def check_proxy(args):
    proxy, protocol = args
    scheme = "http" if protocol == "http" else protocol
    
    proxies_dict = {
        "http": f"{scheme}://{proxy}",
        "https": f"{scheme}://{proxy}"
    }
    
    url = "http://ip-api.com/json/"
    start_time = time.time()
    
    try:
        r = requests.get(url, proxies=proxies_dict, timeout=TIMEOUT)
        if r.status_code == 200:
            ping = int((time.time() - start_time) * 1000)
            data = r.json()
            country = data.get("countryCode", "UNK")
            return {"proxy": proxy, "ping": ping, "country": country}
    except:
        return None

def main():
    print_banner()
    selected_protocol = select_protocol()
    filename = f"working_{selected_protocol}.txt"
    
    target_sites = SOURCES[selected_protocol]
    
    console.print(f"\n[bold green]➜[/bold green] Scraping [bold white]{selected_protocol.upper()}[/bold white] sources... ({len(target_sites)} sites)\n")

    all_proxies = set()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="green", complete_style="magenta"),
        TextColumn("({task.completed}/{task.total})"),
    ) as progress:
        task = progress.add_task("[cyan]Harvesting Sources...", total=len(target_sites))
        
        for url in target_sites:
            site_proxies = scrape_proxies(url)
            all_proxies.update(site_proxies)
            progress.advance(task)
    
    console.print(f"\n[green]✔[/green] Total [bold white]{len(all_proxies)}[/bold white] candidates found for {selected_protocol}.\n")

    table = Table(title=f"[bold magenta]Working {selected_protocol.upper()} List[/bold magenta]", box=box.HEAVY_EDGE)
    table.add_column("Proxy Address", style="cyan")
    table.add_column("Country", style="green")
    table.add_column("Ping", style="yellow")
    
    with open(filename, "w") as f: f.write("")
    working_proxies = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="purple", complete_style="cyan"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task = progress.add_task(f"[cyan]Testing Void {selected_protocol.upper()}...", total=len(all_proxies))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            args_list = [(p, selected_protocol) for p in all_proxies]
            future_to_proxy = {executor.submit(check_proxy, arg): arg for arg in args_list}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                result = future.result()
                if result:
                    working_proxies.append(result['proxy'])
                    if len(working_proxies) <= 20:
                        table.add_row(result['proxy'], result['country'], f"{result['ping']}ms")
                    
                    with open(filename, "a") as f:
                        f.write(result['proxy'] + "\n")
                
                progress.advance(task)

    console.print("\n")
    if working_proxies:
        console.print(table)
    console.print(Panel(f"Total Working: [bold green]{len(working_proxies)}[/bold green]\nSaved to: [bold yellow]{filename}[/bold yellow]", border_style="green"))

if __name__ == "__main__":
    main()