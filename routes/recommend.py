from flask import Blueprint, request, jsonify
from services.database import load_recipe_data
from utils.recommendation import build_vectorizer, recommend
from services.image_detection import detect_ingredients_from_image
import tempfile
from flasgger.utils import swag_from

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route('/recommend', methods=['POST'])
@swag_from({
    'tags': ['Recommendation'],
    'summary': 'Rekomendasi resep berdasarkan gambar',
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'image',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Gambar bahan makanan'
        }
    ],
    'responses': {
        '200': {
            'description': 'Berhasil memberikan rekomendasi',
            'examples': {
                'application/json': {
                    "status": "success",
                    "ingredients_detected": ["telur", "bawang merah"],
                    "data": [
                        {
                            "resep_id": "12345",
                            "judul": "Telur Dadar Sehat",
                            "bahan": ["telur", "bawang merah", "garam"],
                            "bahan_tidak_terdeteksi": ["garam"],
                            "langkah": {
                                "1": {
                                    "deskripsi": "Kocok telur dan bawang.",
                                    "gambar": []
                                }
                            },
                            "kalori": 250,
                            "karbohidrat": 5,
                            "lemak": 20,
                            "protein": 12,
                            "metode_memasak": "goreng",
                            "similarity_score": 0.4,
                            "gambar": "https://..."
                        }
                    ]
                }
            }
        },
        '400': {
            'description': 'Gambar tidak ditemukan dalam request'
        }
    }
})
def recommend_route():
    print('request')
    print(request.files)
    if 'image' not in request.files:
        return jsonify({"error": "Image file is required"}), 400

    image_file = request.files['image']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
        image_file.save(temp_img.name)
        ingredients = detect_ingredients_from_image(temp_img.name)

    if not ingredients:
        return jsonify({"error": "No ingredients detected from image"}), 400
    
    df = load_recipe_data()
    df_vector, vectorizer, matrix = build_vectorizer(df)
    result = recommend(df_vector, matrix, vectorizer, ingredients)
    
    return jsonify({
        "status": "success",
        "ingredients_detected": ingredients,
        "data": result
    })
