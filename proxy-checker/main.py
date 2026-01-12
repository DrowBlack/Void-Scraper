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

# --- AYARLAR ---
GIRIS_DOSYASI = "proxies.txt"   # Proxylerini buraya yapıştır
CIKIS_DOSYASI = "live_proxies.txt" # Çalışanlar buraya kaydolur
THREAD_SAYISI = 50              # Aynı anda kaç kontrol yapılsın
TIMEOUT = 5                     # Kaç saniye beklensin
PROTOKOL = "socks5"             # 'socks5' (Minecraft için) veya 'http'

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
    # Proxy formatını temizle (boşluklar vs.)
    proxy = proxy.strip()
    if not proxy: return None

    # Zenith Proxy için SOCKS5 öncelikli
    proxies_dict = {
        "http": f"{PROTOKOL}://{proxy}",
        "https": f"{PROTOKOL}://{proxy}"
    }
    
    url = "http://ip-api.com/json/" # Test edilecek adres
    
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
    
    # Dosya Kontrolü
    if not os.path.exists(GIRIS_DOSYASI):
        console.print(f"[bold red]HATA:[/bold red] '{GIRIS_DOSYASI}' dosyası bulunamadı!")
        console.print("[yellow]Lütfen aynı klasöre 'proxies.txt' oluşturup içine IP:PORT listesini yapıştırın.[/yellow]")
        return

    # Dosyayı Oku
    with open(GIRIS_DOSYASI, "r") as f:
        proxy_listesi = [line.strip() for line in f.readlines() if line.strip()]

    if not proxy_listesi:
        console.print("[bold red]HATA:[/bold red] Proxy listeniz boş!")
        return

    console.print(f"[blue]ℹ[/blue] Toplam [bold white]{len(proxy_listesi)}[/bold white] adet proxy yüklendi. Tarama başlıyor...\n")

    # Tablo Oluştur
    table = Table(title="[bold magenta]Canlı Proxy Sonuçları[/bold magenta]", box=box.ROUNDED)
    table.add_column("Proxy Adresi", style="cyan")
    table.add_column("Lokasyon", style="green")
    table.add_column("Ping", style="yellow")
    table.add_column("Durum", style="bold green")

    calisanlar = []
    
    # Çıktı dosyasını sıfırla
    open(CIKIS_DOSYASI, "w").close()

    # Taramayı Başlat
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="blue", complete_style="magenta"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task = progress.add_task("[cyan]Bağlantılar Test Ediliyor...", total=len(proxy_listesi))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_SAYISI) as executor:
            future_to_proxy = {executor.submit(proxy_kontrol_et, p): p for p in proxy_listesi}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                result = future.result()
                
                if result and result['status'] == True:
                    # Çalışıyorsa
                    calisanlar.append(result['proxy'])
                    loc_str = f"{result['ulke']} / {result['sehir']}"
                    table.add_row(result['proxy'], loc_str, f"{result['ping']}ms", "WORKING")
                    
                    # Dosyaya yaz
                    with open(CIKIS_DOSYASI, "a") as f:
                        f.write(result['proxy'] + "\n")
                
                progress.advance(task)

    # Sonuçları Göster
    ekranı_temizle()
    banner_yazdir()
    console.print("\n")
    if len(calisanlar) > 0:
        console.print(table)
    else:
        console.print("[bold red]Maalesef hiç çalışan proxy bulunamadı.[/bold red]")
        
    console.print(Panel(
        f"Toplam Taranan: {len(proxy_listesi)}\n"
        f"Çalışan: [bold green]{len(calisanlar)}[/bold green]\n"
        f"Ölü: [red]{len(proxy_listesi) - len(calisanlar)}[/red]\n\n"
        f"Kayıt Dosyası: [bold yellow]{CIKIS_DOSYASI}[/bold yellow]",
        border_style="green"
    ))

if __name__ == "__main__":
    main()