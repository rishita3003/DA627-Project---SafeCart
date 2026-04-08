ALLERGEN_DB = {
    "milk": ["milk", "casein", "lactose", "whey"],
    "peanut": ["peanut", "groundnut", "arachis"],
    "gluten": ["wheat", "barley", "rye", "triticum"],
    "soy": ["soy", "soya", "soybean"],
    "egg": ["egg", "albumin"],
}

def detect_allergens(ingredients_text):
    found = []
    text = ingredients_text.lower()

    for allergen, keywords in ALLERGEN_DB.items():
        for word in keywords:
            if word in text:
                found.append(allergen)
                break

    return list(set(found))