from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=20, unique=True)  # ID Aliexpress
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    url = models.URLField()
    category_id = models.IntegerField(null=True, blank=True)
    has_stock = models.BooleanField(default=True)
    number_sold = models.CharField(max_length=20, null=True, blank=True)  # Peut contenir "+"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
