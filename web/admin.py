from django.contrib import admin

from .models import Food, Meal, user_properties

admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(user_properties)
