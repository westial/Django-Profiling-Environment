from django.contrib import admin
from app_rdbms.models import Product, Sale, User

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(User)