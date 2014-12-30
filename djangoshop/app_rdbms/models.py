from django.db import models


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=90)
    date = models.DateField()
    description = models.TextField()
    image = models.CharField(max_length=255)
    inventory = models.BigIntegerField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)


class User(models.Model):

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=90)
    created = models.DateTimeField(auto_now_add=True)


class Sale(models.Model):

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)