# 📸🍲 Flask Image-Based Recipe Recommendation API

## Deskripsi  
API berbasis Flask untuk merekomendasikan resep masakan berdasarkan bahan makanan yang terdeteksi dari gambar.  
Sistem ini memanfaatkan Computer Vision untuk mendeteksi bahan, TF-IDF Vectorizer untuk representasi resep, dan Cosine Similarity untuk rekomendasi.

---

## 🚀 Fitur Utama

- ✅ Upload Gambar
- ✅ Deteksi Bahan Otomatis
- ✅ Rekomendasi Resep Relevan
- ✅ Langkah Memasak Lengkap
- ✅ Swagger UI (dokumentasi API interaktif)

---

## 🗂️ Struktur Project

```
backend-machine-learning/
├── app.py                # Entry point Flask
├── routes/
│   └── recommend.py      # Route rekomendasi
├── services/
│   ├── database.py       # Load data resep dari DB
│   └── image_detection.py# Fungsi deteksi bahan
├── utils/
│   ├── preprocess.py     # Fungsi preprocessing teks & parse list
│   └── recommendation.py # Build vectorizer & logika rekomendasi
├── requirements.txt      # Dependensi Python
└── README.md             # Dokumentasi ini
```

---

## ⚙️ Instalasi

### 1️⃣ Clone Repo

```bash
git clone https://github.com/kasep-capstone/backend-machine-learning.git
cd backend-machine-learning
```

### 2️⃣ Buat Virtual Environment & Install Dependensi

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
# atau
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3️⃣ Jalankan Server

```bash
python app.py
```

---

## 🔑 Endpoint Utama

### 1️⃣ POST `/api/recommend`

**Deskripsi:**  
Upload gambar bahan makanan untuk mendapatkan rekomendasi resep yang relevan.

**Form Data:**

| Key   | Tipe | Deskripsi          |
|-------|------|--------------------|
| image | file | Gambar bahan makanan |

**Contoh CURL:**

```bash
curl -X POST "http://localhost:5000/api/recommend" \
  -H  "accept: application/json" \
  -H  "Content-Type: multipart/form-data" \
  -F "image=@path_to_your_image.jpg"
```

**Contoh Response:**

```json
{
  "status": "success",
  "ingredients_detected": ["telur", "bawang merah"],
  "data": [
    {
      "judul": "Telur Dadar Sehat",
      "bahan": ["telur", "bawang merah", "garam"],
      "bahan_tidak_terdeteksi": ["garam"],
      "langkah": {
        "1": {
          "deskripsi": "Kocok telur dan bawang.",
          "gambar": []
        }
      },
      "gambar": "https://...",
      "kalori": 250,
      "karbohidrat": 5,
      "lemak": 20,
      "protein": 12,
      "metode_memasak": ["goreng"],
      "deskripsi": "Resep telur dadar praktis...",
      "similarity_score": 0.4
    }
  ]
}
```

---

## ✅ Swagger UI

Setelah server berjalan, buka:

```
http://localhost:5000/apidocs
```

untuk mencoba API melalui Swagger Interaktif.

---

## 🧑‍💻 Author

- **Nama:** [Danny Suggi Saputra]
- **GitHub:** [https://github.com/dannyysaputra](https://github.com/dannyysaputra)

---

## 📜 License

MIT © [2025] [Danny Suggi Saputra]