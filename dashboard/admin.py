from django.contrib import admin
from django.db.models import fields

from dashboard import models as models 

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "domain")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("asin", "title", "domainId", "rootCategory")


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id", "category", "got", "total_asins", "getting_price_in_range",
        "started", "ended", "message", "action_button",
    )

@admin.register(models.HSNDB)
class HSBDBAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.HSNDB._meta.fields]


@admin.register(models.CurrencyRate)
class CurrencyRate(admin.ModelAdmin):
    list_display = ("domain", "rate")
