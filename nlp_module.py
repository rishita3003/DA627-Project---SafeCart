from database import detect_allergens

def analyze_ingredients(text):
    allergens = detect_allergens(text)

    if len(allergens) == 0:
        status = "SAFE"
    else:
        status = "UNSAFE"

    return {
        "ingredients": text,
        "allergens_found": allergens,
        "status": status
    }