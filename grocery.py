def generate_safe_list(products, user_allergies):
    safe_products = []

    for product in products:
        if not any(a in product["allergens"] for a in user_allergies):
            safe_products.append(product["name"])

    return safe_products