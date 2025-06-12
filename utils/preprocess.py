import re
import ast
import pandas as pd

def preprocess_ingredients(ingredients_text):
    if pd.isna(ingredients_text):
        return ""
    ingredients = str(ingredients_text).lower()
    ingredients = re.sub(r'[^\w\s,]', ' ', ingredients)  
    ingredients = re.sub(r'\s+', ' ', ingredients)      
    return ingredients.strip()

def parse_cooking_steps(steps_text):
    if pd.isna(steps_text) or steps_text == "N/A": return {}
    try:
        if isinstance(steps_text, str) and steps_text.startswith("['"):
            steps_list = ast.literal_eval(steps_text)
            steps_text = steps_list[0] if steps_list else ""
        steps_parts = str(steps_text).split(' | ')
        parsed_steps = {}
        for i, step_part in enumerate(steps_parts, 1):
            match = re.match(r'^(\d+)\s+(.*?)\s*(?:\[Gambar:\s*(.*?)\])?$', step_part.strip())
            if match:
                _, step_text, gambar_urls = match.groups()
                parsed_steps[f"langkah_{i}"] = step_text.strip()
                if gambar_urls:
                    gambar_list = [url.strip() for url in gambar_urls.split(',')]
                    parsed_steps[f"gambar_{i}"] = list(dict.fromkeys(gambar_list))
            else:
                parsed_steps[f"langkah_{i}"] = step_part.strip()
        return parsed_steps
    except:
        return {}

def parse_ingredients_list(ingredients_text):
    if isinstance(ingredients_text, list):
        return ingredients_text
    if pd.isna(ingredients_text):
        return []
    try:
        result = ast.literal_eval(ingredients_text)
        return result if isinstance(result, list) else [str(result)]
    except:
        return [str(ingredients_text)]

def parse_list_field(text):
    """Parsing untuk kolom list seperti metode_memasak"""
    if pd.isna(text):
        return []
    try:
        result = ast.literal_eval(text)
        return result if isinstance(result, list) else [str(result)]
    except:
        return [str(text)]