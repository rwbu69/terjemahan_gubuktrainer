#!/usr/bin/env python3
"""
Script untuk menerjemahkan key 'weight', 'dorm', 'class', dan 'shoes' 
dari bahasa Inggris ke bahasa Indonesia dengan mempertahankan nuansa terjemahan.
Membaca terjemahan custom dari file JSON.
"""

import json
import os
from pathlib import Path
from deep_translator import GoogleTranslator

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_DIR = PROJECT_ROOT / "data" / "id_partial_translated"
OUTPUT_DIR = PROJECT_ROOT / "data" / "id_translated"
CUSTOM_TRANSLATIONS_FILE = SCRIPT_DIR / "custom_translations.json"

# Buat output directory jika belum ada
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_custom_translations():
    """
    Load custom translations dari file JSON
    """
    if not CUSTOM_TRANSLATIONS_FILE.exists():
        print(f"⚠️  File custom translations tidak ditemukan: {CUSTOM_TRANSLATIONS_FILE}")
        print("   Menggunakan terjemahan default saja.\n")
        return {}
    
    try:
        with open(CUSTOM_TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Flatten structure untuk lookup yang mudah
        translations = {}
        if "translations" in data:
            for key_type, values in data["translations"].items():
                for original, trans_data in values.items():
                    if isinstance(trans_data, dict) and trans_data.get("translation"):
                        translations[original] = trans_data["translation"]
        
        print(f"✅ Loaded {len(translations)} custom translations from JSON\n")
        return translations
    
    except Exception as e:
        print(f"❌ Error loading custom translations: {e}")
        print("   Menggunakan terjemahan default saja.\n")
        return {}

# Load custom translations dari JSON
CUSTOM_TRANSLATIONS = load_custom_translations()

def translate_with_fallback(text: str, translator: GoogleTranslator) -> str:
    """
    Terjemahkan text dengan prioritas kamus custom, fallback ke Google Translate
    """
    # Cek apakah ada di kamus custom
    if text in CUSTOM_TRANSLATIONS:
        return CUSTOM_TRANSLATIONS[text]
    
    # Jika tidak ada, gunakan Google Translate
    try:
        translated = translator.translate(text)
        return translated if translated else text
    except Exception as e:
        print(f"   ⚠️  Error translating '{text}': {e}")
        return text

def translate_profile_keys(profile: dict, translator: GoogleTranslator) -> dict:
    """
    Terjemahkan semua key string dalam profile menggunakan custom translations
    """
    for key, value in profile.items():
        # Hanya terjemahkan nilai string, skip array/list
        if isinstance(value, str) and value.strip():
            original = value
            translated = translate_with_fallback(original, translator)
            profile[key] = translated
            
            # Log jika ada perubahan
            if original != translated:
                print(f"   {key}: '{original[:50]}...' → '{translated[:50]}...'")
    
    return profile

def process_file(file_path: Path, translator: GoogleTranslator):
    """
    Proses satu file JSON
    """
    try:
        # Baca file JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📄 Processing {file_path.name} ...")
        
        # Cek apakah ada profile
        if 'profile' in data and isinstance(data['profile'], dict):
            data['profile'] = translate_profile_keys(data['profile'], translator)
        
        # Simpan hasil terjemahan
        output_path = OUTPUT_DIR / file_path.name
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Saved: {output_path}\n")
        
    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}\n")

def main():
    """
    Main function
    """
    print("🚀 Memulai terjemahan parsial ke Bahasa Indonesia...\n")
    
    # Inisialisasi translator
    translator = GoogleTranslator(source='en', target='id')
    
    # Dapatkan semua file JSON
    json_files = sorted(INPUT_DIR.glob("*.json"))
    
    if not json_files:
        print(f"❌ Tidak ada file JSON di {INPUT_DIR}")
        return
    
    print(f"📦 Ditemukan {len(json_files)} file JSON\n")
    
    # Proses setiap file
    for file_path in json_files:
        process_file(file_path, translator)
    
    print(f"✨ Selesai! Semua file telah diterjemahkan dan disimpan di {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
