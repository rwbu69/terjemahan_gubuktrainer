#!/usr/bin/env python3
"""
Script helper untuk merge terjemahan dari untranslated_values.json ke custom_translations.json
Mendukung semua key profile termasuk array seperti 'secrets'
"""

import json
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent
CUSTOM_TRANSLATIONS = SCRIPT_DIR / "custom_translations.json"
UNTRANSLATED_VALUES = SCRIPT_DIR / "untranslated_values.json"

def merge_translations():
    """
    Merge translations dari untranslated_values.json ke custom_translations.json
    """
    # Check file existence
    if not CUSTOM_TRANSLATIONS.exists():
        print(f"❌ File {CUSTOM_TRANSLATIONS} tidak ditemukan!")
        return False
    
    if not UNTRANSLATED_VALUES.exists():
        print(f"❌ File {UNTRANSLATED_VALUES} tidak ditemukan!")
        print(f"   Jalankan extract_unique_values.py --untranslated-only terlebih dahulu")
        return False
    
    # Load both files
    with open(CUSTOM_TRANSLATIONS, 'r', encoding='utf-8') as f:
        custom = json.load(f)
    
    with open(UNTRANSLATED_VALUES, 'r', encoding='utf-8') as f:
        untranslated = json.load(f)
    
    # Merge translations
    merged_count = 0
    for key, values in untranslated.get("translations", {}).items():
        if key in custom.get("translations", {}):
            for original, data in values.items():
                if original in custom["translations"][key]:
                    # Hanya update jika ada terjemahan di untranslated
                    if data.get("translation") and data["translation"].strip():
                        custom["translations"][key][original]["translation"] = data["translation"]
                        merged_count += 1
    
    # Save back to custom_translations.json
    with open(CUSTOM_TRANSLATIONS, 'w', encoding='utf-8') as f:
        json.dump(custom, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Berhasil merge {merged_count} terjemahan ke {CUSTOM_TRANSLATIONS}")
    
    # Show summary
    total_values = 0
    translated_values = 0
    for key, values in custom.get("translations", {}).items():
        total = len(values)
        translated = sum(1 for v in values.values() if v.get("translation"))
        total_values += total
        translated_values += translated
    
    print(f"\n📊 Status setelah merge:")
    print(f"   Total nilai: {total_values}")
    print(f"   Sudah diterjemahkan: {translated_values}")
    print(f"   Belum diterjemahkan: {total_values - translated_values}")
    
    return True

if __name__ == "__main__":
    merge_translations()
