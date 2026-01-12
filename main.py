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

# --- AYARLAR ---
THREAD_SAYISI = 100
TIMEOUT = 5

console = Console()

# Tarayıcı Kimliği (User-Agent)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# --- KATEGORİLERE AYRILMIŞ KAYNAKLAR ---
# Buraya istediğin siteyi ekleyebilirsin. Script sitenin HTML'ini okuyup IP:PORT formatına uyan her şeyi çeker.
KAYNAKLAR = {
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
        "https://spys.one/en/socks-proxy-list/"
        "https://www.freeproxy.world/?type=socks5"
    ]
}

def ekrani_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner_yazdir():
    ekrani_temizle()
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

def protokol_secimi():
    console.print("\n[bold white]Hangi tür proxy avlayalım?[/bold white]")
    console.print("[1] [cyan]HTTP / HTTPS[/cyan]")
    console.print("[2] [cyan]SOCKS4[/cyan]")
    console.print("[3] [magenta]SOCKS5[/magenta] (Minecraft/Zenith için önerilen)\n")
    
    secim = Prompt.ask("[bold yellow]Seçiminiz[/bold yellow]", choices=["1", "2", "3"], default="3")
    
    if secim == "1": return "http"
    if secim == "2": return "socks4"
    if secim == "3": return "socks5"
    return "socks5"

def evrensel_tarayici(url):
    """HTML yapısına bakmadan Regex ile IP:PORT çeker"""
    bulunanlar = set()
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        # Regex: Sayı.Sayı.Sayı.Sayı:Port yapısını bul
        regex_deseni = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}"
        eslesmeler = re.findall(regex_deseni, r.text)
        for proxy in eslesmeler:
            bulunanlar.add(proxy)
    except:
        pass
    return bulunanlar

def proxy_kontrol_et(args):
    proxy, protokol = args
    # Protokole göre bağlantı şeması
    scheme = "http" if protokol == "http" else protokol
    
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
            ulke = data.get("countryCode", "UNK")
            return {"proxy": proxy, "ping": ping, "ulke": ulke}
    except:
        return None

def main():
    banner_yazdir()
    secilen_protokol = protokol_secimi()
    dosya_adi = f"working_{secilen_protokol}.txt"
    
    # İlgili kaynakları seç
    hedef_siteler = KAYNAKLAR[secilen_protokol]
    
    console.print(f"\n[bold green]➜[/bold green] [bold white]{secilen_protokol.upper()}[/bold white] kaynakları taranıyor... ({len(hedef_siteler)} site)\n")

    tum_proxyler = set()
    
    # 1. Regex Tarama
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="green", complete_style="magenta"),
        TextColumn("({task.completed}/{task.total})"),
    ) as progress:
        task = progress.add_task("[cyan]Kaynaklar Sömürülüyor...", total=len(hedef_siteler))
        
        for url in hedef_siteler:
            site_proxyleri = evrensel_tarayici(url)
            tum_proxyler.update(site_proxyleri)
            progress.advance(task)
    
    console.print(f"\n[green]✔[/green] Toplam [bold white]{len(tum_proxyler)}[/bold white] adet {secilen_protokol} adayı bulundu.\n")

    # 2. Kontrol (Checker)
    table = Table(title=f"[bold magenta]Çalışan {secilen_protokol.upper()} Listesi[/bold magenta]", box=box.HEAVY_EDGE)
    table.add_column("Proxy Adresi", style="cyan")
    table.add_column("Ülke", style="green")
    table.add_column("Ping", style="yellow")
    
    # Dosyayı sıfırla
    with open(dosya_adi, "w") as f: f.write("")
    calisanlar = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="purple", complete_style="cyan"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task = progress.add_task(f"[cyan]Void {secilen_protokol.upper()} Test Ediliyor...", total=len(tum_proxyler))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_SAYISI) as executor:
            # Argümanları paketle
            args_list = [(p, secilen_protokol) for p in tum_proxyler]
            future_to_proxy = {executor.submit(proxy_kontrol_et, arg): arg for arg in args_list}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                result = future.result()
                if result:
                    calisanlar.append(result['proxy'])
                    if len(calisanlar) <= 20:
                        table.add_row(result['proxy'], result['ulke'], f"{result['ping']}ms")
                    
                    with open(dosya_adi, "a") as f:
                        f.write(result['proxy'] + "\n")
                
                progress.advance(task)

    console.print("\n")
    if calisanlar:
        console.print(table)
    console.print(Panel(f"Toplam Çalışan: [bold green]{len(calisanlar)}[/bold green]\nKayıt Yeri: [bold yellow]{dosya_adi}[/bold yellow]", border_style="green"))

if __name__ == "__main__":
    main()