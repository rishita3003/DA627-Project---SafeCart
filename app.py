from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil

from ocr_module import extract_text
from nlp_module import analyze_ingredients
from utils import safety_color
from models import UserProfile
from grocery import generate_safe_list

app = FastAPI()

# Templates setup
templates = Jinja2Templates(directory="templates")

# ---------- HOME (UI) ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,                # ✅ FIRST argument
        "index.html",           # ✅ SECOND argument
        {"request": request}    # ✅ THIRD argument
    )

# ---------- IMAGE SCAN ----------
from fastapi import Form

@app.post("/scan-product/")
async def scan_product(
    file: UploadFile = File(...),
    user_allergens: str = Form("")
):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    # Convert user input into list
    user_allergens_list = [a.strip().lower() for a in user_allergens.split(",") if a.strip()]

    result = analyze_ingredients(text)

    # 🔥 PERSONAL FILTER
    if user_allergens_list:
        matched = [a for a in result["allergens_found"] if a in user_allergens_list]
        
        result["allergens_found"] = matched
        result["status"] = "UNSAFE" if matched else "SAFE"

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