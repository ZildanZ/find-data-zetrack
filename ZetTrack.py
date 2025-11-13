#OpenSource tapi plis SUBSCRIBE: ZildanSecurity
#Kalau bisa share bang
import requests
from bs4 import BeautifulSoup
import urllib.parse
from getpass import getpass
import os
from tqdm import tqdm
from googlesearch import search 
import re
import shutil

os.system('cls')


def get_redirected_url(url, proxy=None):
    try:
        proxies = {
            'http': proxy,
            'https': proxy
        } if proxy else None
        
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        return response.url
    except requests.exceptions.RequestException:
        return "loading"


def clean_url(url):
    url = urllib.parse.unquote(url)
    url = url.split('&sa=U&')[0]
    url = url.split('&usg=')[0]
    url = url.split('?_rdc=1&_rdr')[0]
    return url


def get_google_search_results(query, proxy=None):
    try:
        proxies = {
            'http': proxy,
            'https': proxy
        } if proxy else None

        response = requests.get(query, proxies=proxies, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('a')
    except requests.exceptions.RequestException:
        return []


def print_social_media_links(platform, links, nama_input):
    if not links:
        return
    print(f"\n🔗 Akun {platform} untuk nama '{nama_input}':")
    for link in links:
        print(f"  • {link}")

def search_social_media_accounts(nama_input, key, proxy=None):
    if key != '1337':
        print("🔒 Kunci tidak valid. Akses ditolak.")
        print("Untuk mendapatkan kunci, silakan bergabung dengan grup Forum Jawa Barat Cyber di https://link.rso.go.id/Forum-JawaBaratCyber")
        return

    platforms = {
        'Facebook': 'site:facebook.com',
        'Twitter': 'site:twitter.com',
        'TikTok': 'site:tiktok.com',
        'Instagram': 'site:instagram.com'
    }

    for platform, search_query in platforms.items():
        query = f'intext:"{nama_input}" {search_query}'
        url = f'https://www.google.com/search?q={urllib.parse.quote(query)}'
        search_results = get_google_search_results(url, proxy)
        social_media_links = []

        for link in search_results:
            href = link.get('href')
            if not href:
                continue
            if href.startswith('/url?q='):
                url2 = href[7:]
                url2 = clean_url(url2)
                if 'google.com' not in url2:
                    url2 = get_redirected_url(url2, proxy)
                    if url2 != "loading":
                        social_media_links.append(url2)

        print_social_media_links(platform, social_media_links, nama_input)


def cek_file(file_path):
    return os.path.exists(file_path)


def parse_hasil_baris(baris):
    """
 
    """
    b = baris.strip()
    if b.lower().startswith("data ditemukan"):
        parts = b.split(':', 1)
        if len(parts) == 2:
            b = parts[1].strip()

    # regex yang berusaha tangkap pola umum
    pattern = re.compile(
        r'^\s*(?P<id>\d{1,})\s+'                                 # id (beberapa digit)
        r'(?P<nik>\d{12,20})\s+'                                 # nik (12-20 digit)
        r'(?P<nama>[A-Z0-9\.\-\'\s]+?)\s+'                       # nama (caps / angka / spasi), non-greedy
        r'(?P<jk>Laki-laki|Perempuan|Laki-laki/Perempuan)\s+'    # jk
        r'(?P<tgl>\d{1,2}\s+[A-Za-z]{3,}\s+\d{4})'               # tanggal lahir e.g. 20 Feb 2004
        r'(?:\s*\((?P<umur>[^)]+)\))?\s+'                        # optional umur dalam ()
        r'(?P<telf>\+?\d{6,20})\s+'                              # telepon (6-20 digit)
        r'(?P<alamat>.+)$', re.IGNORECASE
    )

    m = pattern.search(b)
    if m:
        return {
            'id': m.group('id').strip(),
            'nik': m.group('nik').strip(),
            'nama': ' '.join(m.group('nama').split()),
            'jk': m.group('jk').strip(),
            'tanggal_lahir': m.group('tgl').strip(),
            'umur': (m.group('umur') or '').strip(),
            'telepon': m.group('telf').strip(),
            'alamat': ' '.join(m.group('alamat').split())
        }
    else:
        return None


def cari_data_python(kata_kunci, daftar_file):
    hasil = []

    for nama_file in daftar_file:
        if not cek_file(nama_file):
            print(f"❌ Database tidak ditemukan:")
            continue

        print(f"\nLoading...... ")

        try:
            with open(nama_file, 'r', encoding='utf-8', errors='ignore') as f:
                total_baris = sum(1 for _ in f)

            with open(nama_file, 'r', encoding='utf-8', errors='ignore') as file:
                for nomor_baris, baris in enumerate(tqdm(file, total=total_baris,
                                                         desc=f"⏳Progress....",
                                                         unit="bar", ncols=100)):
                    if kata_kunci.lower() in baris.lower():
                        parsed = parse_hasil_baris(baris.strip())
                        if parsed:
                            hasil.append(parsed)
                        else:
                  
                            hasil.append({'raw': baris.strip()})

        except Exception as e:
            print(f"⚠️ Terjadi kesalahan saat membaca: {e}")

    return hasil


def google_dorking(kata_kunci):
    print(f"\n🌐 Melakukan Osint {kata_kunci}")

    target_sites = [
        "linkedin.com", "tiktok.com", "instagram.com", "twitter.com",
        "facebook.com", "pastebin.com", "github.com"
    ]

    semua_link = []

    for site in target_sites:
        query = f'"{kata_kunci}" {site}'
        print(f"\n🔍 :{query}")
        try:
            hasil = search(query, num=5)  # ✅ pakai num
            for link in hasil:
                print(f"🔗 {link}")
                semua_link.append(link)
        except Exception as e:
            print(f"⚠️ Gagal mengambil hasil untuk {site}: {e}")

    return semua_link


def get_proxy():
    proxy_list = [
        'http://185.104.231.20:8080', 
        'http://200.94.9.2:8080',
        'http://134.209.49.125:8080'
    ]
    return proxy_list[0]  


def tampilkan_hasil_blok(hasil_list):
    if not hasil_list:
        print("❌ Tidak ditemukan data yang cocok.")
        return

    print("\n🔍 Hasil pencarian ditemukan:\n")
    for idx, entry in enumerate(hasil_list, 1):
        print(f"==================== Data #{idx} ====================")
        if 'raw' in entry:
            # Jika raw, tampilkan saja sebagai ALAMAT RAW
            print(f"🆔 ID: (tidak terdeteksi)")
            print(f"🔢 NIK: (tidak terdeteksi)")
            print(f"🧾 Nama: (tidak terdeteksi)")
            print(f"⚧ Jenis Kelamin: (tidak terdeteksi)")
            print(f"🎂 Tanggal Lahir: (tidak terdeteksi)")
            print(f"⏳ Umur: (tidak terdeteksi)")
            print(f"📞 Telepon: (tidak terdeteksi)")
            print(f"📍 Alamat (raw): {entry['raw']}")
        else:
            # Tampilkan field yang ada, jika kosong tampilkan '-'
            id_val = entry.get('id') or '-'
            nik_val = entry.get('nik') or '-'
            nama_val = entry.get('nama') or '-'
            jk_val = entry.get('jk') or '-'
            tgl_val = entry.get('tanggal_lahir') or '-'
            umur_val = entry.get('umur') or '-'
            tel_val = entry.get('telepon') or '-'
            alamat_val = entry.get('alamat') or '-'


            if 'laki' in jk_val.lower():
                jk_emoji = "👨"
            elif 'perempuan' in jk_val.lower():
                jk_emoji = "👩"
            else:
                jk_emoji = "⚧"

            print(f"🆔 ID: {id_val}")
            print(f"🔢 NIK: {nik_val}")
            print(f"🧑‍💼 Nama: {nama_val}")
            print(f"{jk_emoji} Jenis Kelamin: {jk_val}")
            print(f"🎂 Tanggal Lahir: {tgl_val}")
            print(f"⏳ Umur: {umur_val}")
            print(f"📞 Telepon: {tel_val}")
            print(f"📍 Alamat: {alamat_val}")
        print("====================================================\n")


print("\033[36m")
print(r"""
▒███████▒▓█████▄▄▄█████▓▄▄▄█████▓ ██▀███   ▄▄▄       ▄████▄   ██ ▄█▀
▒ ▒ ▒ ▄▀░▓█   ▀▓  ██▒ ▓▒▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ 
░ ▒ ▄▀▒░ ▒███  ▒ ▓██░ ▒░▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ 
  ▄▀▒   ░▒▓█  ▄░ ▓██▓ ░ ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ 
▒███████▒░▒████▒ ▒██▒ ░   ▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄
░▒▒ ▓░▒░▒░░ ▒░ ░ ▒ ░░     ▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒
░░▒ ▒ ░ ░ ░  ░   ░        ░      ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░
░ ░ ░ ░ ░   ░    ░        ░        ░░   ░   ░   ▒   ░        ░ ░░ ░ 
  ░ ░       ░  ░                    ░           ░  ░░ ░      ░  ░   
░                                                   ░                                
                   Subcribe: @ZildanSecurity
""")
print("\033[0m")

kata_kunci = input("Masukkan kata kunci: ")
daftar_file = [
    r'data.txt',
    r'data2.txt',
    r'data3.txt',
    r'data4'
]


hasil_pencarian = cari_data_python(kata_kunci, daftar_file)

print("\n🔍 Hasil pencarian:")
tampilkan_hasil_blok(hasil_pencarian)


print("\n📡 Melanjutkan dengan pencarian akun sosial media otomatis...")
proxy = get_proxy()
search_social_media_accounts(kata_kunci, 'tanya_atmin', proxy)
link_dari_dork = google_dorking(kata_kunci)


if link_dari_dork:
    with open("hasil_dork.txt", "w", encoding="utf-8") as f:
        for link in link_dari_dork:
            f.write(link + "\n")
    print("\n📁 Hasil Osint disimpan di file hasil_dork.txt")
else:
    print("\n⚠️ Tidak ada hasil Dork yang ditemukan.")
