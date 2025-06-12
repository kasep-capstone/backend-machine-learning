import pandas as pd
from config import DATABASE_URL
from collections import defaultdict
from sqlalchemy import create_engine

def load_recipe_data():
    engine = create_engine(DATABASE_URL)
    query = """
        SELECT
            r.id AS receipt_id,
            r.judul,
            r."labelBahan",
            r.gambar,
            r.kalori,
            r."metodeMemasak",
            r.deskripsi,
            r.karbohidrat,
            r.lemak,
            r.protein,
            s."stepNumber",
            s.description AS step_description,
            si.url AS step_image_url,
            si."order" AS step_image_order
        FROM "Receipt" r
        LEFT JOIN "Step" s ON s."receiptId" = r.id
        LEFT JOIN "StepImage" si ON si."stepId" = s.id
        ORDER BY r.id, s."stepNumber", si."order"
    """
    df = pd.read_sql_query(query, engine)

    recipes = defaultdict(lambda: {
        "resep_id": "",
        "judul": "",
        "labelBahan": "",
        "gambar": "",
        "kalori": "",
        "karbohidrat": "",
        "lemak": "",
        "protein": "",
        "metode_memasak": "",
        "deskripsi": "",
        "langkah": defaultdict(lambda: {
            "deskripsi": "",
            "gambar": []
        })
    })

    for _, row in df.iterrows():
        r = recipes[row["receipt_id"]]
        r["receipt_id"] = row["receipt_id"]
        r["judul"] = row["judul"]
        r["labelBahan"] = row["labelBahan"]
        r["gambar"] = row["gambar"]
        r["kalori"] = row["kalori"]
        r["karbohidrat"] = row["karbohidrat"]
        r["lemak"] = row["lemak"]
        r["protein"] = row["protein"]
        r["metode_memasak"] = row["metodeMemasak"]
        r["deskripsi"] = row["deskripsi"]

        step_number = row["stepNumber"]
        if pd.notna(step_number):
            langkah = r["langkah"][int(step_number)]
            langkah["deskripsi"] = row["step_description"]
            if pd.notna(row["step_image_url"]):
                langkah["gambar"].append(row["step_image_url"])

    # Convert defaultdict to dict
    final_data = []
    for recipe in recipes.values():
        recipe["langkah"] = dict(recipe["langkah"])  # konversi langkah per resep ke dict biasa
        final_data.append(recipe)

    df_resep = pd.DataFrame(final_data)
    return df_resep