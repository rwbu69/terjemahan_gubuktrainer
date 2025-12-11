# Translation System Documentation

Sistem terjemahan untuk file JSON karakter Uma Musume.

## Files

### Script Files
- `extract_unique_values.py` - Ekstrak nilai unik dari profile untuk diterjemahkan
- `translate_partial_to_id.py` - Terjemahkan JSON menggunakan custom translations
- `merge_translations.py` - Merge terjemahan dari untranslated_values.json ke custom_translations.json

### Data Files
- `custom_translations.json` - Database terjemahan lengkap (semua nilai)
- `untranslated_values.json` - Database nilai yang belum diterjemahkan (generated)

## Workflow

### 1. Ekstrak Semua Nilai Unik
```bash
python translation/extract_unique_values.py
```
Menghasilkan `custom_translations.json` dengan semua nilai unik dari profile.

### 2. Ekstrak Hanya Yang Belum Diterjemahkan
```bash
python translation/extract_unique_values.py --untranslated-only
# atau
python translation/extract_unique_values.py -u
```
Menghasilkan `untranslated_values.json` dengan hanya nilai yang belum diterjemahkan.

### 3. Terjemahkan Manual
Edit file `untranslated_values.json` dan isi field `"translation"` dengan terjemahan bahasa Indonesia.

### 4. Merge Terjemahan
```bash
python translation/merge_translations.py
```
Merge terjemahan dari `untranslated_values.json` ke `custom_translations.json`.

### 5. Jalankan Terjemahan
```bash
python translation/translate_partial_to_id.py
```
Menerjemahkan file JSON dari `data/id_partial_translated` ke `data/id_translated`.

## Struktur Data

### custom_translations.json
```json
{
  "_info": { ... },
  "translations": {
    "weight": {
      "No change": {
        "count": 13,
        "translation": "Tidak berubah"
      }
    },
    "ears": {
      "Always alert": {
        "count": 1,
        "translation": "Selalu waspada"
      }
    }
  }
}
```

### Input/Output Folders
- **Input**: `data/id_partial_translated/` - File dengan weight, dorm, class, shoes sudah diterjemahkan
- **Output**: `data/id_translated/` - File dengan semua profile sudah diterjemahkan

## Key Profile yang Diterjemahkan

Script `translate_partial_to_id.py` akan menerjemahkan semua key string dalam profile:
- `self_intro` - Perkenalan karakter
- `tagline` - Tagline/slogan
- `weight` - Status berat badan
- `shoes` - Ukuran sepatu
- `dorm` - Asrama
- `class` - Divisi/kelas
- `ears` - Karakteristik telinga
- `tail` - Karakteristik ekor
- `strong` - Keahlian/kekuatan
- `weak` - Kelemahan
- `family` - Tentang keluarga

## Tips

1. **Terjemahkan bertahap**: Gunakan `--untranslated-only` untuk fokus pada yang belum diterjemahkan
2. **Frekuensi tinggi prioritas**: Nilai dengan `count` tinggi muncul lebih sering
3. **Preserve nuansa**: Jaga nuansa dan konteks saat menerjemahkan
4. **Re-extract untuk update**: Jalankan `extract_unique_values.py` lagi jika ada file JSON baru

## Progress
- [x] Weight
- [x] Shoes
- [x] Dorm
- [x] Class
- [x] Self Intro (Masih harus di cek ulang)
- [x] Tagline (Masih harus di cek ulang)
- [x] Ears (Masih harus di cek ulang)
- [x] Tail (Masih harus di cek ulang)
- [x] Strong (Masih harus di cek ulang)
- [x] Weak (Masih harus di cek ulang)
- [x] Family (Masih harus di cek ulang)
- [x] Secrets (Masih harus di cek ulang)
