from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product
from .utils import extract_product_id
from .services import fetch_product_data

def get_or_create_product(request):
    url = request.GET.get("url")  # Récupère l'URL du produit
    if not url:
        return JsonResponse({"error": "Missing URL"}, status=400)

    product_id = extract_product_id(url)
    if not product_id:
        return JsonResponse({"error": "Invalid AliExpress URL"}, status=400)

    # Vérifier si le produit est déjà en base
    product, created = Product.objects.get_or_create(product_id=product_id)

    if created:
        # Ajoutez un peu de log pour le débogage
        data = fetch_product_data(product_id)
        if "error" in data:
            return JsonResponse(data, status=500)

        # Remplissage des champs du produit
        product.title = data["data"].get("title", "Unknown Title")
        product.description = data["data"].get("description", "")
        product.image = data["data"].get("image", "")
        product.url = url
        product.category_id = data["data"].get("category_id", None)
        product.has_stock = data["data"].get("in_stock", True)
        product.number_sold = data["data"].get("number_sold", "0")

        product.save()  # Enregistrer le produit dans la base de données

    else:
        print(f"Product already exists: {product_id}")

    # Appel à l'API ChatGPT avec les données du produit
    transformed_data = call_chatgpt_api({
        "title": product.title,
        "description": product.description,
        "price": product.price,
    })

    return JsonResponse({"message": "Product retrieved", "product": {
        "title": product.title,
        "description": product.description,
        "image": product.image,
        "url": product.url,
        "category_id": product.category_id,
        "has_stock": product.has_stock,
        "number_sold": product.number_sold,
        "transformed_data": transformed_data,
    }}, status=200)


def call_chatgpt_api(product_data):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer ",  # 
        "Content-Type": "application/json"
    }

    # Construisez le prompt que vous voulez envoyer à ChatGPT
    prompt = f"""
    Transforme les données du produit suivant en un tableau contenant :
    - Titre
    - Sous-titre
    - Prix
    - 4 bénéfices

    Détails du produit :
    Titre: {product_data['title']}
    Description: {product_data['description']}
    Prix: {product_data.get('price', 'Indisponible')}

    Réponds sous forme de tableau.
    """

    data = {
        "model": "gpt-4o-mini",  # Modèle à utiliser
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Erreur lors de l'appel à l'API: {response.status_code}")
        return None