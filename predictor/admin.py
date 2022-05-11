from django.contrib import admin
from .models import Data

class DataAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'height', 'sex', 'predictions')

admin.site.register(Data, DataAdmin)