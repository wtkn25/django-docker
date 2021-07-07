from django.db import models


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self) -> str:
        return f"{self.name} {self.shop.name}"


class User(models.Model):
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class FavoriteBook(models.Model):
    book = models.ForeignKey(Book, db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.book} - {self.user}"


"""
これを試したかった
https://qiita.com/ykami/items/226c34853b41887df263
"""
