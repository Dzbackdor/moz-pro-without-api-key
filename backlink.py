
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import re
import urllib.parse
from colorama import Fore, init
# Initialize Colorama
init(autoreset=True)

# Colors for terminal text
B = Fore.BLUE
W = Fore.WHITE
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW


def validate_domain(domain):
    """
    Validasi format domain
    
    Args:
        domain (str): Domain untuk divalidasi
        
    Returns:
        str: Domain yang dibersihkan atau None jika tidak valid
    """
    if not domain:
        return None
    
    # Hapus protokol jika ada
    domain = re.sub(r'^https?://', '', domain)
    
    # Hapus www jika ada
    domain = re.sub(r'^www\.', '', domain)
    
    # Hapus trailing slash
    domain = domain.rstrip('/')
    
    # Validasi domain dasar
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*'
    
    if re.match(domain_pattern, domain):
        return domain
    else:
        return None

def get_domain_input(headless=False):
    """Dapatkan input domain dari pengguna dengan validasi"""
    if headless:
        print(f"\n🔇 {W}MODE HEADLESS - Input Domain")
        print(f"{Y}─" * 50)
        
        try:
            domain = input(f"🌐 {W}Masukkan domain: {Y}").strip()
            
            if not domain:
                print(f"❌ {R}Domain tidak boleh kosong!")
                return None
            
            # Validasi domain
            cleaned_domain = validate_domain(domain)
            
            if cleaned_domain:
                print(f"✅ {W}Domain divalidasi: {Y}{cleaned_domain}")
                return cleaned_domain
            else:
                print(f"❌ {R}Format domain tidak valid!")
                return None
                
        except Exception as e:
            print(f"⚠️ {R}Error input domain: {str(e)}")
            return None
    else:
        print(f"\n🔗 {W}INPUT DOMAIN UNTUK ANALISIS BACKLINK")
        print(f"{Y}─" * 50)
        
        while True:
            try:
                print(f"💡 {W}Masukkan domain yang ingin Anda analisis untuk backlink")
                print(f"📝 {W}Contoh: {Y}example.com, {Y}www.example.com,{Y}https://example.com")
                print(f"{Y}─" * 50)
                
                domain = input(f"🌐 {W}Masukkan domain:{Y} ").strip()
                
                if not domain:
                    print(f"❌ {R}Domain tidak boleh kosong!")
                    continue
                
                # Validasi domain
                cleaned_domain = validate_domain(domain)
                
                if cleaned_domain:
                    print(f"✅ {W}Domain divalidasi: {Y}{cleaned_domain}")
                    return cleaned_domain
                else:
                    print(f"❌ {R}Format domain tidak valid!")
                    print(f"💡 {R}Silakan masukkan domain yang valid (contoh: {Y}example.com{R})")
                    
                    retry = input(f"🔄 {W}Coba lagi? (y/n):{R} ").strip().lower()
                    if retry not in ['y', 'yes', '1', 'true', 'ya']:
                        return None
                        
            except KeyboardInterrupt:
                print(f"\n⚠️ {W}Proses dihentikan oleh pengguna")
                return None
            except Exception as e:
                print(f"❌ {R}Error mendapatkan input domain: {str(e)}")
                return None

def check_and_display_quota(driver):
    """
    Cek dan tampilkan informasi quota dari halaman Moz
    
    Args:
        driver: Instance Selenium WebDriver
    """
    try:
        # Cari elemen quota dengan berbagai selector
        quota_selectors = [
            "p.links-quota",
            ".links-quota", 
            "[class*='quota']",
            "[class*='queries']"
        ]
        
        for selector in quota_selectors:
            try:
                quota_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for quota_element in quota_elements:
                    if quota_element.is_displayed() and quota_element.text.strip():
                        quota_text = quota_element.text.strip()
                        print(f"📊 Quota: {quota_text}")
                        return quota_text
            except:
                continue
        
        print("ℹ️ Informasi quota tidak ditemukan")
        return None
        
    except Exception as e:
        print(f"⚠️ Error mengecek quota: {str(e)}")
        return None

def search_backlinks_direct_url(driver, domain, headless=False, timeout=30):
    """
    Metode GET langsung ke URL hasil pencarian (untuk mode headless)
    
    Args:
        driver: Instance Selenium WebDriver
        domain (str): Domain untuk dicari
        headless (bool): Mode headless
        timeout (int): Waktu tunggu maksimum dalam detik
        
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        print(f"🔗 Menggunakan metode GET langsung untuk: {domain}")
        print("🔇 Mode headless: Navigasi langsung ke URL hasil")
        print(f"{G}═" * 50)
        
        # Encode domain untuk URL
        encoded_domain = urllib.parse.quote(domain)
        
        # Konstruksi URL langsung ke hasil pencarian
        direct_url = f"https://analytics.moz.com/pro/link-explorer/linking-domains?site={encoded_domain}&state=all&target=domain&type=all"
        
        print(f"🌐 {W}Navigasi ke:{Y} {direct_url}")
        
        # Navigasi langsung ke URL
        driver.get(direct_url)
        
        # Tunggu halaman dimuat
        print("⏳ Menunggu halaman dimuat...")
        time.sleep(10)  # Tunggu lebih lama untuk memastikan data dimuat
        
        # Cek dan tampilkan quota
        check_and_display_quota(driver)
        
        # Periksa apakah halaman berhasil dimuat
        current_url = driver.current_url
        print(f"📍 URL saat ini: {current_url}")
        
        # Verifikasi bahwa kita berada di halaman yang benar
        if "link-explorer" in current_url and domain in current_url:
            print("✅ Berhasil navigasi ke halaman hasil backlink")
            return True
        elif "link-explorer" in current_url:
            print("✅ Berada di Link Explorer, mencoba memuat data...")
            # Tunggu lebih lama untuk data dimuat
            time.sleep(15)
            return True
        else:
            print("⚠️ URL tidak sesuai yang diharapkan")
            return False
            
    except Exception as e:
        print(f"❌ Error navigasi langsung: {str(e)}")
        return False

def search_backlinks_interactive(driver, domain, timeout=30):
    """
    Metode pencarian interaktif (untuk mode GUI)
    
    Args:
        driver: Instance Selenium WebDriver
        domain (str): Domain untuk dicari
        timeout (int): Waktu tunggu maksimum dalam detik
        
    Returns:
        bool: True jika pencarian berhasil, False jika gagal
    """
    try:
        print(f"🔗 Memulai pencarian interaktif untuk: {domain}")
        print(f"{G}═" * 50)
        
        # Navigasi ke Link Explorer
        print("🌐 Navigasi ke Moz Link Explorer...")
        driver.get("https://analytics.moz.com/pro/link-explorer/linking-domains")
        
        # Tunggu halaman dimuat
        wait = WebDriverWait(driver, timeout)
        time.sleep(5)
        
        # Cek dan tampilkan quota
        check_and_display_quota(driver)
        
        # Tunggu field input pencarian tertentu
        print("🔍 Mencari field input pencarian...")
        
        # Target utama: input[name="forms.links.search.search"]
        search_field = None
        
        try:
            print("🎯 Mencari target utama: input[name='forms.links.search.search']")
            search_field = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="forms.links.search.search"]'))
            )
            print("✅ Menemukan field pencarian utama!")
            
            # Tunggu elemen dapat diklik
            search_field = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="forms.links.search.search"]'))
            )
            print("✅ Field pencarian dapat diklik!")
            
        except TimeoutException:
            print("⚠️ Target utama tidak ditemukan, mencoba selector alternatif...")
            
            # Selector alternatif jika utama tidak ditemukan
            alternative_selectors = [
                'input[placeholder*="domain"]',
                'input[placeholder*="URL"]',
                'input[placeholder*="Enter"]',
                '.search-input',
                '[data-testid="search-input"]',
                'input[type="search"]',
                'input[type="text"]'
            ]
            
            for selector in alternative_selectors:
                try:
                    print(f"🔍 Mencoba selector alternatif: {selector}")
                    search_field = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Menemukan field pencarian dengan selector: {selector}")
                    break
                except TimeoutException:
                    continue
        
        if not search_field:
            print("❌ Tidak dapat menemukan field input pencarian!")
            return False
        
        # Fokus dan input domain
        print("👆 Memfokuskan field pencarian...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_field)
        time.sleep(2)
        
        search_field.click()
        time.sleep(1)
        
        # Bersihkan dan masukkan domain
        print(f"📝 Memasukkan domain: {domain}")
        search_field.clear()
        time.sleep(1)
        search_field.send_keys(domain)
        time.sleep(2)
        
        # Submit pencarian
        print("🔍 Submit pencarian...")
        search_field.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Cek quota lagi setelah pencarian
        check_and_display_quota(driver)
        
        return True
        
    except Exception as e:
        print(f"❌ Error pencarian interaktif: {str(e)}")
        return False

def search_backlinks(driver, domain, headless=False, timeout=30):
    """
    Cari backlinks domain di Moz Link Explorer
    """
    try:
        if headless:
            print(f"🔗 Memulai pencarian backlink untuk: {domain} (Mode Headless)")
        else:
            print(f"🔗 Memulai pencarian backlink untuk: {domain}")
        print(f"{G}═" * 50)
        
        # Navigasi ke Link Explorer dengan timeout yang lebih pendek untuk headless
        if headless:
            print("🌐 Navigasi langsung ke hasil...")
            # Gunakan URL langsung untuk mode headless
            encoded_domain = domain.replace('.', '%2E')
            direct_url = f"https://analytics.moz.com/pro/link-explorer/linking-domains?site={encoded_domain}&state=all&target=domain&type=all"
            driver.get(direct_url)
            print("✅ Navigasi selesai")
        else:
            print("🌐 Navigasi ke Moz Link Explorer...")
            driver.get("https://analytics.moz.com/pro/link-explorer/linking-domains")
        
        # Tunggu halaman dimuat dengan timeout yang disesuaikan
        if headless:
            wait_timeout = 15  # Timeout lebih pendek untuk headless
            print("⏳ Menunggu halaman dimuat (15 detik)...")
        else:
            wait_timeout = timeout
            print("⏳ Menunggu halaman dimuat...")
        
        wait = WebDriverWait(driver, wait_timeout)
        
        # Jika headless, langsung return True karena sudah menggunakan URL langsung
        if headless:
            try:
                # Tunggu sebentar untuk memastikan halaman dimuat
                time.sleep(5)
                current_url = driver.current_url
                print(f"📍{W}URL saat ini: {Y}{current_url}")
                
                # Cek apakah halaman berhasil dimuat
                if "link-explorer" in current_url:
                    print("✅ Halaman Link Explorer berhasil dimuat")
                    return True
                else:
                    print("⚠️ URL tidak sesuai, tapi melanjutkan...")
                    return True
                    
            except Exception as e:
                print(f"⚠️ Error saat cek halaman: {str(e)}")
                return True  # Tetap lanjutkan meskipun ada error
        
        # Untuk mode GUI, lakukan pencarian manual
        return search_backlinks_interactive(driver, domain, timeout)
        
    except Exception as e:
        print(f"❌ Error dalam pencarian backlink: {str(e)}")
        return False


def analyze_results(driver, headless=False):
    """Analisis dan tampilkan hasil backlink dengan metode yang lebih robust"""
    try:
        if headless:
            print(f"\n{G}" + "═" * 50)
            print(f"📊 {Y}MENGANALISIS HASIL BACKLINK")
            print(f"{G}═" * 50)
        else:
            print(f"\n{G}" + "═" * 50)
            print(f"📊 {Y}MENGANALISIS HASIL BACKLINK")
            print(f"{G}═" * 50)
        
        # Tunggu sebentar untuk memastikan halaman dimuat
        print(f"⏳ {W}Menunggu data dimuat...")
        time.sleep(8)
        
        # Cek apakah ada loading indicator dan tunggu sampai selesai
        loading_selectors = [
            '.loading',
            '.spinner',
            '[class*="loading"]',
            '[class*="spinner"]',
            '.loader'
        ]
        
        for selector in loading_selectors:
            try:
                loading_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if loading_elements:
                    for element in loading_elements:
                        if element.is_displayed():
                            print("⏳ Mendeteksi loading, menunggu selesai...")
                            # Tunggu sampai loading hilang
                            WebDriverWait(driver, 30).until_not(
                                EC.visibility_of(element)
                            )
                            print("✅ Loading selesai")
                            break
            except:
                continue
        
        # Tunggu tambahan setelah loading selesai
        time.sleep(5)
        
        # Analisis konten halaman
        page_source = driver.page_source
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        print("🔍 Menganalisis konten halaman...")
        
        # Cek apakah ada data backlink
        backlink_indicators = [
            "linking domains",
            "backlinks",
            "domain authority",
            "page authority",
            "spam score",
            "root domains",
            "total links"
        ]
        
        found_indicators = []
        for indicator in backlink_indicators:
            if indicator in page_text:
                found_indicators.append(indicator)
        
        if found_indicators:
            print(f"✅ Ditemukan indikator backlink: {', '.join(found_indicators)}")
        else:
            print("⚠️ Tidak ditemukan indikator backlink yang jelas")
        
        # Coba ekstrak metrik spesifik
        metrics_found = False
        
        # Cari Domain Authority
        da_patterns = [
            r'domain authority[:\s]*(\d+)',
            r'da[:\s]*(\d+)',
            r'authority[:\s]*(\d+)'
        ]
        
        for pattern in da_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                print(f"📊 {W}Domain Authority: {G}{matches[0]}")
                metrics_found = True
                break
        
        # Cari jumlah linking domains
        linking_patterns = [
            r'linking domains[:\s]*(\d+)',
            r'root domains[:\s]*(\d+)',
            r'(\d+)\s*linking domains',
            r'(\d+)\s*domains'
        ]
        
        for pattern in linking_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                print(f"🔗 {W}Linking Domains:{G} {matches[0]}")
                metrics_found = True
                break
        
        # Cari total backlinks
        backlink_patterns = [
            r'total (?:back)?links[:\s]*(\d+)',
            r'(\d+)\s*(?:back)?links',
            r'backlinks[:\s]*(\d+)',
            r'links[:\s]*(\d+)'
        ]
        
        for pattern in backlink_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                # Ambil angka terbesar (biasanya total backlinks)
                max_links = max([int(m) for m in matches])
                if max_links > 0:
                    print(f"🔗 Total Backlinks: {max_links}")
                    metrics_found = True
                    break
        
        # Cari tabel data
        print("🔍 Mencari tabel data...")
        table_selectors = [
            'table',
            '.table',
            '[role="table"]',
            '.data-table',
            '.results-table',
            'tbody'
        ]
        
        table_found = False
        total_rows = 0
        
        for selector in table_selectors:
            try:
                tables = driver.find_elements(By.CSS_SELECTOR, selector)
                for table in tables:
                    if table.is_displayed():
                        rows = table.find_elements(By.TAG_NAME, "tr")
                        if len(rows) > 1:  # Lebih dari header
                            total_rows = len(rows) - 1
                            print(f"📊 Ditemukan tabel dengan {G}{total_rows} baris data")
                            table_found = True
                            break
                if table_found:
                    break
            except:
                continue
        
        # Cari list items jika tidak ada tabel
        if not table_found:
            print("🔍 Mencari list items...")
            list_selectors = [
                '.result-item',
                '.link-item',
                '.domain-item',
                '[class*="result"]',
                '[class*="item"]'
            ]
            
            for selector in list_selectors:
                try:
                    items = driver.find_elements(By.CSS_SELECTOR, selector)
                    visible_items = [item for item in items if item.is_displayed()]
                    if len(visible_items) > 0:
                        print(f"📊 {W}Ditemukan {G}{len(visible_items)} item {W}hasil")
                        table_found = True
                        break
                except:
                    continue
        
        # Analisis URL untuk memastikan kita di halaman yang benar
        current_url = driver.current_url
        if "link-explorer" in current_url:
            print("✅ Berada di halaman Link Explorer")
            if "linking-domains" in current_url:
                print("✅ Berada di halaman Linking Domains")
        
        # Cek apakah ada pesan error atau no data
        error_indicators = [
            "no data",
            "no results",
            "tidak ada data",
            "tidak ditemukan",
            "error",
            "failed",
            "gagal"
        ]
        
        has_error = False
        for indicator in error_indicators:
            if indicator in page_text:
                print(f"⚠️ Ditemukan indikator error: {indicator}")
                has_error = True
                break
        
        # Ringkasan analisis
        print(f"\n📋 {W}RINGKASAN ANALISIS:")
        print(f"{Y}─" * 40)
        
        if metrics_found:
            print(f"{W}✅ Metrik backlink ditemukan")
        else:
            print(f"{R}⚠️ Metrik backlink tidak ditemukan")
        
        if table_found:
            print(f"{W}✅ Data tabel/list ditemukan")
        else:
            print(f"{R}⚠️ Data tabel/list tidak ditemukan")
        
        if has_error:
            print(f"{R}❌ Ditemukan indikator error")
        else:
            print(f"{W}✅ Tidak ada indikator error")
        
        print(f"{W}✅ Analisis selesai!")
        
        # Return status berdasarkan temuan
        return metrics_found or table_found or len(found_indicators) > 0
        
    except Exception as e:
        print(f"⚠️ Error menganalisis hasil: {str(e)}")
        return False


def wait_for_data_load(driver, timeout=30):
    """Tunggu data dimuat dengan debug yang disesuaikan untuk headless"""
    try:
        # Deteksi mode untuk output yang sesuai
        is_headless = detect_headless_mode_simple(driver)
        
        if is_headless:
            print(f"⏳ {W}Menunggu data dimuat (mode headless)...")
        else:
            print(f"🔧 {W}Debug: Menunggu data dimuat (timeout: {Y}{timeout}s{W})...")
        
        # Tunggu loading selesai
        time.sleep(5)
        
        # Cek loading indicators
        loading_selectors = ['.loading', '.spinner', '[class*="loading"]']
        
        for selector in loading_selectors:
            try:
                loading_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in loading_elements:
                    if element.is_displayed():
                        if not is_headless:
                            print("⏳ Mendeteksi loading indicator...")
                        
                        # Tunggu sampai loading hilang
                        WebDriverWait(driver, timeout).until_not(
                            EC.visibility_of(element)
                        )
                        break
            except:
                continue
        
        # Tunggu tambahan
        time.sleep(3)
        
        if is_headless:
            print(f"✅ {W}Data dimuat")
        else:
            print(f"🔧 {W}Debug: Selesai menunggu data")
        
        return True
        
    except Exception as e:
        if not detect_headless_mode_simple(driver):
            print(f"🔧 {W}Debug: Error wait_for_data_load: {str(e)}")
        return False

def take_enhanced_screenshot(driver, domain, headless=False):
    """Ambil screenshot dengan informasi tambahan"""
    try:
        # Scroll ke atas untuk memastikan header terlihat
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Ambil screenshot
        timestamp = int(time.time())
        screenshot_path = f"backlinks_{domain}_{timestamp}.png"
        
        if driver.save_screenshot(screenshot_path):
            if not headless:
                print(f"📸 {W}Screenshot disimpan: {G}{screenshot_path}")
                
                # Informasi tambahan tentang screenshot (hanya untuk mode GUI)
                current_url = driver.current_url
                page_title = driver.title
                
                print(f"📋 {W}Info screenshot:")
                print(f"📍 {W}URL: {Y}{current_url}")
                print(f"📄 {W}Judul: {Y}{page_title}")
                print(f"🕒 {W}Timestamp: {Y}{timestamp}")
            
            return screenshot_path
        else:
            if not headless:
                print("❌ Gagal menyimpan screenshot")
            return None
            
    except Exception as e:
        if not headless:
            print(f"❌ Error mengambil screenshot: {str(e)}")
        return None

def extract_backlink_urls_button_click(driver, domain, headless=False):
    """
    Ekstrak URL dengan klik button-link untuk memunculkan nested rows
    Dengan output yang disesuaikan untuk mode headless dan GUI
    """
    try:
        if headless:
            print(f"\n{G}" + "═" * 50)
            print(f"🔗 {Y}EKSTRAKSI URL BACKLINK MODE HEADLESS")
            print(f"{G}═" * 50)
        else:
            print(f"\n{G}" + "═" * 50)
            print(f"🔗 {Y}EKSTRAKSI URL BACKLINK MODE GUI")
            print(f"{G}═" * 50)
        
        # Tunggu halaman dimuat
        initial_wait = 5 if headless else 8
        time.sleep(initial_wait)
        
        # Cari button-link
        buttons = driver.find_elements(By.CSS_SELECTOR, 'button.button-link')
        
        if not buttons:
            if headless:
                print("❌ Tidak ditemukan button")
            else:
                print("❌ Tidak ditemukan button.button-link")
            return []
        
        if headless:
            print(f"🔍 {W}Ditemukan {G}{len(buttons)} {W}button")
        else:
            print(f"🔍 {W}Ditemukan {G}{len(buttons)} {W}button.button-link")
        
        extracted_urls = []
        
        for i, button in enumerate(buttons, 1):
            try:
                if headless:
                    print(f"{R}─" * 50)
                    print(f"🔄 {W}Button {G}{i}{Y}/{G}{len(buttons)}")
                else:
                    print(f"{R}─" * 50)
                    print(f"🔄 {W}Memproses button {G}{i}{Y}/{G}{len(buttons)}")
                
                # Scroll dan klik button
                if headless:
                    # HEADLESS: Direct JavaScript click (fastest & most reliable)
                    driver.execute_script("arguments[0].click();", button)
                    print(f"✅ Berhasil klik button {i}")
                    
                    # Shorter wait for headless
                    time.sleep(2)
                    
                else:
                    # GUI: Scroll first, then try normal click with fallback
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                    time.sleep(1)
                    
                    try:
                        button.click()
                        print(f"✅ Berhasil klik button {i}")
                    except Exception:
                        driver.execute_script("arguments[0].click();", button)
                        print(f"✅ Berhasil klik button {i} dengan JavaScript")
                    
                    # Longer wait for GUI (visual confirmation)
                    time.sleep(3)
                
                # TUNGGU SAMPAI NESTED ROWS MUNCUL DAN URL DITEMUKAN
                max_wait_attempts = 10  # Maksimal 10 kali cek (20-30 detik)
                wait_interval = 2 if headless else 3  # Interval pengecekan
                urls_found_this_button = []
                
                for attempt in range(max_wait_attempts):
                    try:
                        # Cari nested rows yang muncul
                        nested_rows = driver.find_elements(By.CSS_SELECTOR, 'tr.nested.nested-even, tr.nested.nested-odd')
                        
                        if nested_rows:
                            if headless:
                                print(f"🔍 Ditemukan {len(nested_rows)} nested rows")
                            else:
                                print(f"🔍 Ditemukan {len(nested_rows)} nested rows")
                            
                            # Cari URL dalam nested rows
                            for nested_row in nested_rows:
                                try:
                                    if nested_row.is_displayed():
                                        # Cari link dalam nested row
                                        external_links = nested_row.find_elements(By.CSS_SELECTOR, 'a.external-link')
                                        
                                        for link in external_links:
                                            if link.is_displayed():
                                                url = link.get_attribute('href')
                                                if url and url.strip() and url.startswith(('http://', 'https://')):
                                                    url = url.strip()
                                                    if url not in extracted_urls and url not in urls_found_this_button:
                                                        urls_found_this_button.append(url)
                                                        extracted_urls.append(url)
                                                        if headless:
                                                            print(f"🔗 {W}URL ditemukan:{Y} {url}")
                                                            # print(f"{R}─" * 50)
                                                        else:
                                                            print(f"🔗 {W}URL ditemukan:{Y} {url}")
                                                            # print(f"{R}─" * 50)
                                except:
                                    continue
                            
                            # Jika sudah menemukan URL, keluar dari loop tunggu
                            if urls_found_this_button:
                                if headless:
                                    print(f"✅ {W}Button {Y}{i}{W} selesai - {Y}{len(urls_found_this_button)}{W} URL ditemukan")
                                else:
                                    print(f"✅ {W}Button {Y}{i}{W} selesai - {Y}{len(urls_found_this_button)}{W} URL ditemukan")
                                break
                            else:
                                # Nested rows ada tapi belum ada URL, tunggu lagi
                                if headless:
                                    print(f"⏳ {W}Menunggu URL muncul... (percobaan {Y}{attempt + 1}{R}/{Y}{max_wait_attempts}{W})")
                                else:
                                    print(f"⏳ {W}Menunggu URL muncul... (percobaan {Y}{attempt + 1}{R}/{Y}{max_wait_attempts}{W})")
                                time.sleep(wait_interval)
                        else:
                            # Nested rows belum muncul, tunggu
                            if headless:
                                print(f"⏳ {W}Menunggu nested rows... (percobaan {Y}{attempt + 1}{R}/{Y}{max_wait_attempts}{W})")
                            else:
                                print(f"⏳ {W}Menunggu nested rows muncul... (percobaan {Y}{attempt + 1}{R}/{Y}{max_wait_attempts}{W})")
                            time.sleep(wait_interval)
                    
                    except Exception as e:
                        if not headless:
                            print(f"⚠️ {R}Error saat menunggu (percobaan {Y}{attempt + 1}{R}){W}: {str(e)}")
                        time.sleep(wait_interval)
                        continue
                
                # Jika setelah semua percobaan tidak menemukan URL
                if not urls_found_this_button:
                    if headless:
                        print(f"⚠️ {R}Button {G}{i}: Tidak ada URL ditemukan setelah {Y}{max_wait_attempts} {R}percobaan")
                    else:
                        print(f"⚠️ {R}Button {G}{i}: Tidak ada URL ditemukan setelah {Y}{max_wait_attempts} {R}percobaan")
                
                # Tunggu sebentar sebelum memproses button berikutnya
                if headless:
                    time.sleep(1)
                else:
                    time.sleep(2)
                
            except Exception as e:
                if headless:
                    print(f"⚠️ Error button {i}: {str(e)}")
                else:
                    print(f"⚠️ Error memproses button {i}: {str(e)}")
                continue
        
        # Hapus duplikasi URL
        extracted_urls = list(dict.fromkeys(extracted_urls))
        
        # Simpan URL ke file .txt
        if extracted_urls:
            timestamp = int(time.time())
            filename = f"backlinks_urls_{domain}_buttonclick_{timestamp}.txt"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Backlink URLs untuk domain: {domain}\n")
                    f.write(f"Tanggal ekstraksi: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total URL: {len(extracted_urls)}\n")
                    f.write(f"Metode: Button-Link Click -> Nested Rows (Wait for URLs)\n")
                    f.write(f"Mode: {'Headless' if headless else 'GUI'}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, url in enumerate(extracted_urls, 1):
                        f.write(f"{i}. {url}\n")
                
                if headless:
                    print(f"{R}─" * 50)
                    print(f"💾 {len(extracted_urls)} {W}URL berhasil disimpan ke: {G}{filename}")
                else:
                    print(f"{R}─" * 50)
                    print(f"💾 {W}URL berhasil disimpan ke: {G}{filename}")
                    print(f"📊 {W}Total URL diekstrak: {G}{len(extracted_urls)}")
                
            except Exception as e:
                if headless:
                    print(f"❌ {R}Error simpan: {str(e)}")
                else:
                    print(f"❌ {R}Error menyimpan file: {str(e)}")
                return extracted_urls
        else:
            if headless:
                print(f"❌ {R}Tidak ada URL diekstrak")
            else:
                print(f"❌ {R}Tidak ada URL yang berhasil diekstrak")
        
        return extracted_urls
        
    except Exception as e:
        if headless:
            print(f"❌ Error: {str(e)}")
        else:
            print(f"❌ Error ekstraksi URL: {str(e)}")
        return []




def extract_backlink_urls_step_by_step(driver, domain, headless=False):
    """
    Ekstrak URL dengan pendekatan step-by-step yang lebih detail
    """
    try:
        if not headless:
            print(f"\n{G}" + "═" * 50)
            print("🔗 EKSTRAKSI URL BACKLINK (STEP BY STEP)")
            print(f"{G}═" * 50)
        
        # Tunggu halaman dimuat
        time.sleep(5)
        
        # Cari semua baris dengan class "even content-row"
        rows = driver.find_elements(By.CSS_SELECTOR, '.even.content-row')
        
        if not rows:
            if not headless:
                print("❌ Tidak ditemukan baris data")
            return []
        
        if not headless:
            print(f"🔍 Ditemukan {len(rows)} baris data")
        
        extracted_urls = []
        
        for i, row in enumerate(rows, 1):
            try:
                if not headless:
                    print(f"\n🔄 === MEMPROSES BARIS {i}/{len(rows)} ===")
                
                # Scroll dan highlight baris
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", row)
                time.sleep(1)
                
                # Highlight baris untuk debugging (hanya mode GUI)
                if not headless:
                    original_style = row.get_attribute('style')
                    driver.execute_script("arguments[0].style.border='3px solid red';", row)
                    time.sleep(1)
                
                # Klik baris
                if not headless:
                    print(f"👆 Mengklik baris {i}...")
                
                try:
                    row.click()
                except:
                    driver.execute_script("arguments[0].click();", row)
                
                if not headless:
                    print(f"✅ Baris {i} diklik")
                
                # Tunggu elemen baru muncul
                if not headless:
                    print("⏳ Menunggu elemen baru muncul...")
                time.sleep(4)
                
                # Cari URL dalam berbagai cara
                urls_found_this_row = []
                
                # Cara 1: Dalam baris itu sendiri
                try:
                    links_in_row = row.find_elements(By.CSS_SELECTOR, 'td a.external-link')
                    for link in links_in_row:
                        if link.is_displayed():
                            url = link.get_attribute('href')
                            if url and url.startswith(('http://', 'https://')):
                                urls_found_this_row.append(url.strip())
                    
                    if not headless and urls_found_this_row:
                        print(f"🔍 Ditemukan {len(urls_found_this_row)} URL dalam baris")
                except:
                    pass
                
                # Cara 2: Dalam parent table
                if not urls_found_this_row:
                    try:
                        parent_table = row.find_element(By.XPATH, './ancestor::table[1]')
                        visible_links = []
                        all_links = parent_table.find_elements(By.CSS_SELECTOR, 'td a.external-link')
                        
                        for link in all_links:
                            if link.is_displayed():
                                url = link.get_attribute('href')
                                if url and url.startswith(('http://', 'https://')):
                                    visible_links.append(url.strip())
                        
                        # Ambil URL yang baru (belum ada di extracted_urls)
                        for url in visible_links:
                            if url not in extracted_urls:
                                urls_found_this_row.append(url)
                        
                        if not headless and urls_found_this_row:
                            print(f"🔍 Ditemukan {len(urls_found_this_row)} URL dalam tabel")
                    except:
                        pass
                
                # Cara 3: Di seluruh halaman (fallback)
                if not urls_found_this_row:
                    try:
                        all_visible_links = driver.find_elements(By.CSS_SELECTOR, 'td a.external-link')
                        current_visible = []
                        
                        for link in all_visible_links:
                            if link.is_displayed():
                                url = link.get_attribute('href')
                                if url and url.startswith(('http://', 'https://')):
                                    current_visible.append(url.strip())
                        
                        # Ambil yang belum ada
                        for url in current_visible:
                            if url not in extracted_urls:
                                urls_found_this_row.append(url)
                                break  # Ambil hanya 1 untuk menghindari duplikasi
                        
                        if not headless and urls_found_this_row:
                            print(f"🔍 Ditemukan {len(urls_found_this_row)} URL di halaman")
                    except:
                        pass
                
                # Tambahkan URL yang ditemukan
                for url in urls_found_this_row:
                    if url not in extracted_urls:
                        extracted_urls.append(url)
                        if not headless:
                            print(f"✅ URL ditambahkan: {url}")
                
                if not urls_found_this_row and not headless:
                    print("⚠️ Tidak ada URL ditemukan untuk baris ini")
                
                # Restore style (hanya mode GUI)
                if not headless:
                    try:
                        driver.execute_script(f"arguments[0].style='{original_style}';", row)
                    except:
                        pass
                
                # Tunggu sebelum baris berikutnya
                time.sleep(2)
                
            except Exception as e:
                if not headless:
                    print(f"❌ Error pada baris {i}: {str(e)}")
                continue
        
        # Simpan hasil
        if extracted_urls:
            # Hapus duplikasi
            extracted_urls = list(dict.fromkeys(extracted_urls))
            
            timestamp = int(time.time())
            filename = f"backlinks_urls_{domain}_stepbystep_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Backlink URLs untuk domain: {domain}\n")
                f.write(f"Tanggal ekstraksi: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total URL: {len(extracted_urls)}\n")
                f.write("Metode: Step by Step (detail)\n")
                f.write("=" * 50 + "\n\n")
                
                for i, url in enumerate(extracted_urls, 1):
                    f.write(f"{i}. {url}\n")
            
            if not headless:
                print(f"\n💾 URL berhasil disimpan ke: {filename}")
                print(f"📊 Total URL diekstrak: {len(extracted_urls)}")
            else:
                print(f"💾 {len(extracted_urls)} URL disimpan ke: {filename}")
        else:
            if not headless:
                print("❌ Tidak ada URL yang berhasil diekstrak")
        
        return extracted_urls
        
    except Exception as e:
        if not headless:
            print(f"❌ Error ekstraksi step by step: {str(e)}")
        return []

def backlink_menu(driver, domain, headless=False):
    """Menu interaktif untuk analisis backlink"""
    
    # Untuk SEMUA mode (headless dan GUI), tampilkan menu terlebih dahulu
    while True:
        try:
            print(f"\n{G}" + "═" * 50)
            print(f"🔗 {W}BACKLINK EXPLORER - {Y}{domain}")
            print(f"{G}═" * 50)
            print(f"{Y}1{W}.👉 {W}Refresh hasil")
            print(f"{Y}2{W}.👉 {W}Analisis hasil saat ini")
            print(f"{Y}3{W}.👉 {W}Ambil screenshot")
            print(f"{Y}4{W}.👉 {W}Ambil screenshot dengan scroll")
            print(f"{Y}5{W}.👉 {W}Tampilkan URL saat ini")
            print(f"{Y}6{W}.👉 {W}Cari domain baru")
            print(f"{Y}7{W}.👉 {W}Tunggu data dimuat")
            print(f"{Y}8{W}.👉 {W}Ekstrak URL backlink")
            print(f"{Y}9{W}.👉 {W}Kembali ke menu utama")
            print(f"{R}─" * 50)
            
            choice = input(f"👉 {W}Masukkan pilihan:{R} ").strip()
            
            if choice == "1":
                print(f"🔄 {W}Merefresh halaman...")
                driver.refresh()
                wait_for_data_load(driver)
                print(f"✅ {W}Halaman direfresh")
                
            elif choice == "2":
                if headless:
                    print(f"🔇 {W}MODE HEADLESS - Analisis hasil")
                    analyze_results(driver, headless=True)
                else:
                    analyze_results(driver, headless=False)
                
            elif choice == "3":
                if headless:
                    print(f"🔇 {W}MODE HEADLESS - Mengambil screenshot")
                    screenshot_path = f"backlinks_{domain}_headless_{int(time.time())}.png"
                    if driver.save_screenshot(screenshot_path):
                        print(f"📸 {W}Screenshot disimpan: {G}{screenshot_path}")
                    else:
                        print(f"❌ {R}Gagal mengambil screenshot")
                else:
                    take_enhanced_screenshot(driver, domain, headless=False)
                
            elif choice == "4":
                if headless:
                    print(f"🔇 {W}MODE HEADLESS - Multiple screenshot")
                    # Screenshot atas
                    driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(2)
                    screenshot_top = f"backlinks_{domain}_headless_top_{int(time.time())}.png"
                    driver.save_screenshot(screenshot_top)
                    print(f"📸 {W}Screenshot atas:{G} {screenshot_top}")
                    
                    # Screenshot tengah
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                    time.sleep(2)
                    screenshot_middle = f"backlinks_{domain}_headless_middle_{int(time.time())}.png"
                    driver.save_screenshot(screenshot_middle)
                    print(f"📸 {W}Screenshot tengah:{G} {screenshot_middle}")
                    
                    # Screenshot bawah
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    screenshot_bottom = f"backlinks_{domain}_headless_bottom_{int(time.time())}.png"
                    driver.save_screenshot(screenshot_bottom)
                    print(f"📸 {W}Screenshot bawah:{G} {screenshot_bottom}")
                else:
                    print(f"📸 {W}Mengambil multiple screenshot...")
                    take_enhanced_screenshot(driver, domain, headless=False)
                    
                    # Screenshot dengan scroll
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                    time.sleep(2)
                    screenshot_path = f"backlinks_{domain}_middle_{int(time.time())}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"📸 {W}Screenshot tengah:{G} {screenshot_path}")
                    
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    screenshot_path = f"backlinks_{domain}_bottom_{int(time.time())}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"📸 {W}Screenshot bawah: {G}{screenshot_path}")
                
            elif choice == "5":
                current_url = driver.current_url
                print(f"📍 {W}URL saat ini: {Y}{current_url}")
                
            elif choice == "6":
                new_domain = get_domain_input(headless=headless)
                if new_domain:
                    # Update domain dan navigasi ke URL baru
                    encoded_domain = new_domain.replace('.', '%2E')
                    backlink_url = f"https://analytics.moz.com/pro/link-explorer/linking-domains?site={encoded_domain}&state=all&target=domain&type=all"
                    
                    print(f"🌐 {W}Navigasi ke: {Y}{backlink_url}")
                    driver.get(backlink_url)
                    
                    # Tunggu halaman dimuat
                    print("⏳ Menunggu halaman dimuat...")
                    time.sleep(15)
                    
                    # Cek dan tampilkan quota
                    check_and_display_quota(driver)
                    
                    domain = new_domain  # Update domain saat ini
                    wait_for_data_load(driver)
                    print(f"✅ {W}Domain berhasil diubah ke: {Y}{domain}")
                        
            elif choice == "7":
                if headless:
                    print(f"🔇 {W}MODE HEADLESS - Menunggu data dimuat")
                    wait_for_data_load(driver, timeout=45)
                else:
                    wait_for_data_load(driver, timeout=60)
                
            elif choice == "8":
                # Ekstrak URL backlink dengan handling mode headless
                if headless:
                    # print(f"🔇 {W}MODE HEADLESS - Analisis backlink untuk{Y}", {domain})
                    print(f"🔇 {W}MODE HEADLESS - Analisis backlink untuk{Y} {domain}")
                    
                    # Tunggu data dimuat
                    print(f"⏳ {W}Menunggu data dimuat...")
                    wait_for_data_load(driver, timeout=30)
                    
                    # Lakukan analisis otomatis
                    print(f"📊 {W}Menganalisis hasil...")
                    analysis_success = analyze_results(driver, headless=True)
                    
                    if analysis_success:
                        print(f"✅ {G}Analisis selesai!")
                    else:
                        print("⚠️ Analisis tidak lengkap, melanjutkan ekstraksi...")
                    
                    # Ekstrak URL backlink dengan metode button-click
                    print(f"🔗 {W}Memulai ekstraksi URL backlink...")
                    extracted_urls = extract_backlink_urls_button_click(driver, domain, headless=True)
                    
                    if extracted_urls:
                        print(f"✅ {len(extracted_urls)} URL berhasil diekstrak")
                    else:
                        print("⚠️ Tidak ada URL yang berhasil diekstrak")
                    
                    print("🎉 Proses mode headless selesai!")
                    
                else:
                    # Mode GUI - deteksi otomatis atau manual
                    print("🔗 Memulai ekstraksi URL backlink...")
                    
                    # Deteksi mode headless berdasarkan driver options
                    is_headless_detected = driver.capabilities.get('browserName') == 'chrome' and driver.capabilities.get('chrome', {}).get('headless', False)
                    
                    if is_headless_detected:
                        print(f"🔇 {G}Mode headless {G}terdeteksi")
                    else:
                        print(f"🖥️ {G}Mode GUI {W}terdeteksi")
                    
                    extracted_urls = extract_backlink_urls_button_click(driver, domain, headless=is_headless_detected)
                    
                    if extracted_urls:
                        print(f"🎉 {W}Ekstraksi selesai! {G}{len(extracted_urls)} URL {W}berhasil diekstrak")
                        
                        # Tampilkan preview URL (maksimal 5)
                        print("\n📋 Preview URL yang diekstrak:")
                        for i, url in enumerate(extracted_urls[:5], 1):
                            print(f"   {i}. {Y}{url}")
                        
                        if len(extracted_urls) > 5:
                            print(f"   {W}... dan {G}{len(extracted_urls) - 5} URL {W}lainnya")
                            
                    else:
                        print("❌ Tidak ada URL yang berhasil diekstrak")
                        print("💡 Tips troubleshooting:")
                        print("   - Pastikan halaman sudah dimuat sepenuhnya")
                        print("   - Coba refresh halaman dan tunggu beberapa saat")
                        print("   - Periksa apakah ada button-link di halaman")
                        print("   - Periksa apakah ada data backlink di halaman")
                
            elif choice == "9":
                print(f"{Y}↩️ {W}Kembali ke menu utama...")
                break
            else:
                print("❌ Pilihan tidak valid. Silakan masukkan 1-9.")
                
        except KeyboardInterrupt:
            print("\n⚠️ Dihentikan oleh pengguna. Kembali ke menu utama...")
            break
        except Exception as e:
            print(f"❌ Error dalam menu backlink: {str(e)}")
            break
def run_backlink_explorer(driver, headless=False):
    """
    Fungsi utama untuk menjalankan backlink explorer
    DEPRECATED: Gunakan backlink_menu() langsung dari menu utama
    
    Args:
        driver: Instance Selenium WebDriver dari script utama
        headless (bool): Apakah berjalan dalam mode headless
    """
    print("⚠️ DEPRECATED: Fungsi ini sudah digantikan dengan integrasi menu utama")
    print("💡 Silakan gunakan menu utama -> opsi 4 (Analisis Backlink)")
    
    # Fallback untuk kompatibilitas
    try:
        domain = get_domain_input(headless=headless)
        
        if not domain:
            print("❌ Tidak ada domain valid yang diberikan.")
            return False
        
        # Navigasi ke halaman backlink
        encoded_domain = domain.replace('.', '%2E')
        backlink_url = f"https://analytics.moz.com/pro/link-explorer/linking-domains?site={encoded_domain}&state=all&target=domain&type=all"
        
        print(f"🌐 {W}Navigasi ke:{Y} {backlink_url}")
        driver.get(backlink_url)
        
        # Tunggu halaman dimuat
        print("⏳ Menunggu halaman dimuat...")
        time.sleep(15)
        
        # Jalankan menu backlink
        backlink_menu(driver, domain, headless=headless)
        
        return True
        
    except Exception as e:
        print(f"❌ Error dalam backlink explorer: {str(e)}")
        return False

def auto_backlink_analysis(driver, domain_list, headless=True):
    """
    Analisis backlink otomatis untuk multiple domain (khusus mode headless)
    
    Args:
        driver: Instance Selenium WebDriver
        domain_list (list): Daftar domain untuk dianalisis
        headless (bool): Mode headless (default True)
    """
    if not headless:
        print("⚠️ Fungsi ini dirancang untuk mode headless")
        return False
    
    print("🤖 ANALISIS BACKLINK OTOMATIS")
    print(f"{G}═" * 50)
    print(f"📋 Akan menganalisis {len(domain_list)} domain")
    
    results = []
    
    for i, domain in enumerate(domain_list, 1):
        print(f"\n🔄 Memproses domain {i}/{len(domain_list)}: {domain}")
        
        # Validasi domain
        cleaned_domain = validate_domain(domain)
        if not cleaned_domain:
            print(f"❌ Domain tidak valid: {domain}")
            results.append({
                'domain': domain,
                'status': 'invalid',
                'error': 'Format domain tidak valid'
            })
            continue
        
        try:
            # Cari backlink untuk domain ini menggunakan metode GET langsung
            if search_backlinks_direct_url(driver, cleaned_domain, headless=True):
                print(f"✅ Navigasi berhasil untuk {cleaned_domain}")
                
                # Tunggu hasil dimuat
                time.sleep(20)
                wait_for_data_load(driver, timeout=45)
                
                # Analisis hasil
                analysis_success = analyze_results(driver, headless=True)
                
                # Ekstrak URL backlink
                extracted_urls = extract_backlink_urls_button_click(driver, cleaned_domain, headless=True)
                
                # Ambil multiple screenshot (silent)
                screenshots = []
                try:
                    # Screenshot utama
                    screenshot_main = take_enhanced_screenshot(driver, cleaned_domain, headless=True)
                    if screenshot_main:
                        screenshots.append(screenshot_main)
                    
                    # Screenshot dengan scroll
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                    time.sleep(3)
                    screenshot_middle = f"auto_backlinks_{cleaned_domain}_middle_{int(time.time())}.png"
                    if driver.save_screenshot(screenshot_middle):
                        screenshots.append(screenshot_middle)
                    
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    screenshot_bottom = f"auto_backlinks_{cleaned_domain}_bottom_{int(time.time())}.png"
                    if driver.save_screenshot(screenshot_bottom):
                        screenshots.append(screenshot_bottom)
                        
                except Exception as e:
                    pass  # Silent error
                
                results.append({
                    'domain': cleaned_domain,
                    'status': 'success',
                    'analysis_success': analysis_success,
                    'extracted_urls': len(extracted_urls) if extracted_urls else 0,
                    'screenshots': screenshots,
                    'timestamp': int(time.time()),
                    'url': driver.current_url
                })
                
                print("✅ Analisis selesai!")
                
            else:
                print(f"❌ Navigasi gagal untuk {cleaned_domain}")
                results.append({
                    'domain': cleaned_domain,
                    'status': 'failed',
                    'error': 'Navigasi ke halaman backlink gagal'
                })
                
        except Exception as e:
            print(f"❌ Error memproses {cleaned_domain}: {str(e)}")
            results.append({
                'domain': cleaned_domain,
                'status': 'error',
                'error': str(e)
            })
        
        # Jeda antar domain untuk menghindari rate limiting
        if i < len(domain_list):
            time.sleep(10)
    
    # Tampilkan ringkasan hasil
    print(f"\n{G}" + "═" * 50)
    print("📊 RINGKASAN ANALISIS OTOMATIS")
    print(f"{G}═" * 50)
    
    success_count = len([r for r in results if r['status'] == 'success'])
    failed_count = len([r for r in results if r['status'] in ['failed', 'error']])
    invalid_count = len([r for r in results if r['status'] == 'invalid'])
    
    print(f"✅ Berhasil: {success_count}")
    print(f"❌ Gagal: {failed_count}")
    print(f"⚠️ Tidak valid: {invalid_count}")
    print(f"📊 Total: {len(domain_list)}")
    
    # Detail hasil
    print("\n📋 DETAIL HASIL:")
    print("-" * 40)
    for result in results:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        print(f"{status_icon} {result['domain']} - {result['status']}")
        
        if result['status'] == 'success':
            if result.get('extracted_urls', 0) > 0:
                print(f"   🔗 URL diekstrak: {result['extracted_urls']}")
            if result.get('screenshots'):
                print(f"   📸 Screenshots: {len(result['screenshots'])} file")
        elif 'error' in result:
            print(f"   ❌ Error: {result['error']}")
    
    return results

def test_single_domain_headless(driver, domain="example.com"):
    """Test fungsi untuk single domain dalam mode headless"""
    print("🧪 TEST MODE HEADLESS - Single Domain")
    print("=" * 50)
    print(f"🎯 Testing domain: {domain}")
    
    try:
        # Test navigasi langsung
        if search_backlinks_direct_url(driver, domain, headless=True):
            print("✅ Navigasi berhasil")
            
            # Tunggu dan analisis
            time.sleep(15)
            wait_for_data_load(driver, timeout=30)
            
            analysis_result = analyze_results(driver, headless=True)
            
            # Test ekstraksi URL
            extracted_urls = extract_backlink_urls_button_click(driver, domain, headless=True)
            
            # Screenshot
            screenshot = take_enhanced_screenshot(driver, domain, headless=True)
            
            print(f"\n📋 HASIL TEST:")
            print(f"✅ Navigasi: Berhasil")
            print(f"📊 Analisis: {'Berhasil' if analysis_result else 'Tidak lengkap'}")
            print(f"🔗 URL diekstrak: {len(extracted_urls) if extracted_urls else 0}")
            print(f"📸 Screenshot: {'Berhasil' if screenshot else 'Gagal'}")
            
            return True
        else:
            print("❌ Test gagal - navigasi tidak berhasil")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def main():
    """Fungsi standalone untuk testing backlink.py secara independen"""
    print("⚠️ Script ini dirancang untuk bekerja dengan moz_login.py")
    print("💡 Silakan jalankan moz_login.py dan pilih opsi 10 untuk menggunakan fitur ini")
    print("🔗 Atau integrasikan ini dengan Selenium driver yang sudah ada")
    
    # Contoh penggunaan untuk testing
    print("\n🧪 MODE TESTING - Contoh penggunaan:")
    print("=" * 50)
    
    # Test domain input untuk headless
    print("\n🔇 Test Mode Headless:")
    test_domain = get_domain_input(headless=True)
    print(f"Domain yang akan digunakan: {test_domain}")
    
    print("\n💡 Untuk menggunakan fitur ini:")
    print("1. Jalankan moz_login.py")
    print("2. Login ke akun Moz Anda")
    print("3. Pilih opsi 10 (Analisis Backlink)")
    print("4. Masukkan domain yang ingin dianalisis")
    
    print("\n🔧 Metode Button-Link:")
    print("✅ Klik button-link untuk memunculkan nested rows")
    print("✅ Ambil URL dari tr.nested.nested-even dan tr.nested.nested-odd")
    print("✅ Ekstrak dari a.external-link dalam nested rows")

if __name__ == "__main__":
    main()
def detect_headless_mode_simple(driver):
    """
    Deteksi sederhana mode headless berdasarkan window properties
    
    Args:
        driver: Instance Selenium WebDriver
        
    Returns:
        bool: True jika headless, False jika GUI
    """
    try:
        # Cek apakah ada window.outerHeight dan outerWidth
        outer_height = driver.execute_script("return window.outerHeight || 0;")
        outer_width = driver.execute_script("return window.outerWidth || 0;")
        
        # Cek screen availability
        screen_available = driver.execute_script("""
            return window.screen && 
                   window.screen.availHeight > 0 && 
                   window.screen.availWidth > 0;
        """)
        
        # Jika outer dimensions 0 atau screen tidak tersedia, kemungkinan headless
        is_headless = (outer_height == 0 or outer_width == 0) or not screen_available
        
        return is_headless
        
    except Exception:
        # Jika error, asumsikan GUI mode (safer default)
        return False

def get_headless_mode_from_driver(driver):
    """
    Alternatif untuk mendapatkan mode headless dari driver properties
    Jika detect_headless_mode gagal
    """
    try:
        # Cek user agent untuk indikator headless
        user_agent = driver.execute_script("return navigator.userAgent;")
        
        # Beberapa headless browser menambahkan "HeadlessChrome" di user agent
        if "HeadlessChrome" in user_agent:
            return True
        
        # Cek window properties
        window_props = driver.execute_script("""
            return {
                outerHeight: window.outerHeight,
                outerWidth: window.outerWidth,
                screenX: window.screenX,
                screenY: window.screenY,
                devicePixelRatio: window.devicePixelRatio
            };
        """)
        
        # Jika outer dimensions adalah 0, kemungkinan headless
        return window_props['outerHeight'] == 0 or window_props['outerWidth'] == 0
        
    except Exception:
        return False