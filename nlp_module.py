from database import ALLERGEN_DB

def analyze_ingredients(text):
    text_lower = text.lower()

    # 🔍 Step 1: Check if this looks like ingredient text
    if "ingredient" not in text_lower and "ingredients" not in text_lower:
        return {
            "ingredients": text,
            "allergens_found": [],
            "confidence": 0.0,
            "status": "UNKNOWN (No ingredient text detected)"
        }

    detected = {}
    total_matches = 0

    # 🔍 Step 2: Count matches for each allergen
    for allergen, keywords in ALLERGEN_DB.items():
        count = 0

        for word in keywords:
            if word in text_lower:
                count += 1

        if count > 0:
            detected[allergen] = count
            total_matches += count

    # 🔍 Step 3: Calculate confidence
    # Normalize by total possible keywords
    max_possible = sum(len(v) for v in ALLERGEN_DB.values())

    if max_possible == 0:
        confidence = 0.0
    else:
        confidence = round(total_matches / max_possible, 2)

    # 🔍 Step 4: Determine status
    if len(detected) == 0:
        status = "SAFE"
    else:
        status = "UNSAFE"

    return {
        "ingredients": text,
        "allergens_found": list(detected.keys()),
        "confidence": confidence,
        "status": status
    }