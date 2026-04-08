from fastapi import FastAPI, UploadFile, File
import shutil
from ocr_module import extract_text
from nlp_module import analyze_ingredients
from utils import safety_color
from models import UserProfile
from grocery import generate_safe_list

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SafeCart API running"}

# ---------- IMAGE SCAN ----------
@app.post("/scan-product/")
async def scan_product(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    result = analyze_ingredients(text)

    return {
        "ocr_text": text,
        "analysis": result,
        "overlay_color": safety_color(result["status"])
    }

# ---------- USER PROFILE ----------
user_profile = {"allergies": []}

@app.post("/set-profile/")
def set_profile(profile: UserProfile):
    global user_profile
    user_profile = profile.dict()
    return {"message": "Profile saved", "profile": user_profile}

# ---------- GROCERY LIST ----------
@app.post("/generate-list/")
def generate_list():
    sample_products = [
        {"name": "Bread", "allergens": ["gluten"]},
        {"name": "Almond Milk", "allergens": []},
        {"name": "Peanut Butter", "allergens": ["peanut"]},
    ]

    safe = generate_safe_list(sample_products, user_profile["allergies"])

    return {"safe_products": safe}