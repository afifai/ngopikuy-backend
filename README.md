
# ☕ Kas Kopi Backend API

Backend sederhana untuk mencatat dan merekap **pemasukan & pengeluaran kas kopi** (atau kas komunitas).  
Dibangun dengan **Flask + SQLAlchemy + Flask-Migrate** dan siap digunakan dengan **SQLite** maupun **PostgreSQL (lokal / AWS RDS)**.

---

## 🚀 Fitur Utama
- 👥 **Manajemen Anggota**
- 💰 **Kas Bulanan**
- 🧾 **Pengeluaran**
- 🛒 **Belanja Anggota**
- 📊 **Rekapitulasi Bulanan & Keseluruhan**
- 📥 **Ekspor CSV**
- ❤️ **Health Check** (`/health`)

---

## ⚙️ Setup Project

### 1️⃣ Persiapan
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2️⃣ Konfigurasi `.env`
#### Default (SQLite)
```
FLASK_ENV=development
SECRET_KEY=dev-secret-change-me
SQLALCHEMY_DATABASE_URI=sqlite:///kas_kopi.db
```

#### PostgreSQL Lokal
```
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:password@localhost:5432/kas_kopi
```

#### PostgreSQL AWS RDS
```
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:password@kas-kopi.xxxxxx.ap-southeast-1.rds.amazonaws.com:5432/kas_kopi
```

---

## 🗃️ Migrasi Database
Gunakan perintah berikut untuk membuat dan memperbarui tabel:
```bash
python manage.py db init
python manage.py db migrate -m "init"
python manage.py db upgrade
```

---

## ▶️ Menjalankan Server
```bash
python app.py
```
Server akan berjalan di http://localhost:5000

---

## 📚 Endpoint Utama

| Method | Endpoint | Deskripsi |
|:------:|:----------|:-----------|
| GET | `/health` | Cek status API |
| GET/POST/PUT/DELETE | `/members` | CRUD anggota |
| GET/POST | `/cash` | Input & list kas bulanan |
| GET/POST | `/expenses` | Catat & lihat pengeluaran |
| GET/POST | `/purchases` | Input pembelian anggota |
| GET | `/summary/monthly` | Rekap bulanan (`?month=YYYY-MM`) |
| GET | `/summary/overall` | Rekap keseluruhan |
| GET | `/export/csv` | Ekspor CSV (`?month=YYYY-MM`) |

---

## ☁️ AWS RDS Setup Singkat
1. Buat instance RDS PostgreSQL di region terdekat (Jakarta/Singapura).
2. Catat endpoint dan credential.
3. Pastikan port 5432 terbuka untuk IP kamu / EC2.
4. Ubah `.env` sesuai endpoint RDS.
5. Jalankan `python manage.py db upgrade`.

Estimasi biaya (single-AZ, kecil): **$15–40/bulan (~Rp250–650rb)**.

---

## 📄 Lisensi
MIT License © 2025 — Afif Akbar Iskandar
