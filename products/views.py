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
    print(f"Creating new product: {product_id}")
    # Récupérer les données via l'API
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
    # Pour les produits existants, vous pourriez éventuellement vouloir faire une mise à jour.
    print(f"Product already exists: {product_id}")

return JsonResponse({"message": "Product retrieved", "product": {
    "title": product.title,
    "description": product.description,
    "image": product.image,
    "url": product.url,
    "category_id": product.category_id,
    "has_stock": product.has_stock,
    "number_sold": product.number_sold,
}}, status=200)