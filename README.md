# Aplikasi Review MCU Massal

Aplikasi berbasis web untuk memproses dan mereview data Medical Check-Up (MCU) massal menggunakan Python dan Streamlit.

## Fitur Aplikasi

- Mengunggah file Excel dengan data MCU mentah
- Memproses data sesuai dengan algoritma yang telah ditentukan
- Menampilkan hasil dalam format yang terstandarisasi
- Menyediakan opsi untuk mengunduh hasil yang telah diproses
- Menampilkan statistik pemrosesan dalam bentuk chart
- Filter hasil berdasarkan kategori kebugaran
- Menampilkan distribusi berdasarkan departemen

## Cara Menjalankan Aplikasi

### 1. Instalasi Dependensi

Pastikan Anda memiliki Python 3.7+ yang terinstal di sistem Anda. Kemudian instal dependensi yang diperlukan:

```bash
pip install -r requirements.txt
```

Atau instal secara manual:

```bash
pip install streamlit pandas numpy openpyxl xlsxwriter
```

### 2. Menjalankan Aplikasi

Jalankan aplikasi dengan perintah berikut:

```bash
streamlit run mcu_review_app.py
```

Setelah dijalankan, aplikasi akan terbuka di browser Anda (biasanya di alamat http://localhost:8501).

Alternatifnya, Anda juga bisa menjalankan:

```bash
./run_app.sh
```

### 3. Menggunakan Aplikasi

1. Gunakan panel di sebelah kiri untuk mengunggah file Excel dengan data MCU
2. Tunggu proses pemrosesan selesai
3. Lihat hasil pemrosesan dan statistiknya
4. Gunakan filter untuk melihat data berdasarkan kategori tertentu
5. Gunakan tombol "Unduh Hasil dalam Format Excel" untuk mengunduh hasilnya

## Struktur Data Input

Aplikasi ini mengasumsikan bahwa nama kolom dalam file input sesuai dengan yang disebutkan dalam spesifikasi. Jika nama kolom berbeda, Anda perlu menyesuaikan fungsi `map_columns` dalam file `mcu_review_app.py` sesuai dengan struktur data aktual Anda.

Kolom-kolom yang diharapkan meliputi:
- Identitas karyawan: NRP, NAMA KARYAWAN, UMUR, L/P, TIPE MCU, TGL. MCU
- Informasi pekerjaan: SITE / DEPARTEMEN, JABATAN
- Data antropometri: TB (cm), BB (Kg)
- Tanda vital: T. SISTOLE (input), T. DIASTOLE (input), Nadi /menit (input)
- Hasil laboratorium: HB, KOL, TG, HDL, LDL, GDP, HBA1C, UA, UREUM, CREAT, OT, PT
- Pemeriksaan medis: HBSAG, DRUGS, Rontgen (input), EKG (input), THT (input), SISSTEM GENITO UROVENEROLOGI (input)
- Informasi tambahan: Keluhan Alergi, KB. Merokok (input), BUTA WARNA
- Pemeriksaan mata: OD/OS TP KCMT, OD/OS KCMT
- Pemeriksaan gigi: Gigi Karies, Sisa Akar Gigi, Gigi Gangren
- Pemeriksaan fungsi paru dan pendengaran: SPIROMETRY, AUDIOMETRI, Anti HBs

## Lisensi

Aplikasi ini dikembangkan khusus untuk PT PPA BIB.