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
        'Narkoba', 'ALKOHOL TEST', 'Rotgen', 'ABNORMAL RONTGEN', 'EKG', 'ABNORMAL EKG', 'MATA', 'GRADE/VISUS',
        'GIGI DAN MULUT', 'TELINGA', 'HEMOROID', 'ALERGI', 'KEBIASAAN MEROKOK',
        'ABNORMAL FISIK LAINNYA', 'BUTA WARNA', 'BUTA WARNA_hasil', 'SPIROMETRY', 'SPIROMETRY_OBSTRUKTIF',
        'AUDIOMETRY', 'AUDIOMETRY_KANAN'
    ]
    
    result_df = pd.DataFrame(columns=template_columns)
    
    # Identity & Basic Data Mapping
    if 'NRP' in df.columns:
        result_df['NIK'] = df['NRP'].astype(str)
    if 'NAMA KARYAWAN' in df.columns:
        result_df['NAMA'] = df['NAMA KARYAWAN']
    # Handle UMUR column with more robust approach
    umur_columns = ['UMRU', 'UMUR', 'Usia', 'Umur']  # Common variations
    for col in umur_columns:
        if col in df.columns:
            result_df['UMUR'] = pd.to_numeric(df[col], errors='coerce')
            break
    else:
        # If no age column found, try to extract from other columns
        for col in df.columns:
            if 'umur' in col.lower() or 'usia' in col.lower():
                result_df['UMUR'] = pd.to_numeric(df[col], errors='coerce')
                break
    
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
        def process_hbsag(value):
            if pd.isna(value):
                return 'NON REAKTIF'
            
            # Convert to string and uppercase for comparison
            val_str = str(value).upper().strip()
            
            # Define positive indicators
            positive_indicators = ['POSITIF', 'POSITIVE', 'REACTION', 'REACTIVE', '+', 'YA', 'YES']
            
            # Define negative indicators
            negative_indicators = ['NEGATIF', 'NEGATIVE', 'NON REACTIVE', '-', 'TIDAK', 'NO', 'NEG']
            
            # Check for positive indicators
            if any(indicator in val_str for indicator in positive_indicators):
                return 'REAKTIF'
            
            # Check for negative indicators
            if any(indicator in val_str for indicator in negative_indicators):
                return 'NON REAKTIF'
            
            # If numeric value, consider positive if >= 1
            try:
                numeric_val = pd.to_numeric(value, errors='coerce')
                if not pd.isna(numeric_val) and numeric_val >= 1:
                    return 'REAKTIF'
            except:
                pass
            
            # Default to NON REAKTIF if no clear indication
            return 'NON REAKTIF'
        
        result_df['HbsAg'] = df['HBSAG'].apply(process_hbsag)
    if 'Anti HBs (input)' in df.columns:
        result_df['AntiHbs'] = df['Anti HBs (input)'].apply(
            lambda x: 'NON REAKTIF' if pd.to_numeric(x, errors='coerce') < 10 else 'REAKTIF'
        )
    if 'DRUGS' in df.columns:
        def process_drugs(value):
            if pd.isna(value):
                return ''  # Kosongkan jika NaN
            
            # Convert to string and uppercase for comparison
            val_str = str(value).upper().strip()
            
            # Handle empty or dash values
            if val_str in ['', '-', 'NONE', 'NULL', 'NIL']:
                return ''  # Kosongkan
            
            # Define positive indicators
            positive_indicators = ['POSITIF', 'POSITIVE', '+', 'YA', 'YES']
            
            # Define negative indicators
            negative_indicators = ['NEGATIF', 'NEGATIVE', '-', 'TIDAK', 'NO', 'NEG']
            
            # Check for positive indicators
            if any(indicator in val_str for indicator in positive_indicators):
                return 'POSITIF'
            
            # Check for negative indicators
            if any(indicator in val_str for indicator in negative_indicators):
                return 'NEGATIF'
            
            # Default to NEGATIF if no clear indication
            return 'NEGATIF'
        
        result_df['Narkoba'] = df['DRUGS'].apply(process_drugs)
    
    # Process ALKOHOL TEST column if it exists in source data
    alcohol_columns = ['ALKOHOL TEST', 'ALCOHOL TEST', 'ETILIK', 'ALKOHOL']  # Common variations
    for col in alcohol_columns:
        if col in df.columns:
            def process_alcohol(value):
                if pd.isna(value):
                    return ''  # Kosongkan jika NaN
                
                # Convert to string and uppercase for comparison
                val_str = str(value).upper().strip()
                
                # Handle empty or dash values
                if val_str in ['', '-', 'NONE', 'NULL', 'NIL']:
                    return ''  # Kosongkan
                
                # Define positive indicators
                positive_indicators = ['POSITIF', 'POSITIVE', '+', 'YA', 'YES']
                
                # Define negative indicators
                negative_indicators = ['NEGATIF', 'NEGATIVE', '-', 'TIDAK', 'NO', 'NEG']
                
                # Check for positive indicators
                if any(indicator in val_str for indicator in positive_indicators):
                    return 'POSITIF'
                
                # Check for negative indicators
                if any(indicator in val_str for indicator in negative_indicators):
                    return 'NEGATIF'
                
                # Default to NEGATIF if no clear indication
                return 'NEGATIF'
            
            result_df['ALKOHOL TEST'] = df[col].apply(process_alcohol)
            break
    if 'Rontgen (input)' in df.columns:
        def process_rontgen(value):
            if pd.isna(value):
                return ''  # Kosongkan jika NaN
            
            # Convert to string and strip whitespace
            val_str = str(value).strip().upper()
            
            # Handle empty values
            if val_str in ['', '-', 'NO TEST', 'NO_TEST', 'NONE', 'NULL', 'N/A', 'TIDAK ADA', 'TIDAK']:
                return ''  # Kosongkan
            
            # Hanya izinkan nilai NORMAL atau ABNORMAL
            if 'ABNORMAL' in val_str or 'ABN' in val_str:
                return 'ABNORMAL'
            else:
                return 'NORMAL'
        
        result_df['Rotgen'] = df['Rontgen (input)'].apply(process_rontgen)
    if 'EKG (input)' in df.columns:
        def process_ekg_data(value):
            if pd.isna(value):
                return '', ''  # Kosongkan jika NaN
            
            # Convert to string and strip whitespace
            val_str = str(value).strip()
            
            # Handle empty values or indicators of no test
            if val_str.upper() in ['', '-', 'NO TEST', 'NO_TEST', 'NONE', 'NULL', 'N/A', 'TIDAK ADA']:
                return '', ''  # Kosongkan
            
            # Check if it's abnormal - more comprehensive detection
            val_upper = val_str.upper()
            is_abnormal = (
                'ABNORMAL' in val_upper or 
                'ABN' in val_upper or 
                'ABNORMALITAS' in val_upper or
                val_upper in ['ABNORMAL', 'ABN', 'POSITIVE', 'POS', 'POSITIF', 'REACTION', 'REACTIVE', '+', 'YA']
            )
            
            if is_abnormal:
                # Jika abnormal, EKG = "ABNORMAL", ABNORMAL EKG = nilai asli
                return 'ABNORMAL', val_str
            elif val_upper in ['NORMAL', 'NORM', 'NEGATIVE', 'NEG', 'NEGATIF', '-', 'NO', 'TIDAK']:
                # Jika normal, EKG = "NORMAL", ABNORMAL EKG = kosong
                return 'NORMAL', ''
            else:
                # Untuk kasus lain, periksa apakah ada indikasi abnormal
                # Jika ada teks yang bukan indikator normal, anggap sebagai abnormal
                if val_upper not in ['NORMAL', 'NORM']:
                    return 'ABNORMAL', val_str
                else:
                    return 'NORMAL', ''
        
        # Apply processing to EKG data
        ekg_results = df['EKG (input)'].apply(process_ekg_data)
        result_df['EKG'] = [r[0] for r in ekg_results]
        result_df['ABNORMAL EKG'] = [r[1] for r in ekg_results]
    if 'THT (input)' in df.columns:
        def process_telinga(value):
            if pd.isna(value):
                return ''  # Kosongkan jika NaN
            
            # Convert to string and strip whitespace
            val_str = str(value).strip()
            
            # Handle empty values
            if val_str.upper() in ['', '-', 'NONE', 'NULL', 'N/A', 'TIDAK ADA']:
                return ''  # Kosongkan
            
            # Ganti "Serumen ADS" dengan "SERUMEN PROP"
            if val_str.upper() == 'SERUMEN ADS':
                return 'SERUMEN PROP'
            
            # Ubah ke UPPERCASE
            return val_str.upper()
        
        result_df['TELINGA'] = df['THT (input)'].apply(process_telinga)
    if 'SISSTEM GENITO UROVENEROLOGI (input)' in df.columns:
        def process_hemoroid(value):
            if pd.isna(value):
                return ''  # Kosongkan jika NaN
            
            # Convert to string and strip whitespace
            val_str = str(value).strip().upper()
            
            # Handle empty values
            if val_str in ['', '-', 'NONE', 'NULL', 'N/A', 'TIDAK ADA']:
                return ''  # Kosongkan
            
            # Kriteria yang diperbolehkan (dengan variasi penulisan)
            allowed_values = [
                'NORMAL', 'GRADE 1', 'GRADE 2', 'GRADE 3', 'GRADE 4', 
                'MENOLAK RT', 'EKSTERNAL', 'POLIP RECTUM', 'INTERNAL',
                'HEMOROID EKSTERNA GR 1', 'HEMOROID EKSTERNA GR 2',
                'HEMOROID INTERNA GR 1', 'HEMOROID INTERNA GR 2',
                'HEMOROID EKSTERNAL', 'HEMOROID INTERNAL',
                'FISTULA ANI', 'FISTEL ANI', 'FISTEL', 'ABNORMAL',
                'HEMOROID', 'ABN'
            ]
            
            # Cek apakah nilai mengandung salah satu dari kriteria yang diperbolehkan
            for allowed in allowed_values:
                if allowed in val_str:
                    return val_str  # Return original value if it contains allowed terms
            
            # Jika tidak mengandung istilah yang diperbolehkan, kosongkan
            return ''
        
        result_df['HEMOROID'] = df['SISSTEM GENITO UROVENEROLOGI (input)'].apply(process_hemoroid)
    if 'Keluhan Alergi (Sebutkan Alergi Apa)' in df.columns:
        def process_alergi(value):
            if pd.isna(value):
                return ''  # Kosongkan jika NaN
            
            # Convert to string and strip whitespace
            val_str = str(value).strip()
            
            # Return value as is (in uppercase) - even if it appears to be negative
            return val_str.upper()
        
        result_df['ALERGI'] = df['Keluhan Alergi (Sebutkan Alergi Apa)'].apply(process_alergi)
    if 'KB. Merokok (input)' in df.columns:
        def process_smoking(value):
            if pd.isna(value):
                return ''
            
            # Convert to string and standardize
            val_str = str(value).strip().upper()
            
            # Handle empty or dash values
            if val_str in ['', '-', 'NONE', 'NULL', 'NIL']:
                return ''
            
            # Handle numeric values (0 = TIDAK, non-zero = YA)
            try:
                numeric_val = pd.to_numeric(value, errors='coerce')
                if not pd.isna(numeric_val):
                    if numeric_val == 0:
                        return 'TIDAK'
                    else:
                        return 'YA'
            except:
                pass
            
            # Handle various positive indicators
            positive_indicators = ['YA', 'IYA', 'YES', 'POSITIF', '+', 'MEROKOK']
            
            # Handle various negative indicators
            negative_indicators = ['TIDAK', 'NO', 'NEGATIF', '-', 'TIDAK MEROKOK']
            
            # Check for positive indicators
            if any(indicator in val_str for indicator in positive_indicators):
                return 'YA'
            
            # Check for negative indicators
            if any(indicator in val_str for indicator in negative_indicators):
                return 'TIDAK'
            
            # Default to TIDAK if no clear indication
            return 'TIDAK'
        
        result_df['KEBIASAAN MEROKOK'] = df['KB. Merokok (input)'].apply(process_smoking)
    if 'BUTA WARNA (NEG/TOTAL/PARSIAL)' in df.columns:
        def process_color_vision(value):
            if pd.isna(value):
                return '', ''  # Return empty for both columns if NaN
            
            # Convert to string and strip whitespace
            val_str = str(value).strip().upper()
            
            # Handle empty values
            if val_str in ['', '-', 'NONE', 'NULL', 'N/A', 'TIDAK ADA']:
                return '', ''
            
            # Map values to appropriate categories
            if val_str in ['NEG', 'NEGATIF', 'NORMAL', 'N']:
                return 'NORMAL', 'NORMAL'
            elif val_str in ['PARSIAL', 'P', 'SEBAGIAN']:
                return 'PARSIAL', 'PARSIAL'
            elif val_str in ['TOTAL', 'T', 'SEMPURNA']:
                return 'TOTAL', 'TOTAL'
            else:
                # For any other values, return the original value in the detail column
                return val_str, val_str
        
        # Process BUTA WARNA column
        color_vision_results = df['BUTA WARNA (NEG/TOTAL/PARSIAL)'].apply(process_color_vision)
        result_df['BUTA WARNA'] = [r[0] for r in color_vision_results]  # Main result
        # Add new column for detailed results
        if 'BUTA WARNA_hasil' not in result_df.columns:
            result_df.insert(
                result_df.columns.get_loc('BUTA WARNA') + 1, 
                'BUTA WARNA_hasil', 
                [r[1] for r in color_vision_results]
            )
    
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
        return value_str not in ["", "TIDAK", "NORMAL", "NEG", "NEGATIF", "-"]
    
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
    
    # Check Ureum
    if not pd.isna(row.get('Ur(10-40)', np.nan)):
        ureum = row['Ur(10-40)']
        if ureum < 10 or ureum > 40:
            findings.append("Ureum abnormal")
    
    # Check Creatinine
    if not pd.isna(row.get('Cre (0,6-1,3)', np.nan)):
        creat = row['Cre (0,6-1,3)']
        if creat < 0.6 or creat > 1.3:
            findings.append("Creatinine abnormal")
    
    # Check Hemoglobin
    if not pd.isna(row.get('Hb', np.nan)):
        hb = row['Hb']
        # Normal range for men: 13-18, women: 12-16
        gender = row.get('L/P', '').lower() if not pd.isna(row.get('L/P', '')) else ''
        if 'perempuan' in gender or 'wanita' in gender:
            if hb < 12 or hb > 16:
                findings.append("Hemoglobin abnormal")
        else:  # Assume male if not specified as female
            if hb < 13 or hb > 18:
                findings.append("Hemoglobin abnormal")
    
    return "; ".join(findings) if findings else "NORMAL"

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
        
        # Kosongkan GRADE/VISUS jika hasilnya "OD: N/A, OS: N/A"
        result_df['GRADE/VISUS'] = result_df['GRADE/VISUS'].apply(
            lambda x: '' if x == "OD: N/A, OS: N/A" else x
        )
    else:
        # Cek kolom alternatif untuk mata
        od_tp_cols = ['OD_TP', 'OD_TP_KCMT', 'VISUS_OD']
        os_tp_cols = ['OS_TP', 'OS_TP_KCMT', 'VISUS_OS']
        od_cmt_cols = ['OD_CMT', 'OD_KCMT', 'VISUS_OD_CMT']
        os_cmt_cols = ['OS_CMT', 'OS_KCMT', 'VISUS_OS_CMT']
        
        od_tp_col, os_tp_col, od_cmt_col, os_cmt_col = None, None, None, None
        
        for col in od_tp_cols:
            if col in df.columns:
                od_tp_col = col
                break
                
        for col in os_tp_cols:
            if col in df.columns:
                os_tp_col = col
                break
                
        for col in od_cmt_cols:
            if col in df.columns:
                od_cmt_col = col
                break
                
        for col in os_cmt_cols:
            if col in df.columns:
                os_cmt_col = col
                break
        
        if all(col is not None for col in [od_tp_col, os_tp_col, od_cmt_col, os_cmt_col]):
            eye_results = df.apply(
                lambda row: analyze_eyes(
                    row[od_tp_col],
                    row[os_tp_col],
                    row[od_cmt_col],
                    row[os_cmt_col]
                ), axis=1
            )
            result_df['MATA'] = [r[0] for r in eye_results]
            result_df['GRADE/VISUS'] = [r[1] for r in eye_results]
            
            # Kosongkan GRADE/VISUS jika hasilnya "OD: N/A, OS: N/A"
            result_df['GRADE/VISUS'] = result_df['GRADE/VISUS'].apply(
                lambda x: '' if x == "OD: N/A, OS: N/A" else x
            )
    
    # Terapkan algoritma analisis gigi
    if all(col in df.columns for col in ['Gigi Karies (input)', 'Sisa Akar Gigi (input)', 'Gigi Gangren (input)']):
        result_df['GIGI DAN MULUT'] = df.apply(
            lambda row: analyze_dental(
                row['Gigi Karies (input)'],
                row['Sisa Akar Gigi (input)'],
                row['Gigi Gangren (input)']
            ), axis=1
        )
    else:
        # Cek kolom alternatif untuk gigi
        karies_cols = ['KARIES', 'GIGI_KARIES', 'CARIES']
        akar_cols = ['AKAR', 'SISA_AKAR', 'AKAR_GIGI']
        gangren_cols = ['GANGREN', 'GIGI_GANGREN']
        
        karies_col, akar_col, gangren_col = None, None, None
        
        for col in karies_cols:
            if col in df.columns:
                karies_col = col
                break
                
        for col in akar_cols:
            if col in df.columns:
                akar_col = col
                break
                
        for col in gangren_cols:
            if col in df.columns:
                gangren_col = col
                break
        
        if all(col is not None for col in [karies_col, akar_col, gangren_col]):
            result_df['GIGI DAN MULUT'] = df.apply(
                lambda row: analyze_dental(
                    row[karies_col],
                    row[akar_col],
                    row[gangren_col]
                ), axis=1
            )
    
    # Terapkan algoritma analisis spirometri
    if 'SPIROMETRY (input)' in df.columns:
        spirometry_results = df['SPIROMETRY (input)'].apply(analyze_spirometry)
        result_df['SPIROMETRY'] = [r[0] for r in spirometry_results]
        result_df['SPIROMETRY_OBSTRUKTIF'] = [r[1] for r in spirometry_results]
    else:
        # Jika kolom SPIROMETRY tidak ada, cek kolom alternatif
        spirometry_columns = ['SPIROMETRI', 'SPIRO', 'PEF', 'FEV1', 'FVC']
        for col in spirometry_columns:
            if col in df.columns:
                spirometry_results = df[col].apply(analyze_spirometry)
                result_df['SPIROMETRY'] = [r[0] for r in spirometry_results]
                result_df['SPIROMETRY_OBSTRUKTIF'] = [r[1] for r in spirometry_results]
                break
    
    # Terapkan algoritma analisis audiometri
    if 'AUDIOMETRI (input)' in df.columns:
        audiometry_results = df['AUDIOMETRI (input)'].apply(analyze_audiometry)
        result_df['AUDIOMETRY'] = [r[0] for r in audiometry_results]
        result_df['AUDIOMETRY_KANAN'] = [r[1] for r in audiometry_results]
    else:
        # Cek kolom alternatif untuk audiometri
        audiometry_columns = ['AUDIOMETRY', 'HEARING_TEST', 'PENDENGARAN']
        for col in audiometry_columns:
            if col in df.columns:
                audiometry_results = df[col].apply(analyze_audiometry)
                result_df['AUDIOMETRY'] = [r[0] for r in audiometry_results]
                result_df['AUDIOMETRY_KANAN'] = [r[1] for r in audiometry_results]
                break
    
    # Terapkan algoritma analisis laboratorium abnormal
    result_df['ABNORMAL LAB'] = result_df.apply(analyze_abnormal_lab, axis=1)
    
    # Isi kolom default
    result_df['PERUSAHAAN'] = 'PT PPA BIB'
    result_df['Tempat MCU'] = 'Klinik Perusahaan'
    
    return result_df

# Fungsi untuk menghasilkan statistik
def generate_statistics(result_df):
    total_records = len(result_df)
    
    return {
        "summary": {
            "total_records": total_records
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
    
    # Tambahkan opsi konfigurasi
    st.sidebar.header("Konfigurasi")
    show_debug = st.sidebar.checkbox("Tampilkan informasi debug", value=False)
    
    if uploaded_file is not None:
        try:
            # Baca file Excel
            df = pd.read_excel(uploaded_file)
            
            # Tampilkan preview data
            st.subheader("Preview Data Mentah")
            st.dataframe(df.head())
            
            # Tampilkan informasi file
            st.info(f"Jumlah baris: {len(df)}, Jumlah kolom: {len(df.columns)}")
            
            # Proses data
            with st.spinner("Memproses data MCU..."):
                result_df = process_mcu_data(df)
                statistics = generate_statistics(result_df)
            
            # Tampilkan hasil
            st.subheader("Hasil Pemrosesan Data MCU")
            st.dataframe(result_df)
            
            # Tampilkan informasi debug jika diaktifkan
            if show_debug:
                st.subheader("Informasi Debug")
                st.write(f"Shape of result dataframe: {result_df.shape}")
                st.write(f"Columns with non-null UMUR: {result_df['UMUR'].count() if 'UMUR' in result_df.columns else 0}")
                if 'UMUR' in result_df.columns:
                    st.write(f"Sample UMUR values: {result_df['UMUR'].head()}")
                
                # Tampilkan kolom yang tersedia
                st.write("Available columns:", list(result_df.columns))
            
            # Tampilkan statistik
            st.subheader("Statistik Pemrosesan")
            st.metric("Total Records", statistics['summary']['total_records'])
            
            # Tampilkan chart distribusi kategori
            st.subheader("Distribusi Kategori Kebugaran")
            st.info("Fitur kategorisasi telah dihapus")
            
            # Tampilkan distribusi berdasarkan departemen jika ada
            if 'DEPT' in result_df.columns:
                st.subheader("Distribusi berdasarkan Departemen")
                dept_stats = result_df['DEPT'].value_counts().reset_index()
                dept_stats.columns = ['Departemen', 'Jumlah']
                st.bar_chart(dept_stats.set_index('Departemen'))
            
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
            st.error("Silakan periksa format file Anda dan pastikan sesuai dengan template yang diharapkan.")
    else:
        st.info("Silakan unggah file Excel data MCU menggunakan panel di sebelah kiri.")
        
        # Tampilkan informasi penggunaan
        st.subheader("Cara Menggunakan Aplikasi")
        st.markdown("""
        1. Siapkan file data MCU dalam format Excel (.xlsx atau .xls)
        2. Pastikan file memiliki kolom-kolom yang sesuai dengan template
        3. Unggah file menggunakan tombol di panel sebelah kiri
        4. Tunggu proses pemrosesan selesai
        5. Lihat hasil pemrosesan dan statistiknya
        6. Gunakan filter untuk melihat data berdasarkan kategori tertentu
        7. Unduh hasil dalam format Excel jika diperlukan
        """)
        
        # Tampilkan contoh struktur kolom
        st.subheader("Contoh Struktur Kolom yang Diharapkan")
        sample_columns = [
            "NRP", "NAMA KARYAWAN", "UMRU", "L/P", "TIPE MCU", "TGL. MCU",
            "SITE / DEPARTEMEN", "JABATAN", "TB (cm)", "BB (Kg)", 
            "T. SISTOLE (input)", "T. DIASTOLE (input)", "Nadi /menit (input)",
            "HB 13 ~ 18 (input)", "KOL", "TG", "HDL", "LDL", "GDP", "HBA1C", "UA",
            "UREUM (10-50)", "CREAT", "OT", "PT", "HBSAG", "DRUGS", 
            "Rontgen (input)", "EKG (input)", "THT (input)", 
            "SISSTEM GENITO UROVENEROLOGI (input)", 
            "Keluhan Alergi (Sebutkan Alergi Apa)", "KB. Merokok (input)", 
            "BUTA WARNA (NEG/TOTAL/PARSIAL)", "OD (TP KCMT) (input)", 
            "OS (TP KCMT) (input)", "OD (KCMT) (input)", "OS (KCMT) (input)", 
            "Gigi Karies (input)", "Sisa Akar Gigi (input)", "Gigi Gangren (input)", 
            "SPIROMETRY (input)", "AUDIOMETRI (input)", "Anti HBs (input)"
        ]
        st.code(", ".join(sample_columns))

if __name__ == "__main__":
    main()