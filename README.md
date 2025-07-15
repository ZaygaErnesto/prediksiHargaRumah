# 🏠 Dashboard Analisis Properti Yogyakarta

Dasbor interaktif yang dibangun menggunakan Streamlit untuk menganalisis data properti (rumah) di wilayah Daerah Istimewa Yogyakarta. Aplikasi ini memvisualisasikan berbagai aspek data seperti harga, luas, dan distribusi geografis untuk memberikan wawasan mendalam kepada pengguna.

Data yang digunakan dalam proyek ini diambil dari situs `Rumah123.com` dan telah melalui proses pembersihan.

<img width="1919" height="969" alt="image" src="https://github.com/user-attachments/assets/bb2ea527-7423-45b8-b111-7e7ca9dea18b" />
<img width="1919" height="972" alt="image" src="https://github.com/user-attachments/assets/a2da190c-44a1-4011-9e70-c3e16df068f4" />

## ✨ Fitur Utama

-   **Filter Interaktif**: Filter data properti berdasarkan Kabupaten/Kota (Sleman, Bantul, Gunungkidul, Kulon Progo, Kota Yogyakarta).
-   **Ringkasan Statistik**: Tampilkan metrik utama seperti rata-rata harga, median harga, harga minimum/maksimum, rata-rata luas tanah, dan total properti yang terdaftar.
-   **Visualisasi Data Komprehensif**:
    -   **Distribusi Harga**: Histogram untuk melihat sebaran harga properti.
    -   **Perbandingan Harga per Lokasi**: Boxplot untuk membandingkan rentang harga di setiap kabupaten/kota.
    -   **Jumlah Properti**: Bar chart yang menunjukkan jumlah properti di setiap lokasi.
    -   **Proporsi Properti**: Pie chart untuk melihat persentase properti di setiap lokasi.
    -   **Hubungan Harga dan Luas**: Scatter plot interaktif untuk menganalisis korelasi antara harga dengan luas tanah atau luas bangunan.
    -   **Distribusi Kamar**: Bar chart untuk jumlah kamar tidur dan kamar mandi.
    -   **Matriks Korelasi**: Heatmap untuk melihat korelasi antara variabel numerik seperti harga, luas, dan jumlah kamar.
-   **Tampilan Data Mentah**: Opsi untuk melihat dan menelusuri data mentah dalam bentuk tabel.

---

## 🛠️ Teknologi yang Digunakan

-   **Python**: Bahasa pemrograman utama.
-   **Streamlit**: Framework untuk membangun aplikasi web data.
-   **Pandas**: Untuk manipulasi dan analisis data.
-   **Plotly**: Untuk membuat visualisasi data yang interaktif.

---

## 🚀 Cara Menjalankan Proyek Secara Lokal

Untuk menjalankan dasbor ini di komputer Anda, ikuti langkah-langkah berikut:

1.  **Clone Repository**
    ```bash
    git clone [URL-repository-Anda]
    cd [nama-folder-repository]
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    Disarankan untuk menggunakan virtual environment agar dependensi proyek tidak tercampur dengan instalasi Python global Anda.
    ```bash
    # Buat venv
    python -m venv .venv

    # Aktifkan venv (Windows)
    .\.venv\Scripts\activate

    # Aktifkan venv (macOS/Linux)
    source .venv/bin/activate
    ```

3.  **Install Dependensi**
    Pastikan Anda memiliki file `requirements.txt` yang berisi semua paket yang dibutuhkan.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Streamlit**
    Pastikan file data `rumah123_yogya_cleaned.csv` berada di direktori yang sama dengan `app.py`.
    ```bash
    streamlit run app.py
    ```
    Aplikasi akan terbuka secara otomatis di browser Anda.

---

## 📂 Struktur File

```
.
├── app.py                      # Kode utama aplikasi Streamlit
├── rumah123_yogya_cleaned.csv  # Dataset properti
├── requirements.txt            # Daftar dependensi Python
└── README.md                   # File ini
```
