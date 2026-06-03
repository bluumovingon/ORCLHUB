# 🏁 Oracle Red Bull Racing Hub 🏁

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?style=flat-for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Framework](https://img.shields.io/badge/django-5.0%20%7C%206.0-092E20?style=flat-for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap styling](https://img.shields.io/badge/bootstrap-5.3-7952B3?style=flat-for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/license-MIT-red?style=flat-for-the-badge)](LICENSE)

Selamat datang di **Oracle Red Bull Racing Hub** — portal web interaktif Formula 1 yang dirancang khusus untuk penggemar dan kontributor tim Red Bull Racing. Aplikasi berbasis **Django** ini menghadirkan analisis sirkuit, info berita paddock terkini, galeri koleksi helm pembalap, serta panel manajemen hak akses (role authorization) terintegrasi untuk pengelolaan konten yang andal.

---

## 🚀 Fitur Utama

### 1. 🛡️ Role-Based Access Control (RBAC) & Authorization
Mekanisme pengamanan ketat menggunakan Django Groups yang membedakan hak akses pengguna menjadi tiga level utama:
*   **Admin**: Akses penuh ke seluruh sistem, Console Manajemen Pengguna, dan CRUD Kategori secara dinamis.
*   **Editor**: Memiliki akses untuk menulis, mengedit, dan menerbitkan artikel berita paddock.
*   **User (Member)**: Memiliki hak baca (read-only) untuk menjelajahi artikel, koleksi helm, dan berinteraksi di forum/portal.

### 2. 👥 User Management Console
Panel khusus Admin untuk mengelola status hak akses pengguna secara langsung dari antarmuka web:
*   Daftar pengguna terurut berdasarkan waktu registrasi terbaru.
*   Formulir interaktif untuk mengganti peran/grup (`Admin`, `Editor`, `User`).
*   Modifikasi status status `is_staff` dan `is_superuser` dengan validasi pencegahan penghapusan akun sendiri.

### 3. 🏷️ Dynamic Category CRUD
Kategori artikel yang dinamis dan disimpan langsung di database menggunakan relasi `ForeignKey` dan pengisian otomatis slug URL:
*   Admin dapat menambah, menyunting, dan menghapus kategori sirkuit/berita.
*   Menghitung jumlah artikel secara real-time di tiap kategori.
*   Dilengkapi peringatan sebelum penghapusan jika kategori masih berisi artikel (perlindungan integritas data).

### 4. ✍️ Press Room (Article CRUD)
Tempat menulis dan merilis artikel berita tim F1, analisis balapan, pembaruan teknis, dan opini fans. Dilengkapi fitur gambar sampul fallback dan ringkasan otomatis.

### 5. 🪖 Helmet Gallery
Koleksi desain helm pembalap ikonik Oracle Red Bull Racing lengkap dengan detail tahun, tipe sasis mobil, dan memori balapan yang berkesan.

---

## 🛠️ Tech Stack

*   **Backend**: Python, Django
*   **Database**: SQLite (default pengembangan)
*   **Frontend**: HTML5, Vanilla CSS (kustomisasi tema gelap premium), Bootstrap 5, FontAwesome Icons

---

## ⚙️ Cara Instalasi & Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek ini di lingkungan lokal Anda:

### 1. Clone Repositori
```bash
git clone https://github.com/username/Praktikum5Web.git
cd Praktikum5Web
```

### 2. Buat & Aktifkan Virtual Environment
```bash
# Untuk Windows
python -m venv myenv
myenv\Scripts\activate

# Untuk macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
# Atau instal Django secara manual jika berkas requirements.txt belum ada
pip install django
```

### 4. Jalankan Migrasi Database
Proyek dilengkapi dengan **otomatisasi pembuatan grup** (`Admin`, `Editor`, `User`) melalui sinyal `post_migrate`. Cukup jalankan perintah berikut:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Buat Superuser (Akun Admin)
```bash
python manage.py createsuperuser
```
*Ikuti instruksi di terminal untuk mengisi username, email, dan password.*

### 6. Jalankan Server Lokal
```bash
python manage.py runserver
```
Buka browser Anda dan akses aplikasi melalui [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 📂 Struktur Direktori Proyek

```text
Praktikum5Web/
├── accounts/               # Aplikasi Manajemen Akun & Autentikasi
│   ├── templatetags/       # Custom Template Filters (auth_extras.py)
│   └── templates/          # Halaman Login, Register, & Dashboard
├── artikel/                # Aplikasi Berita & Analisis Paddock
│   ├── templates/          # Halaman Artikel, User List, & Kategori CRUD
│   ├── models.py           # Model Artikel & Kategori
│   └── views.py            # Logika CRUD & Proteksi Role
├── galeri/                 # Aplikasi Galeri Helm Pembalap
├── f1_app/                 # Landing Page & Pengaturan Administratif
├── Praktikum5Web/          # Konfigurasi Utama Proyek (settings.py, urls.py)
└── manage.py               # Utilitas Command-line Django
```

---

## 🔒 Konfigurasi Keamanan (Template Tags Kustom)
Berkas `accounts/templatetags/auth_extras.py` memuat filter kustom untuk menangani keamanan UI:
*   `{% if request.user|is_admin %}`: Menampilkan elemen admin.
*   `{% if request.user|is_editor %}`: Memverifikasi hak cipta artikel.
*   `{% if request.user|is_regular_user %}`: Logika fallback untuk user biasa.

---

🏁 *Gasspolll! Sampai jumpa di grid start!* 🏁
