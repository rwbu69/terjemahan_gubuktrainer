#!/usr/bin/env python3
"""
Script untuk mengekstrak nilai-nilai unik dari semua key dalam 'profile'
untuk memudahkan proses terjemahan manual.
Dapat mengekstrak semua nilai atau hanya yang belum diterjemahkan.
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_DIR = PROJECT_ROOT / "data" / "id_partial_translated"
OUTPUT_FILE = SCRIPT_DIR / "custom_translations.json"
UNTRANSLATED_OUTPUT = SCRIPT_DIR / "untranslated_values.json"

def extract_unique_values(json_files):
    """
    Ekstrak semua nilai unik dari semua key dalam profile yang bertipe string atau array
    Termasuk nilai dalam array seperti 'secrets'
    """
    # Gunakan defaultdict untuk mengumpulkan nilai dari setiap key
    values = defaultdict(list)
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'profile' in data and isinstance(data['profile'], dict):
                profile = data['profile']
                
                # Iterasi semua key dalam profile
                for key, value in profile.items():
                    # Untuk string langsung
                    if isinstance(value, str) and value.strip():
                        values[key].append(value)
                    # Untuk array (seperti 'secrets')
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str) and item.strip():
                                values[key].append(item)
        
        except Exception as e:
            print(f"❌ Error reading {file_path.name}: {e}")
    
    # Hitung frekuensi dan urutkan
    unique_values = {}
    for key, value_list in sorted(values.items()):
        counter = Counter(value_list)
        # Sort by frequency (descending) then alphabetically
        sorted_values = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
        unique_values[key] = {
            value: {
                "count": count,
                "translation": ""
            }
            for value, count in sorted_values
        }
    
    return unique_values

def create_translation_template():
    """
    Buat template terjemahan dengan nilai default
    """
    return {
        "_info": {
            "description": "File ini berisi terjemahan custom untuk semua key dalam 'profile'",
            "instructions": "Isi field 'translation' dengan terjemahan bahasa Indonesia yang sesuai",
            "note": "Field 'count' menunjukkan berapa kali nilai tersebut muncul di dataset",
            "special_note": "Key yang sudah diterjemahkan (weight, dorm, class, shoes) sudah memiliki terjemahan default"
        },
        "translations": {}
    }

def load_existing_translations():
    """
    Load terjemahan yang sudah ada dari file JSON (jika ada)
    """
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "translations" in data:
                    existing = {}
                    for key, values in data["translations"].items():
                        existing[key] = {}
                        for original, trans_data in values.items():
                            if isinstance(trans_data, dict) and trans_data.get("translation"):
                                existing[key][original] = trans_data["translation"]
                    return existing
        except Exception as e:
            print(f"⚠️  Error loading existing translations: {e}")
    return {}

def main():
    """
    Main function
    """
    # Check untuk argument --untranslated-only
    untranslated_only = "--untranslated-only" in sys.argv or "-u" in sys.argv
    
    # Keys yang sudah diterjemahkan dan tidak perlu diambil lagi
    # Weight dan shoes sudah lengkap, dorm dan class mungkin masih ada yang perlu diterjemahkan
    skip_keys = ["weight", "shoes"]
    
    if untranslated_only:
        print("🔍 Mengekstrak nilai-nilai yang BELUM diterjemahkan...")
        print(f"   (Mengabaikan key: {', '.join(skip_keys)})\n")
    else:
        print("🔍 Mengekstrak nilai-nilai unik dari semua key dalam profile...\n")
    
    # Dapatkan semua file JSON
    json_files = sorted(INPUT_DIR.glob("*.json"))
    
    if not json_files:
        print(f"❌ Tidak ada file JSON di {INPUT_DIR}")
        return
    
    print(f"📦 Memproses {len(json_files)} file JSON...\n")
    
    # Load terjemahan yang sudah ada
    existing_translations = load_existing_translations()
    
    # Ekstrak nilai unik
    unique_values = extract_unique_values(json_files)
    
    # Buat template
    template = create_translation_template()
    template["translations"] = unique_values
    
    # Masukkan terjemahan yang sudah ada (dari file sebelumnya)
    for key in unique_values:
        if key in existing_translations:
            for original, translation in existing_translations[key].items():
                if original in template["translations"][key]:
                    template["translations"][key][original]["translation"] = translation
    
    # Filter untranslated jika diminta
    if untranslated_only:
        untranslated_template = {
            "_info": {
                "description": "File ini berisi nilai-nilai yang BELUM diterjemahkan",
                "instructions": "Isi field 'translation' dengan terjemahan bahasa Indonesia yang sesuai",
                "note": "Field 'count' menunjukkan berapa kali nilai tersebut muncul di dataset",
                "generated_from": "Difilter dari custom_translations.json",
                "skipped_keys": f"Key {', '.join(skip_keys)} tidak disertakan karena sudah diterjemahkan"
            },
            "translations": {}
        }
        
        # Hanya ambil yang belum diterjemahkan dan bukan skip_keys
        for key, values in template["translations"].items():
            # Skip keys yang sudah diterjemahkan
            if key in skip_keys:
                continue
                
            untranslated_values = {
                original: data 
                for original, data in values.items() 
                if not data["translation"] or data["translation"].strip() == ""
            }
            if untranslated_values:
                untranslated_template["translations"][key] = untranslated_values
        
        # Simpan ke file terpisah
        output_path = UNTRANSLATED_OUTPUT
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(untranslated_template, f, ensure_ascii=False, indent=2)
        
        # Tampilkan statistik untuk untranslated
        print("📊 Statistik nilai yang BELUM diterjemahkan:\n")
        total_untranslated = 0
        
        for key in sorted(untranslated_template["translations"].keys()):
            values = untranslated_template["translations"][key]
            count = len(values)
            total_untranslated += count
            
            print(f"  ⚠️  {key}")
            print(f"      Belum diterjemahkan: {count}")
            print()
        
        print(f"✨ File nilai yang belum diterjemahkan disimpan di: {output_path}")
        print(f"\n📝 Total nilai yang belum diterjemahkan: {total_untranslated}")
        
        if total_untranslated == 0:
            print(f"\n🎉 Semua nilai sudah memiliki terjemahan!")
        else:
            print(f"\n💡 Silakan edit file tersebut dan isi field 'translation' yang masih kosong.")
            print(f"   Setelah selesai, jalankan script ini tanpa flag --untranslated-only")
            print(f"   untuk merge terjemahan kembali ke custom_translations.json")
    
    else:
        # Simpan ke file JSON lengkap
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        
        # Tampilkan statistik lengkap
        print("📊 Statistik nilai unik per key:\n")
        total_values = 0
        translated_values = 0
        
        for key in sorted(template["translations"].keys()):
            values = template["translations"][key]
            total = len(values)
            translated = sum(1 for v in values.values() if v["translation"])
            total_values += total
            translated_values += translated
            
            status = "✅" if translated == total else "⚠️ "
            print(f"  {status} {key}")
            print(f"      Total unik: {total}")
            print(f"      Sudah diterjemahkan: {translated}")
            if translated < total:
                print(f"      Perlu diterjemahkan: {total - translated}")
            print()
        
        print(f"✨ File terjemahan disimpan di: {OUTPUT_FILE}")
        print(f"\n📝 Total: {total_values} nilai unik")
        print(f"✅ Sudah diterjemahkan: {translated_values}")
        
        if translated_values < total_values:
            print(f"⚠️  Perlu diterjemahkan: {total_values - translated_values}")
            print(f"\n💡 Silakan edit file tersebut dan isi field 'translation' yang masih kosong.")
            print(f"   Atau gunakan flag --untranslated-only untuk hanya melihat yang belum diterjemahkan:")
            print(f"   python {Path(__file__).name} --untranslated-only")
        else:
            print(f"\n🎉 Semua nilai sudah memiliki terjemahan!")

if __name__ == "__main__":
    main()
