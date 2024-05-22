from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)


class Stars(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  #позволяет оставлять поле пустым
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
