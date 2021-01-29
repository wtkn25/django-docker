from django.db import models


class Product(models.Model):
    class Meta:
        db_table = 'product'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.PositiveIntegerField()
