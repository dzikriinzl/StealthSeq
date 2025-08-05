# StealthSeq – Sequential Pattern Brute Forcer

**StealthSeq** adalah alat brute force yang dirancang untuk menghasilkan kombinasi password secara **dinamis** tanpa menggunakan wordlist. Fokus utama alat ini adalah pada **evasi deteksi**, **efisiensi**, dan **dukungan multi-protokol**, menjadikannya lebih stealthy dibandingkan alat brute force konvensional.

---

## 🔑 Fitur Utama

### 1. Tidak Menggunakan Wordlist
- Sebagian besar brute forcer seperti `hydra` atau `medusa` menggunakan file wordlist (misal: `rockyou.txt`).
- **StealthSeq** justru membangkitkan password secara **sequential** dari charset yang ditentukan pengguna.

### 2. Evasi Deteksi
- **Delay Acak:** Menambahkan jeda waktu antar percobaan.
- **Jitter:** Variasi tambahan pada delay untuk membuat traffic tampak alami.
- **Thread Terbatas:** Membatasi jumlah thread untuk menghindari deteksi oleh IDS/IPS.

### 3. Multi-Protokol
- **HTTP Basic Auth**
- **SSH**
- *(Dapat dikembangkan untuk FTP, RDP, dll)*  
Fokus pada layer aplikasi, bukan serangan jaringan seperti port scanning.

---

## ⚙️ Cara Kerja StealthSeq

### 1. Generate Pola Sequential
Menghasilkan kombinasi password dari charset yang ditentukan:

```text
Charset = abc123
Panjang min = 3, max = 4

Output:
aaa, aab, aac, aa1, aa2, aa3, aba, abb, ..., 3333
```

### 2. Delay + Jitter
Menghindari deteksi dengan waktu antar-percobaan yang tidak tetap:

```bash
Delay dasar: 0.5 detik
Jitter: ±0.3 detik
Total waktu: acak antara 0.2 – 0.8 detik
```
### 3. Multi-threading Terkontrol
Menggunakan ThreadPoolExecutor dengan jumlah thread yang terbatas agar tidak memicu sistem deteksi.

### 4. Dukungan Protokol
- HTTP Basic Auth → Login web
- SSH Brute Force → Server SSH
- FTP → (Planned)

# Contoh Penggunaan
## 1.  Brute Force HTTP Basic Auth
```bash
python3 stealthseq.py -t http://target.com/admin -p http -min 4 -max 6 -d 1.0 -j 0.5
```
- **-t:** Target URL
- **-p http:** Protokol HTTP
- **-min / -max:** Panjang password
- **-d:** Delay Dasar (detik)
- **-j:** Jitter

## 2. Brute Force SSH
```bash
python3 stealthseq.py -t target.com:2222 -p ssh -c "abcdef123456" -min 5 -max 5 -w 2
```
- **-t:** Target Host dan port
- **-p ssh:** Protokol HTTP
- **-c:** Charset
- **-min / -max:** Panjang password
- **-w:** Jumlah thread/worker

Disclaimer:
StealthSeq hanya untuk tujuan edukasi dan pengujian di lingkungan legal. Dilarang keras menggunakan alat ini untuk aktivitas yang melanggar hukum.

