from django.urls import path
from .views import get_or_create_product

urlpatterns = [
    path("get-product/", get_or_create_product, name="get_product"),
]
