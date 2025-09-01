Aplikasi Review MCU Massal
Saya akan membantu Anda membuat aplikasi untuk memproses dan mereview data Medical Check-Up (MCU) massal. Berikut adalah implementasi aplikasi berbasis web menggunakan Python dengan Streamlit.

Rencana Implementasi
Aplikasi ini akan:

Memungkinkan upload file Excel dengan data MCU mentah

Memproses data sesuai dengan algoritma yang Anda tentukan

Menampilkan hasil dalam format yang terstandarisasi

Menyediakan opsi untuk mengunduh hasil yang telah diproses

Menampilkan statistik pemrosesan

Kode Implementasi
python
import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime
import io
import re

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Review MCU Massal",
    page_icon="🏥",
    layout="wide"
)

# Judul aplikasi
st.title("🏥 Aplikasi Review MCU Massal")
st.markdown("Sistem otomatis untuk memproses dan menganalisis data Medical Check-Up (MCU) dari PT PPA BIB")

# Fungsi untuk memetakan kolom
def map_columns(df):
    # Inisialisasi dataframe hasil dengan kolom template
    template_columns = [
        'STATUS MCU MASUK', 'NIK', 'NAMA', 'PERUSAHAAN', 'DEPT', 'JABATAN',
        'UMUR', 'L/P', 'Tempat MCU', 'TANGGAL MCU', 'SISTOLE', 'DIASTOLE',
        'Nadi', 'TB', 'BB', 'BMI', 'Hb', 'Col (<250)', 'Trig (<230)', 'HDL',
        'LDL', 'GDP 70-115', 'HbA1c', 'AU 2,1-7,9', 'Ur(10-40)', 'Cre (0,6-1,3)',
        'SGOT(<40)', 'SGPT(<50)', 'ABNORMAL LAB', 'HbsAg', 'AntiHbs', 'Urin',
        'Narkoba', 'ALKOHOL TEST', 'Rotgen', 'EKG', 'MATA', 'GRADE/VISUS',
        'GIGI DAN MULUT', 'TELINGA', 'HEMOROID', 'ALERGI', 'KEBIASAAN MEROKOK',
        'ABNORMAL FISIK LAINNYA', 'BUTA WARNA', 'SPIROMETRY', 'SPIROMETRY_OBSTRUKTIF',
        'AUDIOMETRY', 'AUDIOMETRY_KANAN', 'TEMUAN', 'TEMUAN_1', 'TEMUAN_2',
        'TEMUAN_3', 'HASIL', 'Kesimpulan', 'MCU', 'Kategori', 'STATUS OPEN/CLOSE',
        'SISTOLE_1', 'DIASTOLE_1', 'CHOL', 'GDP', 'PETUGAS'
    ]
    
    result_df = pd.DataFrame(columns=template_columns)
    
    # Identity & Basic Data Mapping
    if 'NRP' in df.columns:
        result_df['NIK'] = df['NRP'].astype(str)
    if 'NAMA KARYAWAN' in df.columns:
        result_df['NAMA'] = df['NAMA KARYAWAN']
    if 'UMRU' in df.columns:
        result_df['UMUR'] = pd.to_numeric(df['UMRU'], errors='coerce')
    if 'L/P' in df.columns:
        result_df['L/P'] = df['L/P']
    if 'SITE / DEPARTEMEN' in df.columns:
        result_df['DEPT'] = df['SITE / DEPARTEMEN']
    if 'JABATAN' in df.columns:
        result_df['JABATAN'] = df['JABATAN']
    
    # MCU Information Mapping
    if 'TIPE MCU' in df.columns:
        result_df['STATUS MCU MASUK'] = df['TIPE MCU'].apply(
            lambda x: 'CALON KARYAWAN' if str(x).upper() == 'PRE EMPLOYE' else 'ANNUAL'
        )
    if 'TGL. MCU' in df.columns:
        result_df['TANGGAL MCU'] = pd.to_datetime(df['TGL. MCU'], errors='coerce').dt.strftime('%d/%m/%Y')
    
    # Vital Signs Mapping
    if 'TB (cm)' in df.columns:
        result_df['TB'] = pd.to_numeric(df['TB (cm)'], errors='coerce')
    if 'BB (Kg)' in df.columns:
        result_df['BB'] = pd.to_numeric(df['BB (Kg)'], errors='coerce')
    if 'T. SISTOLE (input)' in df.columns:
        result_df['SISTOLE'] = pd.to_numeric(df['T. SISTOLE (input)'], errors='coerce')
    if 'T. DIASTOLE (input)' in df.columns:
        result_df['DIASTOLE'] = pd.to_numeric(df['T. DIASTOLE (input)'], errors='coerce')
    if 'Nadi /menit (input)' in df.columns:
        result_df['Nadi'] = pd.to_numeric(df['Nadi /menit (input)'], errors='coerce')
    
    # Laboratory Values Mapping
    if 'HB 13 ~ 18 (input)' in df.columns:
        result_df['Hb'] = pd.to_numeric(df['HB 13 ~ 18 (input)'], errors='coerce')
    if 'KOL' in df.columns:
        result_df['Col (<250)'] = pd.to_numeric(df['KOL'], errors='coerce')
    if 'TG' in df.columns:
        result_df['Trig (<230)'] = pd.to_numeric(df['TG'], errors='coerce')
    if 'HDL' in df.columns:
        result_df['HDL'] = pd.to_numeric(df['HDL'], errors='coerce')
    if 'LDL' in df.columns:
        result_df['LDL'] = pd.to_numeric(df['LDL'], errors='coerce')
    if 'GDP' in df.columns:
        result_df['GDP 70-115'] = pd.to_numeric(df['GDP'], errors='coerce')
    if 'HBA1C' in df.columns:
        result_df['HbA1c'] = pd.to_numeric(df['HBA1C'], errors='coerce')
    if 'UA' in df.columns:
        result_df['AU 2,1-7,9'] = pd.to_numeric(df['UA'], errors='coerce')
    if 'UREUM (10-50)' in df.columns:
        result_df['Ur(10-40)'] = pd.to_numeric(df['UREUM (10-50)'], errors='coerce')
    if 'CREAT' in df.columns:
        result_df['Cre (0,6-1,3)'] = pd.to_numeric(df['CREAT'], errors='coerce')
    if 'OT' in df.columns:
        result_df['SGOT(<40)'] = pd.to_numeric(df['OT'], errors='coerce')
    if 'PT' in df.columns:
        result_df['SGPT(<50)'] = pd.to_numeric(df['PT'], errors='coerce')
    
    # Medical Examinations Mapping
    if 'HBSAG' in df.columns:
        result_df['HbsAg'] = df['HBSAG']
    if 'Anti HBs (input)' in df.columns:
        result_df['AntiHbs'] = df['Anti HBs (input)'].apply(
            lambda x: 'NON REAKTIF' if pd.to_numeric(x, errors='coerce') < 10 else 'REAKTIF'
        )
    if 'DRUGS' in df.columns:
        result_df['Narkoba'] = df['DRUGS'].apply(
            lambda x: 'NON REAKTIF' if str(x).lower() == 'negatif' else 'REAKTIF'
        )
    if 'Rontgen (input)' in df.columns:
        result_df['Rotgen'] = df['Rontgen (input)']
    if 'EKG (input)' in df.columns:
        result_df['EKG'] = df['EKG (input)']
    if 'THT (input)' in df.columns:
        result_df['TELINGA'] = df['THT (input)']
    if 'SISSTEM GENITO UROVENEROLOGI (input)' in df.columns:
        result_df['HEMOROID'] = df['SISSTEM GENITO UROVENEROLOGI (input)']
    if 'Keluhan Alergi (Sebutkan Alergi Apa)' in df.columns:
        result_df['ALERGI'] = df['Keluhan Alergi (Sebutkan Alergi Apa)']
    if 'KB. Merokok (input)' in df.columns:
        result_df['KEBIASAAN MEROKOK'] = df['KB. Merokok (input)']
    if 'BUTA WARNA (NEG/TOTAL/PARSIAL)' in df.columns:
        result_df['BUTA WARNA'] = df['BUTA WARNA (NEG/TOTAL/PARSIAL)']
    
    return result_df

# Algoritma analisis mata
def analyze_eyes(od_tp, os_tp, od_cmt, os_cmt):
    # MATA Analysis
    if pd.isna(od_tp) or pd.isna(os_tp):
        mata_result = "MIOPIA"
    elif od_tp == "6/6" and os_tp == "6/6":
        mata_result = "NORMAL"
    else:
        mata_result = "KELAINAN REFRAKSI"
    
    # GRADE/VISUS Analysis
    if pd.isna(od_cmt) or pd.isna(os_cmt):
        visus_result = "OD: N/A, OS: N/A"
    elif od_cmt == "6/6" and os_cmt == "6/6":
        visus_result = "TERKOREKSI"
    else:
        visus_result = f"OD: {od_cmt}, OS: {os_cmt}"
    
    return mata_result, visus_result

# Algoritma analisis gigi
def analyze_dental(karies, akar, gangren):
    # Helper function to check if a value indicates a condition
    def has_condition(value):
        if pd.isna(value):
            return False
        value_str = str(value).upper().strip()
        return value_str not in ["", "TIDAK", "NORMAL", "NEG", "NEGATIF"]
    
    has_karies = has_condition(karies)
    has_akar = has_condition(akar)
    has_gangren = has_condition(gangren)
    
    if has_gangren and has_akar:
        return "AKAR GIGI & GANGREN"
    elif has_gangren:
        return "GANGREN RADIX"
    elif has_karies and has_akar:
        return "CARIES DAN AKAR GIGI"
    elif has_akar:
        return "AKAR GIGI"
    elif has_karies:
        return "CARIES"
    else:
        return "NORMAL"

# Algoritma analisis spirometri
def analyze_spirometry(input_text):
    if pd.isna(input_text):
        return "NORMAL", "NORMAL"
    
    text = str(input_text).upper().strip()
    
    obstructive = "NORMAL"
    restrictive = "NORMAL"
    
    # Check for obstructive patterns
    if "OBSTRUKTIF" in text or "OBSTRUCTIVE" in text:
        if "RINGAN" in text or "MILD" in text:
            obstructive = "OBSTRUKTIF RINGAN"
        elif "SEDANG" in text or "MODERATE" in text:
            obstructive = "OBSTRUKTIF SEDANG"
        elif "BERAT" in text or "SEVERE" in text:
            obstructive = "OBSTRUKTIF BERAT"
        else:
            obstructive = "OBSTRUKTIF"
    
    # Check for restrictive patterns
    if "RESTRIKSI" in text or "RESTRICTIVE" in text:
        if "RINGAN" in text or "MILD" in text:
            restrictive = "RESTRIKSI RINGAN"
        elif "SEDANG" in text or "MODERATE" in text:
            restrictive = "RESTRIKSI SEDANG"
        elif "BERAT" in text or "SEVERE" in text:
            restrictive = "RESTRIKSI BERAT"
        else:
            restrictive = "RESTRIKSI"
    
    # If no patterns found but text exists
    if obstructive == "NORMAL" and restrictive == "NORMAL" and text != "":
        restrictive = text
    
    return restrictive, obstructive

# Algoritma analisis audiometri
def analyze_audiometry(input_text):
    if pd.isna(input_text):
        return "NORMAL", "NORMAL"
    
    text = str(input_text).upper().strip()
    
    def classify_hearing_loss(part):
        if pd.isna(part) or part == "":
            return "NORMAL"
        part_str = str(part).upper()
        if "RINGAN" in part_str or "MILD" in part_str:
            return "GANGGUAN PENDENGARAN RINGAN"
        elif "SEDANG" in part_str or "MODERATE" in part_str:
            return "GANGGUAN PENDENGARAN SEDANG"
        elif "BERAT" in part_str or "SEVERE" in part_str:
            return "GANGGUAN PENDENGARAN BERAT"
        elif "GANGGUAN" in part_str or "TULI" in part_str:
            return "GANGGUAN PENDENGARAN"
        else:
            return part_str
    
    left = "NORMAL"
    right = "NORMAL"
    
    # Simple text-based extraction
    if "KIRI" in text or "LEFT" in text:
        if "KANAN" in text or "RIGHT" in text:
            # Both ears mentioned
            parts = re.split(r"KANAN|RIGHT", text)
            if len(parts) > 0:
                left_part = parts[0]
                left = classify_hearing_loss(left_part)
            if len(parts) > 1:
                right_part = parts[1]
                right = classify_hearing_loss(right_part)
        else:
            # Only left ear mentioned
            left = classify_hearing_loss(text)
    elif "KANAN" in text or "RIGHT" in text:
        # Only right ear mentioned
        right = classify_hearing_loss(text)
    else:
        # General condition
        result = classify_hearing_loss(text)
        left = result
        right = result
    
    return left, right

# Algoritma analisis laboratorium abnormal
def analyze_abnormal_lab(row):
    findings = []
    
    # Check cholesterol
    if not pd.isna(row.get('Col (<250)', np.nan)) and row['Col (<250)'] >= 250:
        findings.append("Kolesterol tinggi")
    
    # Check triglycerides
    if not pd.isna(row.get('Trig (<230)', np.nan)) and row['Trig (<230)'] >= 230:
        findings.append("Trigliserida tinggi")
    
    # Check blood glucose
    if not pd.isna(row.get('GDP 70-115', np.nan)):
        gdp = row['GDP 70-115']
        if gdp < 70 or gdp > 115:
            findings.append("Gula darah abnormal")
    
    # Check SGOT
    if not pd.isna(row.get('SGOT(<40)', np.nan)) and row['SGOT(<40)'] >= 40:
        findings.append("SGOT tinggi")
    
    # Check SGPT
    if not pd.isna(row.get('SGPT(<50)', np.nan)) and row['SGPT(<50)'] >= 50:
        findings.append("SGPT tinggi")
    
    return "; ".join(findings) if findings else "NORMAL"

# Algoritma kategorisasi kebugaran
def categorize_fitness(row):
    lab_abnormal = row.get('ABNORMAL LAB', 'NORMAL') != 'NORMAL'
    
    # Check physical abnormalities
    physical_abnormalities = 0
    
    if row.get('MATA', 'NORMAL') != 'NORMAL':
        physical_abnormalities += 1
    
    if row.get('GIGI DAN MULUT', 'NORMAL') != 'NORMAL':
        physical_abnormalities += 1
    
    if row.get('SPIROMETRY', 'NORMAL') != 'NORMAL':
        physical_abnormalities += 1
    
    if row.get('SPIROMETRY_OBSTRUKTIF', 'NORMAL') != 'NORMAL':
        physical_abnormalities += 1
    
    if row.get('AUDIOMETRY', 'NORMAL') != 'NORMAL':
        physical_abnormalities += 1
    
    if row.get('AUDIOMETRY_KANAN', 'NORMAL') != 'NORMAL':
        physical_abnormalities += 1
    
    # Check other physical findings
    other_findings = [
        row.get('TELINGA', ''),
        row.get('HEMOROID', ''),
        row.get('ALERGI', ''),
        row.get('BUTA WARNA', '')
    ]
    
    for finding in other_findings:
        if not pd.isna(finding) and str(finding).upper() not in ['', 'NORMAL', 'NEG', 'NEGATIF']:
            physical_abnormalities += 1
            break
    
    # Determine fitness category
    if not lab_abnormal and physical_abnormalities == 0:
        return "FIT"
    elif lab_abnormal and physical_abnormalities == 0:
        return "FIT WITH NOTE"
    else:
        return "NOT FIT"

# Fungsi utama untuk memproses data
def process_mcu_data(df):
    # Pemetaan kolom dasar
    result_df = map_columns(df)
    
    # Hitung BMI
    if 'TB' in result_df.columns and 'BB' in result_df.columns:
        result_df['BMI'] = result_df.apply(
            lambda row: row['BB'] / ((row['TB'] / 100) ** 2) if not pd.isna(row['TB']) and row['TB'] > 0 and not pd.isna(row['BB']) else np.nan,
            axis=1
        )
    
    # Terapkan algoritma analisis mata
    if all(col in df.columns for col in ['OD (TP KCMT) (input)', 'OS (TP KCMT) (input)', 'OD (KCMT) (input)', 'OS (KCMT) (input)']):
        eye_results = df.apply(
            lambda row: analyze_eyes(
                row['OD (TP KCMT) (input)'],
                row['OS (TP KCMT) (input)'],
                row['OD (KCMT) (input)'],
                row['OS (KCMT) (input)']
            ), axis=1
        )
        result_df['MATA'] = [r[0] for r in eye_results]
        result_df['GRADE/VISUS'] = [r[1] for r in eye_results]
    
    # Terapkan algoritma analisis gigi
    if all(col in df.columns for col in ['Gigi Karies (input)', 'Sisa Akar Gigi (input)', 'Gigi Gangren (input)']):
        result_df['GIGI DAN MULUT'] = df.apply(
            lambda row: analyze_dental(
                row['Gigi Karies (input)'],
                row['Sisa Akar Gigi (input)'],
                row['Gigi Gangren (input)']
            ), axis=1
        )
    
    # Terapkan algoritma analisis spirometri
    if 'SPIROMETRY (input)' in df.columns:
        spirometry_results = df['SPIROMETRY (input)'].apply(analyze_spirometry)
        result_df['SPIROMETRY'] = [r[0] for r in spirometry_results]
        result_df['SPIROMETRY_OBSTRUKTIF'] = [r[1] for r in spirometry_results]
    
    # Terapkan algoritma analisis audiometri
    if 'AUDIOMETRI (input)' in df.columns:
        audiometry_results = df['AUDIOMETRI (input)'].apply(analyze_audiometry)
        result_df['AUDIOMETRY'] = [r[0] for r in audiometry_results]
        result_df['AUDIOMETRY_KANAN'] = [r[1] for r in audiometry_results]
    
    # Terapkan algoritma analisis laboratorium abnormal
    result_df['ABNORMAL LAB'] = result_df.apply(analyze_abnormal_lab, axis=1)
    
    # Terapkan algoritma kategorisasi kebugaran
    result_df['Kategori'] = result_df.apply(categorize_fitness, axis=1)
    
    # Isi kolom default
    result_df['PERUSAHAAN'] = 'PT PPA BIB'
    result_df['Tempat MCU'] = 'Klinik Perusahaan'
    
    return result_df

# Fungsi untuk menghasilkan statistik
def generate_statistics(result_df):
    total_records = len(result_df)
    fit_count = len(result_df[result_df['Kategori'] == 'FIT'])
    fit_with_note_count = len(result_df[result_df['Kategori'] == 'FIT WITH NOTE'])
    not_fit_count = len(result_df[result_df['Kategori'] == 'NOT FIT'])
    
    return {
        "summary": {
            "total_records": total_records,
            "fit_count": fit_count,
            "fit_percentage": round((fit_count / total_records * 100), 1) if total_records > 0 else 0,
            "fit_with_note_count": fit_with_note_count,
            "fit_with_note_percentage": round((fit_with_note_count / total_records * 100), 1) if total_records > 0 else 0,
            "not_fit_count": not_fit_count,
            "not_fit_percentage": round((not_fit_count / total_records * 100), 1) if total_records > 0 else 0
        },
        "processing_info": {
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processing_time_seconds": 0,  # Would be calculated in a real implementation
            "success_rate": 100  # Would be calculated based on successful processing
        }
    }

# Antarmuka pengguna
def main():
    st.sidebar.header("Unggah Data MCU")
    uploaded_file = st.sidebar.file_uploader("Pilih file Excel", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Baca file Excel
            df = pd.read_excel(uploaded_file)
            
            # Tampilkan preview data
            st.subheader("Preview Data Mentah")
            st.dataframe(df.head())
            
            # Proses data
            with st.spinner("Memproses data MCU..."):
                result_df = process_mcu_data(df)
                statistics = generate_statistics(result_df)
            
            # Tampilkan hasil
            st.subheader("Hasil Pemrosesan Data MCU")
            st.dataframe(result_df)
            
            # Tampilkan statistik
            st.subheader("Statistik Pemrosesan")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Records", statistics['summary']['total_records'])
            col2.metric("FIT", f"{statistics['summary']['fit_count']} ({statistics['summary']['fit_percentage']}%)")
            col3.metric("NOT FIT", f"{statistics['summary']['not_fit_count']} ({statistics['summary']['not_fit_percentage']}%)")
            
            # Tampilkan chart distribusi kategori
            chart_data = pd.DataFrame({
                'Kategori': ['FIT', 'FIT WITH NOTE', 'NOT FIT'],
                'Jumlah': [
                    statistics['summary']['fit_count'],
                    statistics['summary']['fit_with_note_count'],
                    statistics['summary']['not_fit_count']
                ]
            })
            st.bar_chart(chart_data.set_index('Kategori'))
            
            # Opsi untuk mengunduh hasil
            st.subheader("Unduh Hasil")
            output_filename = st.text_input("Nama file output", "hasil_mcu_terproses.xlsx")
            
            # Konversi ke Excel untuk diunduh
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                result_df.to_excel(writer, index=False, sheet_name='Hasil MCU')
                
                # Tambahkan sheet dengan statistik
                stats_df = pd.DataFrame.from_dict(statistics['summary'], orient='index', columns=['Nilai'])
                stats_df.to_excel(writer, sheet_name='Statistik')
            
            st.download_button(
                label="Unduh Hasil dalam Format Excel",
                data=output.getvalue(),
                file_name=output_filename,
                mime="application/vnd.ms-excel"
            )
            
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses file: {str(e)}")
    else:
        st.info("Silakan unggah file Excel data MCU menggunakan panel di sebelah kiri.")

if __name__ == "__main__":
    main()
Cara Menjalankan Aplikasi
Simpan kode di atas dalam file bernama mcu_review_app.py

Install dependensi yang diperlukan:

text
pip install streamlit pandas numpy openpyxl xlsxwriter
Jalankan aplikasi dengan perintah:

text
streamlit run mcu_review_app.py
Buka browser dan akses alamat yang ditampilkan (biasanya http://localhost:8501)

Fitur Aplikasi
Unggah Data: Memungkinkan pengguna mengunggah file Excel dengan data MCU mentah

Pemrosesan Otomatis:

Memetakan kolom dari format sumber ke format template

Menerapkan algoritma analisis medis (mata, gigi, spirometri, audiometri)

Mengidentifikasi hasil laboratorium yang abnormal

Mengkategorikan kebugaran karyawan (FIT, FIT WITH NOTE, NOT FIT)

Visualisasi Data: Menampilkan statistik dan chart distribusi kategori kebugaran

Ekspor Hasil: Memungkinkan pengunduhan hasil dalam format Excel

Catatan Implementasi
Aplikasi ini mengasumsikan bahwa nama kolom dalam file input sesuai dengan yang disebutkan dalam spesifikasi. Jika nama kolom berbeda, Anda mungkin perlu menyesuaikan fungsi map_columns sesuai dengan struktur data aktual Anda.

Aplikasi ini dapat diperluas dengan menambahkan lebih banyak validasi data, penanganan kesalahan yang lebih robust, dan opsi konfigurasi tambahan sesuai kebutuhan.