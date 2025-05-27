# 🔗 Moz Backlink Analyzer | Without api key
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15%2B-green.svg)](https://selenium-python.readthedocs.io/)

🐍 Tool otomatis untuk login ke Moz.com dan menganalisis backlink domain menggunakan Python Selenium dengan dukungan mode headless dan GUI.

note : minimal menggunakan akun moz pro standard agar mendapatkan hasil maksimal


<img src="/1.png" width="600" alt="Moz Backlink Analyzer | Without api key">

## 📋 Deskripsi

Moz Backlink Analyzer adalah tool yang memungkinkan Anda untuk:
- Login otomatis ke akun Moz.com
- Menganalisis backlink dari domain tertentu
- Mengekstrak URL backlink secara otomatis
- Mengambil screenshot hasil analisis
- Bekerja dalam mode HEADLESS (tanpa tampilan browser) dan mode GUI (tampilan browser)

Tool ini dirancang khusus untuk mengotomatisasi proses analisis backlink yang biasanya dilakukan secara manual di platform Moz.

## ⚡ Mengapa Mode Headless Direkomendasikan?

**Mode Headless** sangat direkomendasikan karena:

- **🚀 Kecepatan 3-5x lebih cepat** dibanding mode GUI
- **💾 Konsumsi RAM 60-70% lebih rendah**
- **🔋 CPU usage 40-50% lebih efisien**
- **🎯 Lebih stabil** untuk proses otomatis
- **⚡ Tidak ada gangguan visual** yang memperlambat

<img src="/2.png" width="600" alt="Moz Backlink Analyzer | Without api key">

### Perbandingan Performa:
```
Mode GUI:     ████████████████████ 100% (20 detik)
Mode Headless: ████████ 40% (8 detik)
```

## 🚀 Fitur Utama

### 🔐 Login Otomatis
- Login ke Moz.com dengan kredensial Anda (pastikan menggunakan akun moz pro standard agar hasil maksimal)
- Penanganan popup otomatis
- Verifikasi status login
- Support berbagai ukuran browser (Mode GUI)

### 🔗 Analisis Backlink
- Pencarian domain otomatis
- Ekstraksi URL backlink
- Analisis metrik (Domain Authority, Linking Domains, dll)
- Export hasil ke file .txt

### 📸 Screenshot & Dokumentasi
- Screenshot otomatis hasil analisis
- Multiple screenshot (atas, tengah, bawah)
- Timestamp pada setiap file

### 🎛️ Mode Operasi
- **Mode GUI**: Visual browser untuk monitoring
- **Mode Headless**: Background processing untuk kecepatan maksimal (Direkomendasikan)

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/Dzbackdor/moz-pro-without-api-key.git
cd moz-pro-without-api-key
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
## 🎯 Cara Penggunaan

### Menjalankan Tool
```bash
python moz_login.py
```

### Input yang Diperlukan
1. **Email Moz**: Masukkan email akun Moz.com Anda
2. **Password**: Masukkan password akun Moz.com Anda (password mode tersembunyi tidak akan tampil di terminal)
3. **Mode**: Pilih mode headless (y) atau mode GUI default(n)
4. **Ukuran Browser** (jika mode GUI): Pilih resolusi browser

## 🎮 Menu Utama

Setelah login berhasil, Anda akan melihat menu berikut:

```
🎯 BROWSER SIAP - Pilih tindakan:
═══════════════════════════════════════════════════
1.👉 Periksa status login
2.👉 Pergi ke Moz Home
3.👉 Ambil screenshot
4.👉 Cek quota
5.👉 Analisis Backlink
6.👉 Tutup browser dan keluar
```

## 🔗 Menu Analisis Backlink

Ketika memilih opsi 5 (Analisis Backlink):

```
🔗 BACKLINK EXPLORER - example.com
═══════════════════════════════════════════════════
1.👉 Refresh hasil
2.👉 Analisis hasil saat ini
3.👉 Ambil screenshot
4.👉 Ambil screenshot dengan scroll
5.👉 Tampilkan URL saat ini
6.👉 Cari domain baru
7.👉 Tunggu data dimuat
8.👉 Ekstrak URL backlink
9.👉 Kembali ke menu utama
```

## 📊 Contoh Output

### Login Berhasil
```
✅ Email berhasil dimasukkan
🔐 Password berhasil dimasukkan
🎉 LOGIN BERHASIL!
📍 URL saat ini: https://moz.com/home
✅ Status login dikonfirmasi
```

### Analisis Domain
```
🔗 Memulai pencarian backlink untuk: example.com
📊 Quota: 2,847 queries available this month
✅ Halaman Link Explorer berhasil dimuat
📊 Domain Authority: 85
🔗 Linking Domains: 1,234
🔗 Total Backlinks: 45,678
```

### Ekstraksi URL
```
🔗 EKSTRAKSI URL BACKLINK MODE HEADLESS
═══════════════════════════════════════════════════
🔍 Ditemukan 25 button
🔄 Button 1/25
✅ Berhasil klik button 1
🔍 Ditemukan 3 nested rows
🔗 URL ditemukan: https://example-site1.com/article
🔗 URL ditemukan: https://example-site2.com/blog
✅ Button 1 selesai - 2 URL ditemukan
...
💾 47 URL berhasil disimpan ke: backlinks_urls_example.com_buttonclick_1234567890.txt
```

### File Output
File `backlinks_urls_example.com_buttonclick_1234567890.txt`:
```
Backlink URLs untuk domain: example.com
Tanggal ekstraksi: 2024-01-15 14:30:25
Total URL: 47
Metode: Button-Link Click -> Nested Rows (Wait for URLs)
Mode: Headless
==================================================

1. https://authoritysite1.com/resource-page
2. https://blog.example2.com/industry-insights
3. https://news.site3.com/press-release
4. https://directory.site4.com/listing
...
```

## ⚙️ Konfigurasi

### Ukuran Browser (Jika Memilih Mode GUI)
```
1. Kecil (800x600)
2. Sedang (1024x768)  
3. Besar (1366x768)
4. Full HD (1920x1080)
5. Ukuran Custom
6. Default (default sistem)
```

## 🎯 Tips Penggunaan

### Mode Headless (Direkomendasikan)
```bash
# Jalankan dengan input otomatis
python moz_login.py
# Pilih: y untuk headless
```

**Keuntungan Mode Headless:**
- ⚡ **Kecepatan**: 3-5x lebih cepat
- 💾 **Efisiensi**: RAM usage 60-70% lebih rendah
- 🔋 **Performa**: CPU usage 40-50% lebih efisien
- 🎯 **Stabilitas**: Lebih konsisten untuk automation

### Mode GUI
```bash
# Untuk monitoring visual
python moz_login.py
# Pilih: n untuk GUI mode
```

**Kapan Menggunakan GUI:**
- 🔍 Debugging dan troubleshooting
- 👀 Monitoring proses secara visual
- 🎓 Learning dan understanding workflow

## 🔧 Troubleshooting

### Error Login
```
❌ LOGIN GAGAL!
💡 Silakan periksa kredensial Anda dan coba lagi
```
**Solusi**: Pastikan email dan password Moz.com benar

### Quota Habis
```
📊 Quota: 0 queries available this month
```
**Solusi**: Tunggu reset bulanan atau upgrade akun Moz

### Chrome Driver Error
```
❌ Gagal menyiapkan driver
```
**Solusi**: 
- Pastikan Chrome browser terinstall
- Update Chrome ke versi terbaru
- Restart script untuk auto-download driver

### Tidak Ada Data Backlink
```
⚠️ Tidak ada URL yang berhasil diekstrak
```
**Solusi**:
- Pastikan domain memiliki backlink data di Moz
- Tunggu halaman dimuat sepenuhnya
- Coba refresh dan analisis ulang

## 📊 Performa Benchmark

### Mode Headless vs GUI
| Metrik | Headless | GUI | Selisih |
|--------|----------|-----|---------|
| Waktu Login | 8 detik | 15 detik | **53% lebih cepat** |
| Analisis Domain | 12 detik | 25 detik | **52% lebih cepat** |
| Ekstraksi 50 URL | 45 detik | 90 detik | **50% lebih cepat** |
| RAM Usage | 150 MB | 400 MB | **62% lebih efisien** |
| CPU Usage | 15% | 35% | **57% lebih efisien** |

### Rekomendasi Sistem
- **Minimum**: 4GB RAM, Chrome browser
- **Optimal**: 8GB RAM, SSD storage
- **Mode Headless**: 2GB RAM sudah cukup

## ⚠️ Disclaimer

- Tool ini untuk tujuan edukasi dan research
- Pastikan mematuhi Terms of Service Moz.com
- Gunakan dengan bijak dan tidak berlebihan
- Saya tidak bertanggung jawab atas penyalahgunaan tool

## 🙏 Acknowledgments

- [Selenium](https://selenium.dev/) - Web automation framework
- [Undetected ChromeDriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) - Stealth Chrome automation
- [Colorama](https://github.com/tartley/colorama) - Terminal color output
- [Moz.com](https://moz.com/) - SEO tools platform

**⭐ Jika tool ini membantu, berikan star di GitHub repository!**

**Made with ❤️ by Dzone**
