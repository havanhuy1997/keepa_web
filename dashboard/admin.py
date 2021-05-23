from django.contrib import admin

from dashboard import models as models 

admin.site.register(models.Category)
admin.site.register(models.Product)
