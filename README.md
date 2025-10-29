# Information Retrieval System - UTS Praktikum PI

Sistem Information Retrieval berbasis CLI untuk pencarian dan ranking dokumen dari 5 dataset: ETD-USK, ETD-UGM, Kompas, Tempo, dan Mojok.

## 👥 Tim Pengembang

- Anggota 1: Al-Mahfuzh Fadhlur Rohman (2208107010016)

**Kelompok:** 9

## 📋 Deskripsi Sistem

Sistem ini mengimplementasikan pipeline lengkap Information Retrieval yang mencakup:

- **Text Preprocessing**: Case folding, tokenization, stopword removal
- **Document Representation**: Bag of Words (BoW) menggunakan CountVectorizer
- **Indexing**: Whoosh search engine untuk indexing cepat
- **Ranking**: Cosine Similarity untuk menghitung relevansi dokumen

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+**
- **Whoosh**: Library indexing dan searching
- **scikit-learn**: CountVectorizer dan cosine similarity
- **pandas**: Manipulasi data (opsional)

## 📦 Instalasi

### 1. Install Dependencies

```bash
pip install whoosh scikit-learn pandas
```

### 2. Struktur Folder Dataset

Pastikan struktur folder dataset sudah sesuai:

```
project/
├── UTS-PI.py
├── README.md
└── dataset/
    ├── etd-usk.csv
    ├── etd-ugm.csv
    ├── kompas.csv
    ├── tempo.csv
    └── mojok.csv
```

## 🚀 Cara Menjalankan

```bash
python uts-py.py
```

## 📖 Panduan Penggunaan

### Menu Utama

```
=== INFORMATION RETRIEVAL SYSTEM ===
[1] Load & Index Dataset
[2] Search Query
[3] Exit
====================================
```

### 1. Load & Index Dataset

- Pilih menu [1] untuk memuat semua dataset
- Sistem akan:
  - Membaca semua dokumen dari 5 folder dataset
  - Melakukan preprocessing pada setiap dokumen
  - Membuat index Whoosh
  - Membuat representasi BoW untuk semua dokumen

**Output contoh:**

```
Loading dataset: etd-usk...
Loaded 150 documents from etd-usk
Loading dataset: etd-ugm...
Loaded 200 documents from etd-ugm
...
Total documents loaded: 1000

=== Creating Index ===
Indexing documents...
Indexed 1000/1000 documents
Indexing complete!

=== Creating Document Vectors (BoW) ===
Vocabulary size: 15000
Document vectors shape: (1000, 15000)
```

### 2. Search Query

- Pilih menu [2]
- Masukkan kata kunci pencarian
- Sistem akan menampilkan 5 dokumen paling relevan beserta skor

**Contoh pencarian:**

```
Enter your search query: machine learning

=== Searching for: 'machine learning' ===
Preprocessed query: 'machine learning'
Found 45 candidate documents from Whoosh

=== Top 5 Results ===

Rank 1:
  Title: ml_research.txt
  Source: etd-ugm
  Score: 0.8524
  Preview: Machine learning adalah cabang dari artificial intelligence...
  Path: datasets/etd-ugm/ml_research.txt

Rank 2:
  Title: ai_development.txt
  Source: etd-usk
  Score: 0.7231
  Preview: Perkembangan machine learning di Indonesia...
  Path: datasets/etd-usk/ai_development.txt
...
```

### 3. Exit

- Pilih menu [3] untuk keluar dari program

## 🔧 Fitur Preprocessing

### 1. Case Folding

Mengubah semua teks menjadi huruf kecil untuk normalisasi.

```python
text = "Machine Learning" → "machine learning"
```

### 2. Tokenization

Memecah teks menjadi token-token individual.

```python
text = "machine learning adalah" → ["machine", "learning", "adalah"]
```

### 3. Stopword Removal

Menghapus kata-kata umum yang tidak memberikan informasi penting.

```python
tokens = ["machine", "learning", "adalah", "yang"]
→ ["machine", "learning"]  # "adalah" dan "yang" dihapus
```

### 4. Special Character Removal

Menghapus karakter khusus dan angka.

```python
text = "AI-2024: machine learning!" → "ai machine learning"
```

## 📊 Metode Ranking

### Cosine Similarity

Sistem menggunakan cosine similarity untuk menghitung kemiripan antara query dan dokumen:

```
similarity = (query_vector · doc_vector) / (||query_vector|| × ||doc_vector||)
```

**Rentang nilai:** 0.0 - 1.0

- 1.0 = Sangat mirip
- 0.0 = Tidak mirip sama sekali

## 🏗️ Arsitektur Sistem

```
User Input (Query)
    ↓
Preprocessing (case folding, tokenization, stopword removal)
    ↓
Whoosh Indexing (mencari kandidat dokumen)
    ↓
Vectorization (BoW dengan CountVectorizer)
    ↓
Cosine Similarity (ranking dokumen)
    ↓
Top-K Results (5 dokumen teratas)
```

## 📁 File-File Proyek

```
NoKelompok_UTS_Praktikum_PI/
├── uts-pi.py              # Program utama
├── README.md              # Dokumentasi ini
├── laporan.pdf            # Laporan UTS
├── datasets/              # Folder dataset (tidak disubmit)
│   ├── etd-usk.csv
│   ├── etd-ugm.csv
│   ├── kompas.csv
│   ├── tempo.csv
│   └── mojok.csv
└── indexdir/             # Index Whoosh (auto-generated)
```

## 🧪 Testing

### Test Query Examples

1. **Query umum:**

   - "machine learning"
   - "pendidikan Indonesia"
   - "ekonomi digital"

2. **Query spesifik:**
   - "penerapan AI dalam kesehatan"
   - "dampak pandemi terhadap pendidikan"
   - "politik Indonesia 2024"

### Expected Results

- Sistem harus mengembalikan 5 dokumen teratas
- Dokumen dengan skor lebih tinggi lebih relevan
- Dokumen harus berasal dari berbagai dataset yang sesuai

## ⚠️ Troubleshooting

### Error: "No documents found"

- Pastikan folder `datasets/` ada dan berisi 5 subfolder
- Pastikan setiap subfolder berisi file .txt atau .text
- Periksa encoding file (harus UTF-8)

### Error: "Index not found"

- Jalankan menu [1] Load & Index Dataset terlebih dahulu
- Pastikan folder `indexdir/` dapat dibuat

### Error: "Import Error"

- Install semua dependencies: `pip install -r requirements.txt`
- Gunakan Python 3.8 atau lebih baru

## 📚 Referensi

- Whoosh Documentation: https://whoosh.readthedocs.io/
- scikit-learn Documentation: https://scikit-learn.org/
- Information Retrieval: Manning, Raghavan, and Schütze

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik UTS Praktikum Penelusuran Informasi, Departemen Informatika FMIPA Universitas Syiah Kuala.

---

**Dosen Pengampu:**

- Fathia Sabrina, S.T., M.Inf.Tech
- Fitria Nilamsari, S.Kom., M.Sc

**Semester:** Ganjil 2025/2026
