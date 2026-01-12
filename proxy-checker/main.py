import requests
import concurrent.futures
import time
import os
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich import box

GIRIS_DOSYASI = "proxies.txt"   
CIKIS_DOSYASI = "live_proxies.txt" 
THREAD_SAYISI = 50             
TIMEOUT = 5                     
PROTOKOL = "socks5"             

console = Console()

def ekranı_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner_yazdir():
    ekranı_temizle()
    banner = """
    ██╗   ██╗ ██████╗ ██╗██████╗         
    ██║   ██║██╔═══██╗██║██╔══██╗        
    ██║   ██║██║   ██║██║██║  ██║        
    ╚██╗ ██╔╝██║   ██║██║██║  ██║        
     ╚████╔╝ ╚██████╔╝██║██████╔╝        
      ╚═══╝   ╚═════╝ ╚═╝╚═════╝         
      C H E C K E R  -  Local Mode
    """
    console.print(Panel(Text(banner, justify="center", style="bold cyan"), 
                        title="[bold magenta]VOID CHECKER[/bold magenta]", 
                        border_style="blue"))

def proxy_kontrol_et(proxy):
    proxy = proxy.strip()
    if not proxy: return None

    proxies_dict = {
        "http": f"{PROTOKOL}://{proxy}",
        "https": f"{PROTOKOL}://{proxy}"
    }
    
    url = "http://ip-api.com/json/" 
    
    start_time = time.time()
    try:
        r = requests.get(url, proxies=proxies_dict, timeout=TIMEOUT)
        if r.status_code == 200:
            ping = int((time.time() - start_time) * 1000)
            data = r.json()
            ulke = data.get("countryCode", "UNK")
            sehir = data.get("city", "Unknown")
            return {"proxy": proxy, "ping": ping, "ulke": ulke, "sehir": sehir, "status": True}
    except:
        return {"proxy": proxy, "status": False}

def main():
    banner_yazdir()
    
    if not os.path.exists(GIRIS_DOSYASI):
        console.print(f"[bold red]ERROR:[/bold red] '{GIRIS_DOSYASI}' dosyası bulunamadı!")
        console.print("[yellow]Please Create: 'proxies.txt' And add your proxies in this format: IP:PORT[/yellow]")
        return

    with open(GIRIS_DOSYASI, "r") as f:
        proxy_listesi = [line.strip() for line in f.readlines() if line.strip()]

    if not proxy_listesi:
        console.print("[bold red]ERROR:[/bold red] Proxy listeniz boş!")
        return

    console.print(f"[blue]ℹ[/blue] Total [bold white]{len(proxy_listesi)}[/bold white] Amount of proxy found. Scanning...\n")

    table = Table(title="[bold magenta]Live Proxies[/bold magenta]", box=box.ROUNDED)
    table.add_column("Proxy Adresi", style="cyan")
    table.add_column("Lokasyon", style="green")
    table.add_column("Ping", style="yellow")
    table.add_column("Durum", style="bold green")

    calisanlar = []
    
    open(CIKIS_DOSYASI, "w").close()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="blue", complete_style="magenta"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task = progress.add_task("[cyan]Testing Proxies...", total=len(proxy_listesi))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_SAYISI) as executor:
            future_to_proxy = {executor.submit(proxy_kontrol_et, p): p for p in proxy_listesi}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                result = future.result()
                
                if result and result['status'] == True:
                    calisanlar.append(result['proxy'])
                    loc_str = f"{result['ulke']} / {result['sehir']}"
                    table.add_row(result['proxy'], loc_str, f"{result['ping']}ms", "WORKING")
                    
                    with open(CIKIS_DOSYASI, "a") as f:
                        f.write(result['proxy'] + "\n")
                
                progress.advance(task)

    ekranı_temizle()
    banner_yazdir()
    console.print("\n")
    if len(calisanlar) > 0:
        console.print(table)
    else:
        console.print("[bold red]There has 0 Working Proxies.[/bold red]")
        
    console.print(Panel(
        f"Total Scanned: {len(proxy_listesi)}\n"
        f"Working: [bold green]{len(calisanlar)}[/bold green]\n"
        f"Dead: [red]{len(proxy_listesi) - len(calisanlar)}[/red]\n\n"
        f"Saved File: [bold yellow]{CIKIS_DOSYASI}[/bold yellow]",
        border_style="green"
    ))

if __name__ == "__main__":
    main()
