import http.client
import json
from django.conf import settings

RAPIDAPI_HOST = "aliexpress-data.p.rapidapi.com"
RAPIDAPI_KEY = "48d8ada1cdmsh34af8abd0529e73p19e015jsn5451399fca13"  # Remplace par ta clé

def fetch_product_data(product_id):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

    conn.request("GET", f"/product/descriptionv5?productId={product_id}&country=fr", headers=headers)
    res = conn.getresponse()

    data = res.read()

    # Ajoutez ceci pour le débogage
    print(f"Status: {res.status}")
    print(f"Response Body: {data.decode('utf-8')}")

    if res.status != 200:  # Vérifier que la requête réussie
        return {"error": "Failed to fetch data"}  # Retourner un message d'erreur

    return json.loads(data.decode("utf-8"))