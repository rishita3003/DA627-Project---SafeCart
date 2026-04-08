import requests
import os
import time

os.makedirs("sample_images", exist_ok=True)

products = [
    "3017620422003",
    "737628064502",
    "7622210449283",
    "5000159484695",
    "3560070768398"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def download_image(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        print("Processing:", barcode)

        res = requests.get(url, headers=HEADERS)
        data = res.json()

        if data.get("status") != 1:
            print(f"No product found: {barcode}")
            return

        product = data["product"]

        # 🔥 IMPORTANT CHANGE HERE
        img_url = product.get("image_ingredients_url") or product.get("image_url")

        if not img_url:
            print(f"No ingredient image for {barcode}")
            return

        img_data = requests.get(img_url, headers=HEADERS).content

        filename = f"sample_images/{barcode}_ingredients.jpg"

        with open(filename, "wb") as f:
            f.write(img_data)

        print(f"Downloaded: {filename}")

        time.sleep(1)

    except Exception as e:
        print(f"Error for {barcode}: {e}")


for p in products:
    download_image(p)