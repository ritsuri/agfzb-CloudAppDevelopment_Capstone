from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.
admin.site.register(CarModel)
admin.site.register(CarMake)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarMake
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['dealer_id', 'car_type', 'year']
    inlines = [CarModelInline]


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']


# Register models here

