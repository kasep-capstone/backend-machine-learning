import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import preprocess_ingredients, parse_ingredients_list, parse_list_field

def build_vectorizer(df):
    # Pastikan kolom labelBahan ada
    df['labelBahan_Clean'] = df['labelBahan'].apply(preprocess_ingredients)
    df = df[df['labelBahan_Clean'] != ''].reset_index(drop=True)

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    matrix = vectorizer.fit_transform(df['labelBahan_Clean'])
    return df, vectorizer, matrix


def recommend(df, tfidf_matrix, vectorizer, detected_ingredients, top_k=5, threshold=0.1):
    detected_text = ' '.join([preprocess_ingredients(i) for i in detected_ingredients])
    detected_vec = vectorizer.transform([detected_text])
    similarities = cosine_similarity(detected_vec, tfidf_matrix).flatten()

    indices = np.argsort(similarities)[::-1]
    recommendations = []

    for idx in indices:
        if similarities[idx] >= threshold and len(recommendations) < top_k:
            row = df.iloc[idx]

            # Ambil bahan dari resep
            bahan_asli = parse_ingredients_list(row['labelBahan'])
            # Ambil bahan yang tidak terdeteksi
            bahan_tidak_terdeteksi = [
                b for b in bahan_asli 
                if preprocess_ingredients(b) not in [preprocess_ingredients(i) for i in detected_ingredients]
            ]

            # Pastikan langkah tersedia dan terstruktur dengan benar
            langkah_dict = {}
            langkah_raw = row.get('langkah', {})

            if isinstance(langkah_raw, dict):
                for step_number, step_data in sorted(langkah_raw.items()):
                    langkah_dict[int(step_number)] = {
                        'deskripsi': step_data.get('deskripsi', ''),
                        'gambar': step_data.get('gambar', [])
                    }

            recommendations.append({
                'receipt_id': row['receipt_id'],
                'judul': row['judul'],
                'bahan': bahan_asli,
                'bahan_tidak_terdeteksi': bahan_tidak_terdeteksi,
                'metode_memasak': parse_list_field(row.get('metode_memasak', '')),
                'langkah': langkah_dict,
                'gambar': row.get('gambar', 'N/A'),
                'kalori': row.get('kalori', 'N/A'),
                'karbohidrat': row.get('karbohidrat', 'N/A'),
                'lemak': row.get('lemak', 'N/A'),
                'protein': row.get('protein', 'N/A'),
                'deskripsi': row.get('deskripsi', ''),
                'similarity_score': round(similarities[idx], 4)
            })

    return recommendations