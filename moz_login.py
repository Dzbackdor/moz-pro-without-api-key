import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import getpass
import sys
import random
import os
from colorama import Fore, init
# Initialize Colorama
init(autoreset=True)

# Colors for terminal text
B = Fore.BLUE
W = Fore.WHITE
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW

# ✅ MONKEY PATCH UNTUK HILANGKAN WARNING
import warnings
warnings.filterwarnings("ignore")

# Override logging untuk undetected_chromedriver
class SilentLogger:
    def debug(self, *args, **kwargs): pass
    def info(self, *args, **kwargs): pass
    def warning(self, *args, **kwargs): pass
    def error(self, *args, **kwargs): pass
    def critical(self, *args, **kwargs): pass

# Replace logger
logging.getLogger('undetected_chromedriver').handlers = []
logging.getLogger('undetected_chromedriver').addHandler(logging.NullHandler())
logging.getLogger('undetected_chromedriver').propagate = False

# Setup logging utama
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def clear_terminal():
    """
    Membersihkan terminal untuk semua OS (Windows, Linux, macOS)
    """
    try:
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # Linux/macOS
        else:
            os.system('clear')
    except Exception as e:
        print(f"{R}Gagal membersihkan terminal: {e}{W}")


def banner():
    print(rf"""
{R}╔══════════════════════════════════════╗
{R}║ {B}  /\/\   ___ ____ {Y} _ __  _ __ ___    {R}║
{R}║ {B} /    \ / _ \_  / {Y}| '_ \| '__/ _ \   {R}║
{R}║ {B}/ /\/\ \ (_) / /  {Y}| |_) | | | (_) |  {R}║
{R}║ {B}\/    \/\___/___| {Y}| .__/|_|  \___/   {R}║
{R}║🐍 {W}Python Seo Tool {Y}|_|{W} Without Api Key{R}║         
{R}╚══════════════════════════════════════╝
""")


def get_random_user_agent():
    """
    Ambil user agent secara acak dari file user-agents.txt
    
    Returns:
        str: User agent string atau default jika file tidak ditemukan
    """
    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    try:
        # Cek apakah file user-agents.txt ada
        if not os.path.exists('user-agents.txt'):
            print("⚠️ File user-agents.txt tidak ditemukan, menggunakan user agent default")
            return default_user_agent
        
        # Baca semua user agents dari file
        with open('user-agents.txt', 'r', encoding='utf-8') as f:
            user_agents = [line.strip() for line in f.readlines() if line.strip()]
        
        if not user_agents:
            print("⚠️ File user-agents.txt kosong, menggunakan user agent default")
            return default_user_agent
        
        # Pilih user agent secara acak
        selected_user_agent = random.choice(user_agents)
        print(f"🎲 Random User agent : {Y}{selected_user_agent[:80]}...")
        
        return selected_user_agent
        
    except Exception as e:
        print(f"⚠️ {W}Error membaca file user-agents.txt: {str(e)}")
        print(f"🔄 {W}Menggunakan user agent default")
        return default_user_agent




class MozLogin:
    def __init__(self, headless=False, window_size=None):
        """
        Inisialisasi kelas Moz login
        
        Args:
            headless (bool): Jalankan browser dalam mode headless
            window_size (tuple): Ukuran jendela browser (lebar, tinggi)
        """
        self.driver = None
        self.headless = headless
        self.window_size = window_size
        
    def get_chrome_version(self):
        """Deteksi versi Chrome yang terinstal"""
        try:
            import subprocess
            import re
            
            # Windows
            if os.name == 'nt':
                try:
                    # Method 1: Registry
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                    version, _ = winreg.QueryValueEx(key, "version")
                    winreg.CloseKey(key)
                    major_version = int(version.split('.')[0])
                    print(f"🔍 Versi Chrome dari registry: {version} (major: {major_version})")
                    return major_version
                except Exception as e1:
                    print(f"⚠️ Registry method gagal: {str(e1)}")
                    try:
                        # Method 2: Command line
                        result = subprocess.run([
                            'reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', 
                            '/v', 'version'
                        ], capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            version_match = re.search(r'version\s+REG_SZ\s+(\d+)', result.stdout)
                            if version_match:
                                major_version = int(version_match.group(1))
                                print(f"🔍 Versi Chrome dari command: {major_version}")
                                return major_version
                    except Exception as e2:
                        print(f"⚠️ Command method gagal: {str(e2)}")
            
            # Linux/Mac
            else:
                commands = [
                    ['google-chrome', '--version'],
                    ['google-chrome-stable', '--version'],
                    ['chromium-browser', '--version'],
                    ['chromium', '--version'],
                    ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version']
                ]
                
                for cmd in commands:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            version_match = re.search(r'(\d+)\.', result.stdout)
                            if version_match:
                                major_version = int(version_match.group(1))
                                print(f"🔍 Versi Chrome dari {cmd[0]}: {major_version}")
                                return major_version
                    except Exception as e:
                        print(f"⚠️ Command {cmd[0]} gagal: {str(e)}")
                        continue
            
            print("⚠️ Semua metode deteksi versi gagal")
            return None
            
        except Exception as e:
            print(f"⚠️ Error umum deteksi versi Chrome: {str(e)}")
            return None
    
    def setup_driver(self):
        """Setup undetected Chrome driver dengan versi yang terdeteksi"""
        try:
            print("🔧 Menyiapkan Chrome driver...")
            
            # Deteksi versi Chrome yang terinstal
            chrome_version = self.get_chrome_version()
            if chrome_version:
                print(f"🔍 Chrome terdeteksi: versi {chrome_version}")
            else:
                print("⚠️ Tidak dapat mendeteksi versi Chrome, menggunakan auto-detect")
            
            # Buat ChromeOptions baru
            options = uc.ChromeOptions()
            
            # Opsi dasar
            if self.headless:
                options.add_argument('--headless=new')
                print("🔇 Berjalan dalam mode headless")
            
            # Pengaturan ukuran jendela
            if self.window_size:
                width, height = self.window_size
                options.add_argument(f'--window-size={width},{height}')
                print(f"📐 Ukuran browser diatur ke: {width}x{height}")
            
            # Opsi penting untuk undetected_chromedriver
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # User agent acak dari file
            random_user_agent = get_random_user_agent()
            options.add_argument(f'--user-agent={random_user_agent}')

            # ✅ METODE 3: Dengan versi yang terdeteksi
            if chrome_version:
                print(f"🔄 Membuat driver dengan Chrome versi {chrome_version}...")
                self.driver = uc.Chrome(
                    options=options, 
                    version_main=chrome_version,
                    use_subprocess=True
                )
                print(f"✅ {G}Berhasil dengan Chrome versi {chrome_version}")
            else:
                print("🔄 Membuat driver dengan auto-detect...")
                self.driver = uc.Chrome(
                    options=options,
                    use_subprocess=True
                )
                print(f"✅ {G}Berhasil dengan auto-detect")
            
            # Atur ukuran jendela setelah driver dibuat (jika tidak headless)
            if not self.headless and self.window_size:
                width, height = self.window_size
                self.driver.set_window_size(width, height)
                print(f"📐 Jendela browser diubah ukurannya ke: {width}x{height}")
            
            # Jalankan skrip stealth
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"✅ {G}Chrome driver berhasil diinisialisasi")
            return True
            
        except Exception as e:
            print(f"❌ Gagal menyiapkan driver: {str(e)}")
            logger.error(f"Gagal menyiapkan driver: {str(e)}")
            return False
    
    def close_popups(self):
        """
        Tutup popup yang mungkin muncul setelah login
        
        Returns:
            bool: True jika popup berhasil ditangani, False jika tidak ada
        """
        try:
            print("🔍 Memeriksa popup...")
            
            # Selector popup umum untuk "ubah password" dan notifikasi lainnya
            popup_selectors = [
                # Selector popup ubah password
                '[data-testid="change-password-modal"]',
                '[data-testid="password-modal"]',
                '.password-change-modal',
                '.change-password-popup',
                '.password-popup',
                
                # Selector modal umum
                '.modal',
                '.popup',
                '.overlay',
                '[role="dialog"]',
                '[role="alertdialog"]',
                '.dialog',
                
                # Selector modal Bootstrap
                '.modal-dialog',
                '.modal-content',
                
                # Selector Moz khusus
                '.moz-modal',
                '.notification-modal',
                '.security-modal',
                
                # Container popup umum
                '[class*="modal"]',
                '[class*="popup"]',
                '[class*="dialog"]',
                '[id*="modal"]',
                '[id*="popup"]'
            ]
            
            popup_found = False
            
            for selector in popup_selectors:
                try:
                    popups = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for popup in popups:
                        if popup.is_displayed():
                            print(f"🔍 Menemukan popup yang terlihat: {selector}")
                            
                            # Periksa apakah ini popup terkait password
                            popup_text = popup.text.lower()
                            password_keywords = [
                                'change password', 'update password', 'password security',
                                'strengthen password', 'improve security', 'password strength',
                                'secure your account', 'password recommendation',
                                'ubah password', 'perbarui password', 'keamanan password',
                                'perkuat password', 'tingkatkan keamanan', 'amankan akun'
                            ]
                            
                            is_password_popup = any(keyword in popup_text for keyword in password_keywords)
                            
                            if is_password_popup:
                                print(f"🔐 Terdeteksi popup terkait password")
                                print(f"📝 Pratinjau teks popup: {popup_text[:100]}...")
                            
                            # Cari tombol tutup dalam popup ini
                            close_selectors = [
                                # Selector tombol X
                                '.close',
                                '.close-button',
                                '[aria-label="Close"]',
                                '[aria-label="close"]',
                                '[aria-label="Tutup"]',
                                '[data-dismiss="modal"]',
                                '.modal-close',
                                
                                # Tombol Skip/Nanti
                                'button:contains("Skip")',
                                'button:contains("Later")',
                                'button:contains("Not now")',
                                'button:contains("Maybe later")',
                                'button:contains("Remind me later")',
                                'button:contains("Lewati")',
                                'button:contains("Nanti")',
                                'button:contains("Tidak sekarang")',
                                'button:contains("Ingatkan nanti")',
                                
                                # Tombol Batal
                                'button:contains("Cancel")',
                                'button:contains("No thanks")',
                                'button:contains("Batal")',
                                'button:contains("Tidak terima kasih")',
                                
                                # Selector tutup umum
                                '[data-testid="close"]',
                                '[data-testid="skip"]',
                                '[data-testid="cancel"]',
                                
                                # Tombol tutup berbasis ikon
                                '.fa-times',
                                '.fa-close',
                                '.icon-close',
                                '.icon-x',
                                
                                # Tombol dengan simbol X
                                'button[title="Close"]',
                                'button[title="close"]',
                                'button[title="Tutup"]'
                            ]
                            
                            close_button_found = False
                            
                            # Coba temukan tombol tutup dalam popup
                            for close_selector in close_selectors:
                                try:
                                    close_buttons = popup.find_elements(By.CSS_SELECTOR, close_selector)
                                    
                                    for close_button in close_buttons:
                                        if close_button.is_displayed() and close_button.is_enabled():
                                            print(f"🎯 Menemukan tombol tutup: {close_selector}")
                                            
                                            # Coba klik tombol tutup
                                            try:
                                                close_button.click()
                                                print("✅ Popup berhasil ditutup")
                                                popup_found = True
                                                close_button_found = True
                                                time.sleep(1)
                                                break
                                            except Exception as e:
                                                print(f"⚠️ Error mengklik tombol tutup: {str(e)}")
                                                # Coba klik JavaScript
                                                try:
                                                    self.driver.execute_script("arguments[0].click();", close_button)
                                                    print("✅ Popup ditutup dengan klik JavaScript")
                                                    popup_found = True
                                                    close_button_found = True
                                                    time.sleep(1)
                                                    break
                                                except:
                                                    continue
                                    
                                    if close_button_found:
                                        break
                                        
                                except:
                                    continue
                            
                            # Jika tidak ada tombol tutup ditemukan, coba tekan tombol Escape
                            if not close_button_found:
                                print("🔍 Tidak ada tombol tutup ditemukan, mencoba tombol Escape...")
                                try:
                                    from selenium.webdriver.common.keys import Keys
                                    popup.send_keys(Keys.ESCAPE)
                                    print("✅ Popup ditutup dengan tombol Escape")
                                    popup_found = True
                                    time.sleep(1)
                                except:
                                    print("⚠️ Tombol Escape tidak berhasil")
                            
                            # Jika masih terlihat, coba klik di luar popup
                            if popup.is_displayed() and not close_button_found:
                                print("🔍 Mencoba klik di luar popup...")
                                try:
                                    # Klik pada elemen body untuk menutup popup
                                    body = self.driver.find_element(By.TAG_NAME, "body")
                                    body.click()
                                    time.sleep(1)
                                    
                                    if not popup.is_displayed():
                                        print("✅ Popup ditutup dengan klik di luar")
                                        popup_found = True
                                except:
                                    print("⚠️ Klik di luar tidak berhasil")
                            
                            break  # Keluar dari loop popup jika kita menemukan dan menangani satu
                            
                except Exception as e:
                    continue
            
            if popup_found:
                print("🎉 Popup berhasil ditangani!")
                return True
            else:
                print("ℹ️ Tidak ada popup ditemukan")
                return False
                
        except Exception as e:
            print(f"⚠️ Error menangani popup: {str(e)}")
            return False
    
    def login(self, email, password, timeout=30):
        """
        Login ke Moz.com
        
        Args:
            email (str): Email pengguna
            password (str): Password pengguna
            timeout (int): Waktu tunggu maksimum dalam detik
            
        Returns:
            bool: True jika login berhasil, False jika gagal
        """
        try:
            if not self.driver:
                if not self.setup_driver():
                    return False
            
            print("🌐 Navigasi ke halaman login Moz")
            self.driver.get("https://moz.com/login")
            
            # Tunggu halaman dimuat
            wait = WebDriverWait(self.driver, timeout)
            
            # Tunggu field email dan masukkan email
            # print("📧 Memasukkan email...")
            email_field = wait.until(
                EC.element_to_be_clickable((By.ID, "email"))
            )
            email_field.clear()
            time.sleep(1)
            email_field.send_keys(email)
            print(f"📧 {G}Email berhasil dimasukkan")
            
            # Temukan dan masukkan password
            # print("🔐 Memasukkan password...")
            password_field = wait.until(
                EC.element_to_be_clickable((By.ID, "password"))
            )
            password_field.clear()
            time.sleep(1)
            password_field.send_keys(password)
            print(f"🔐 {G}Password berhasil dimasukkan")
            
            # Tunggu sebentar sebelum klik submit
            time.sleep(2)
            
            # Temukan dan klik tombol login
            print("🔘 Mengklik tombol login...")
            login_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            login_button.click()
            
            # Tunggu login selesai
            print("⏳ Menunggu login selesai...")
            try:
                # Tunggu redirect ke halaman home atau halaman login lainnya
                wait = WebDriverWait(self.driver, 45)  # Timeout ditingkatkan
                wait.until(
                    lambda driver: (
                        # Indikator sukses utama - halaman home
                        "moz.com/home" in driver.current_url.lower() or
                        # Halaman sukses lainnya yang mungkin
                        "dashboard" in driver.current_url.lower() or 
                        "pro" in driver.current_url.lower() or
                        "campaigns" in driver.current_url.lower() or
                        "tools" in driver.current_url.lower() or
                        # Indikator umum - tidak lagi di halaman login
                        ("moz.com/login" not in driver.current_url.lower() and 
                         "login" not in driver.current_url.lower())
                    )
                )
                
                current_url = self.driver.current_url
                # print(f"🔍 Dialihkan ke: {current_url}")
                
                # Tangani popup setelah login berhasil
                # print("🔍 Memeriksa popup setelah login...")
                time.sleep(2)  # Tunggu sebentar agar popup muncul
                self.close_popups()
                
                # Periksa khusus untuk halaman home
                if "moz.com/home" in current_url.lower():
                    print(f"🎉 {G}Login berhasil! Dialihkan ke halaman home.")
                    return True
                elif any(page in current_url.lower() for page in ["dashboard", "pro", "campaigns", "tools"]):
                    print("🎉 Login berhasil! Dialihkan ke platform Moz.")
                    return True
                else:
                    print("🎉 Login tampaknya berhasil! Halaman berubah dari login.")
                    return True
                
            except TimeoutException:
                # Periksa pesan error
                current_url = self.driver.current_url
                print(f"⚠️ Timeout terjadi. URL saat ini: {current_url}")
                
                error_selectors = [
                    ".error", 
                    ".alert-danger", 
                    "[class*='error']",
                    ".form-error",
                    ".login-error",
                    ".alert",
                    ".message"
                ]
                
                for selector in error_selectors:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if error_elements and error_elements[0].is_displayed():
                        error_text = error_elements[0].text
                        print(f"❌ Login gagal dengan error: {error_text}")
                        return False
                
                # Jika masih di halaman login, login gagal
                if "login" in current_url.lower():
                    print("❌ Login gagal - masih di halaman login")
                    return False
                else:
                    print("🤔 Tidak pasti - halaman berubah tapi timeout terjadi")
                    # Tetap coba tangani popup meskipun tidak pasti
                    self.close_popups()
                    return True
                
        except TimeoutException:
            print("❌ Timeout menunggu elemen halaman")
            return False
        except NoSuchElementException as e:
            print(f"❌ Tidak dapat menemukan elemen yang diperlukan: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error tak terduga saat login: {str(e)}")
            return False
    
    def is_logged_in(self):
        """
        Periksa apakah pengguna saat ini sudah login
        
        Returns:
            bool: True jika sudah login, False jika belum
        """
        try:
            if not self.driver:
                print("🔍 Debug: Tidak ada driver tersedia")
                return False
            
            current_url = self.driver.current_url.lower()
            print(f"{W}🔍 Debug URL saat ini: {Y}{current_url}")
            
            # Pemeriksaan utama: Halaman home menunjukkan login berhasil
            if "moz.com/home" in current_url:
                print(f"✅ Debug: Login dikonfirmasi - {Y}di halaman home")
                return True
            
            # Pemeriksaan kedua: Halaman login lainnya
            logged_in_urls = ["dashboard", "profile", "pro", "campaigns", "tools", "keyword-explorer", "link-explorer"]
            url_match = any(url in current_url for url in logged_in_urls)
            if url_match:
                print("✅ Debug: Login dikonfirmasi - di halaman platform Moz")
                return True
            
            # Pemeriksaan ketiga: Tidak di halaman login
            if "login" not in current_url:
                print("✅ Debug: Tidak di halaman login - kemungkinan sudah login")
                
                # Verifikasi tambahan: Cari form login
                login_form_selectors = ["#email", "#password", "input[type='email']", "input[type='password']"]
                has_login_form = False
                for selector in login_form_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and elements[0].is_displayed():
                        has_login_form = True
                        break
                
                if not has_login_form:
                    print("✅ Debug: Tidak ada form login terlihat - dikonfirmasi sudah login")
                    return True
                else:
                    print("❌ Debug: Form login masih terlihat")
                    return False
            
            # Pemeriksaan keempat: Cari indikator login
            logged_in_indicators = [
                # Selector menu pengguna
                "[data-testid='user-menu']",
                "[data-qa='user-menu']", 
                ".user-menu",
                ".user-avatar",
                
                # Elemen navigasi
                ".dashboard",
                "[href*='dashboard']",
                "[href*='logout']",
                "[href*='account']",
                "[href*='billing']",
                
                # Elemen khusus Moz
                ".moz-nav",
                ".pro-nav",
                ".main-nav",
                "[data-cy='user-menu']",
                ".user-dropdown",
                
                # Indikator login umum
                ".logged-in",
                "[class*='logged']"
            ]
            
            print("🔍 Debug: Memeriksa elemen login...")
            
            for indicator in logged_in_indicators:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                    if elements:
                        for element in elements:
                            if element.is_displayed():
                                print(f"✅ Debug: Menemukan elemen login: {indicator}")
                                return True
                except Exception:
                    continue
            
            print("❌ Debug: Tidak ada indikator login ditemukan")
            return False
            
        except Exception as e:
            print(f"❌ Debug: Error memeriksa status login: {str(e)}")
            return False
    
    def get_current_url(self):
        """Dapatkan URL saat ini"""
        if self.driver:
            return self.driver.current_url
        return None
    
    def navigate_to(self, url):
        """Navigasi ke URL tertentu"""
        if self.driver:
            try:
                print(f"{W}🌐 Navigasi ke: {Y}{url}")
                self.driver.get(url)
                
                # Periksa popup setelah navigasi
                time.sleep(2)
                self.close_popups()
                
                return True
            except Exception as e:
                print(f"❌ Error navigasi ke {url}: {str(e)}")
                return False
        return False
    
    def get_driver(self):
        """Dapatkan instance driver untuk digunakan di modul lain"""
        return self.driver
    
    def is_headless(self):
        """Periksa apakah driver berjalan dalam mode headless"""
        return self.headless
    
    def wait_for_user_action(self):
        """Tunggu aksi pengguna dengan opsi menu yang telah disederhanakan"""
        while True:
            try:
                print(f"\n{G}" + "═" * 50)
                print(f"🎯 {W}BROWSER SIAP - {Y}Pilih tindakan:")
                print(f"{G}═" * 50)
                print(f"{Y}1{W}.👉 {W}Periksa status login")
                print(f"{Y}2{W}.👉 {W}Pergi ke Moz Home")
                print(f"{Y}3{W}.👉 {W}Ambil screenshot")
                print(f"{Y}4{W}.👉 {W}Cek quota")
                print(f"{Y}5{W}.👉 {W}Analisis Backlink")
                print(f"{Y}6{W}.👉 {W}Tutup browser dan keluar")
                print(f"{R}─" * 50)
                
                choice = input(f"👉 {W}Masukkan pilihan atau tekan Enter untuk tutup:{R} ").strip()
                
                if choice == "" or choice == "6":
                    print(f"🔒 {W}Menutup browser...")
                    break
                elif choice == "1":
                    if self.is_logged_in():
                        print(f"✅ {G}Masih login ke Moz.com")
                    else:
                        print("❌ Tidak login atau sesi berakhir")
                elif choice == "2":
                    self.navigate_to("https://moz.com/home")
                elif choice == "3":
                    try:
                        screenshot_path = f"moz_screenshot_{int(time.time())}.png"
                        self.driver.save_screenshot(screenshot_path)
                        print(f"{W}📸 Screenshot disimpan: {G}{screenshot_path}")
                    except Exception as e:
                        print(f"❌ Error mengambil screenshot: {str(e)}")
                elif choice == "4":
                    # Cek quota - navigasi ke Link Explorer
                    try:
                        print(f"{W}📊 Mengecek quota Moz...")
                        print(f"{W}🌐 Navigasi ke Link Explorer...")
                        
                        # Navigasi ke halaman Link Explorer
                        self.driver.get("https://analytics.moz.com/pro/link-explorer/linking-domains")
                        
                        # Tunggu halaman dimuat
                        print("⏳ Menunggu halaman dimuat...")
                        time.sleep(10)
                        
                        # Cek dan tampilkan quota
                        try:
                            # Cari elemen quota dengan berbagai selector
                            quota_selectors = [
                                "p.links-quota",
                                ".links-quota", 
                                "[class*='quota']",
                                "[class*='queries']",
                                "p:contains('queries available')",
                                "span:contains('queries available')",
                                "div:contains('queries available')"
                            ]
                            
                            quota_found = False
                            
                            for selector in quota_selectors:
                                try:
                                    quota_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                                    for quota_element in quota_elements:
                                        if quota_element.is_displayed() and quota_element.text.strip():
                                            quota_text = quota_element.text.strip()
                                            if 'queries' in quota_text.lower() or 'quota' in quota_text.lower():
                                                print(f"📊 {W}Quota: {G}{quota_text}")
                                                quota_found = True
                                                break
                                    if quota_found:
                                        break
                                except Exception:
                                    continue
                            
                            if not quota_found:
                                # Coba cari dengan XPath untuk teks yang mengandung "queries"
                                try:
                                    xpath_selectors = [
                                        "//*[contains(text(), 'queries available')]",
                                        "//*[contains(text(), 'queries')]",
                                        "//*[contains(text(), 'quota')]"
                                    ]
                                    
                                    for xpath in xpath_selectors:
                                        try:
                                            quota_elements = self.driver.find_elements(By.XPATH, xpath)
                                            for quota_element in quota_elements:
                                                if quota_element.is_displayed() and quota_element.text.strip():
                                                    quota_text = quota_element.text.strip()
                                                    print(f"📊 Quota: {G}{quota_text}")
                                                    quota_found = True
                                                    break
                                            if quota_found:
                                                break
                                        except Exception:
                                            continue
                                except Exception:
                                    pass
                            
                            if not quota_found:
                                print("ℹ️ Informasi quota tidak ditemukan di halaman")
                                print("💡 Mungkin quota tidak ditampilkan atau struktur halaman berubah")
                                
                                # Tampilkan URL saat ini untuk debugging
                                current_url = self.driver.current_url
                                print(f"📍 URL saat ini: {current_url}")
                                
                                # Coba ambil screenshot untuk debugging
                                try:
                                    screenshot_path = f"quota_debug_{int(time.time())}.png"
                                    self.driver.save_screenshot(screenshot_path)
                                    print(f"📸 Screenshot debug disimpan: {screenshot_path}")
                                except Exception:
                                    pass
                            
                        except Exception as e:
                            print(f"❌ Error mengecek quota: {str(e)}")
                            
                    except Exception as e:
                        print(f"❌ Error navigasi ke Link Explorer: {str(e)}")
                        
                elif choice == "5":
                    # Analisis Backlink - Input domain dan navigasi langsung
                    try:
                        print(f"{W}🔗 Memulai Analisis Backlink...")
                        
                        # Input domain
                        domain = input(f"{W}🌐 Masukkan domain untuk analisis backlink:{Y} ").strip()
                        if not domain:
                            print("❌ Domain tidak boleh kosong!")
                            continue
                        
                        # Import dan validasi domain
                        import backlink
                        cleaned_domain = backlink.validate_domain(domain)
                        
                        if not cleaned_domain:
                            print("❌ Format domain tidak valid!")
                            continue
                        
                        print(f"{W}✅ Domain divalidasi: {Y}{cleaned_domain}")
                        
                        # Navigasi langsung ke halaman backlink
                        encoded_domain = cleaned_domain.replace('.', '%2E')
                        backlink_url = f"https://analytics.moz.com/pro/link-explorer/linking-domains?site={encoded_domain}&state=all&target=domain&type=all"
                        
                        print(f"{W}🌐 Navigasi ke: {Y}{backlink_url}")
                        self.driver.get(backlink_url)
                        
                        # Tunggu halaman dimuat
                        print("⏳ Menunggu halaman dimuat...")
                        time.sleep(15)
                        
                        # Cek dan tampilkan quota
                        try:
                            quota_element = self.driver.find_element(By.CSS_SELECTOR, "p.links-quota")
                            if quota_element.is_displayed():
                                quota_text = quota_element.text
                                print(f"📊 Quota: {G}{quota_text}")
                            else:
                                print("ℹ️ Informasi quota tidak terlihat")
                        except Exception:
                            print("ℹ️ Informasi quota tidak ditemukan")
                        
                        # Jalankan menu backlink explorer (SELALU tampilkan menu dulu)
                        backlink.backlink_menu(self.driver, cleaned_domain, headless=self.headless)
                        
                    except ImportError:
                        print("❌ backlink.py tidak ditemukan!")
                        print("💡 Pastikan backlink.py berada di direktori yang sama.")
                    except Exception as e:
                        print(f"❌ Error menjalankan analisis backlink: {str(e)}")
                else:
                    print("❌ Pilihan tidak valid. Silakan masukkan 1-6.")
                    
            except KeyboardInterrupt:
                print("\n⚠️ Dihentikan oleh pengguna. Menutup browser...")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                break
    
    def close(self):
        """Tutup browser"""
        if self.driver:
            try:
                self.driver.quit()
                print("🔒 Browser berhasil ditutup")
            except Exception as e:
                print(f"❌ Error menutup browser: {str(e)}")
def get_window_size_choice():
    """Dapatkan pilihan ukuran jendela dari pengguna"""
    print("\n📐 OPSI UKURAN BROWSER:")
    print(f"{Y}─" * 50)
    print(f"{Y}1{W}.👉 {W}Kecil (800x600)")
    print(f"{Y}2{W}.👉 {W}Sedang (1024x768)")
    print(f"{Y}3{W}.👉 {W}Besar (1366x768)")
    print(f"{Y}4{W}.👉 {W}Full HD (1920x1080)")
    print(f"{Y}5{W}.👉 {W}Ukuran Custom")
    print(f"{Y}6{W}.👉 {W}Default (default sistem)")
    print(f"{R}─" * 50)
    
    while True:
        try:
            choice = input(f"👉 {W}Pilih ukuran browser (1-6):{R} ").strip()
            
            if choice == "1":
                return (800, 600)
            elif choice == "2":
                return (1024, 768)
            elif choice == "3":
                return (1366, 768)
            elif choice == "4":
                return (1920, 1080)
            elif choice == "5":
                try:
                    width = int(input(f"📏 Masukkan lebar (px):{Y} ").strip())
                    height = int(input(f"📏 Masukkan tinggi (px):{Y} ").strip())
                    if width > 0 and height > 0:
                        return (width, height)
                    else:
                        print("❌ Lebar dan tinggi harus angka positif")
                except ValueError:
                    print("❌ Silakan masukkan angka yang valid")
            elif choice == "6":
                return None
            else:
                print("❌ Pilihan tidak valid. Silakan masukkan 1-6.")
                
        except KeyboardInterrupt:
            print("\n⚠️ Menggunakan ukuran default")
            return None

def get_user_credentials():
    """Dapatkan email dan password dari input pengguna"""
    print(f"{G}═" * 50)
    print("🔐 OTOMATIS LOGIN MOZ.COM")
    print("🎯 Fitur Utama: Mode Gui, Mode Headless")
    print(f"{G}═" * 50)
    
    try:
        # Dapatkan email
        email = input("📧 Masukkan akun email moz: ").strip()
        if not email:
            print("❌ Email tidak boleh kosong!")
            return None, None, None, None
        
        # Dapatkan password (input tersembunyi)
        password = getpass.getpass(f" 🔐 Masukkan password moz: ").strip()
        if not password:
            print("❌ Password tidak boleh kosong!")
            return None, None, None, None
        
        # Tanya mode headless
        headless_input = input("🔇 Jalankan dalam mode headless? (y/n, default(mode gui): n): ").strip().lower()
        headless = headless_input in ['y', 'yes', '1', 'true', 'ya']
        
        # Dapatkan ukuran jendela (hanya jika tidak headless)
        window_size = None
        if not headless:
            window_size = get_window_size_choice()
        
        return email, password, headless, window_size
        
    except KeyboardInterrupt:
        print("\n⚠️ Proses dihentikan oleh pengguna")
        return None, None, None, None
    except Exception as e:
        print(f"❌ Error mendapatkan kredensial: {str(e)}")
        return None, None, None, None

def main():
    """
    Fungsi utama dengan input interaktif
    Menu yang tersedia:
    1. Periksa status login
    2. Pergi ke Moz Home  
    3. Ambil screenshot
    4. Analisis Backlink (terintegrasi dengan ekstraksi URL)
    5. Tutup browser dan keluar
    """
    
    # Dapatkan kredensial dari pengguna
    credentials = get_user_credentials()
    if not credentials or not credentials[0]:
        print("❌ Kredensial tidak valid. Keluar...")
        sys.exit(1)
    
    email, password, headless, window_size = credentials
    
    print(f"{G}═" * 50)
    print(f"📧 Email: {Y}{email}")
    print(f"🔇 Mode headless: {Y}{'Aktif' if headless else 'Nonaktif'}")
    if window_size:
        print(f"📐 Ukuran Browser:{Y}{window_size[0]}x{window_size[1]}")
    else:
        print(f"📐 Ukuran Browser: {Y}Default")
    print(f"{Y}─" * 50)
    
    # Buat instance login
    moz_login = MozLogin(headless=headless, window_size=window_size)
    
    try:
        # Coba login
        if moz_login.login(email, password):
            # print("\n🎉 LOGIN BERHASIL!")
            print(f"{G}═" * 50)
            
            # Tunggu sebentar agar halaman dimuat sepenuhnya
            print("⏳ Menunggu halaman dimuat sepenuhnya...")
            time.sleep(3)
            
            # Pemeriksaan popup tambahan setelah login awal
            print("🔍 Pemeriksaan popup final...")
            moz_login.close_popups()
            
            # Periksa URL saat ini
            current_url = moz_login.get_current_url()
            print(f"📍 URL saat ini: {Y}{current_url}")
            
            # Periksa apakah di halaman home secara khusus
            if "moz.com/home" in current_url.lower():
                print(f"🏠 {G}Sempurna! Anda berada di halaman home Moz.")
            
            # Verifikasi status login dengan debugging detail
            print("🔍 Memverifikasi status login...")
            if moz_login.is_logged_in():
                print("✅ Status login dikonfirmasi")
                
                # Coba dapatkan judul halaman
                try:
                    page_title = moz_login.driver.title
                    print(f"📄 Judul halaman: {page_title}")
                except:
                    print("📄 Judul halaman: Tidak dapat diambil")
                
                print("\n🎯 Anda sekarang sudah login ke Moz.com!")
                print("💡 Browser akan tetap terbuka!")
                print("🚫 Popup telah ditangani secara otomatis!")
                
                if headless:
                    print(f"🔇 {G}Mode headless aktif")
                else:
                    print(f"🖥️ {G}Mode GUI aktif")
                
                # Tunggu aksi pengguna (menu interaktif)
                moz_login.wait_for_user_action()
                    
            else:
                print("⚠️ Verifikasi login tidak pasti")
                print(f"📍 URL saat ini: {current_url}")
                
                # Beri opsi pengguna untuk melanjutkan
                print("\n🤔 Verifikasi login gagal, tapi Anda mungkin masih login.")
                print("💡 Ini bisa terjadi jika Moz mengubah struktur halaman mereka.")
                
                # Periksa apakah setidaknya tidak di halaman login
                if "login" not in current_url.lower():
                    print("✅ Kabar baik: Anda tidak lagi di halaman login!")
                    
                continue_choice = input("🔄 Apakah Anda ingin tetap membuka browser? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes', '1', 'true', 'ya']:
                    print("✅ Membiarkan browser tetap terbuka...")
                    moz_login.wait_for_user_action()
                else:
                    print("🔄 Browser akan ditutup dalam 5 detik...")
                    time.sleep(5)
        else:
            print("\n❌ LOGIN GAGAL!")
            print(f"{G}═" * 50)
            print("💡 Silakan periksa kredensial Anda dan coba lagi")
            
            # Tampilkan URL saat ini untuk debugging
            current_url = moz_login.get_current_url()
            if current_url:
                print(f"📍 URL saat ini: {current_url}")
                
                # Periksa apakah ada pesan error yang terlihat
                try:
                    error_selectors = [".error", ".alert-danger", "[class*='error']", ".form-error", ".login-error"]
                    for selector in error_selectors:
                        error_elements = moz_login.driver.find_elements(By.CSS_SELECTOR, selector)
                        if error_elements and error_elements[0].is_displayed():
                            error_text = error_elements[0].text
                            print(f"🚨 Pesan error: {error_text}")
                            break
                except:
                    pass
            
            print("🔄 Browser akan ditutup dalam 10 detik...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n⚠️ Proses dihentikan oleh pengguna")
    except Exception as e:
        print(f"\n❌ Error tak terduga: {str(e)}")
        print("🔍 Info debug:")
        if moz_login.driver:
            try:
                print(f"📍 {W}URL saat ini: {Y}{moz_login.get_current_url()}")
                print(f"📄 {W}Judul halaman: {Y}{moz_login.driver.title}")
            except:
                print("📍 Tidak dapat mendapatkan info debug")

    finally:
        # Selalu tutup browser
        try:
            moz_login.close()
        except:
            pass
        print("\n👋 Script selesai.")                
        os._exit(0)  
if __name__ == "__main__":
    clear_terminal()
    banner()
    main()