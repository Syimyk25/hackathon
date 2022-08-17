from django.contrib import admin

from applications.cars.models import CarClass, Car, Travel, Image, Rating, Like

admin.site.register(Car)
admin.site.register(Like)
admin.site.register(Rating)


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 5


class CarClassAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(CarClass, CarClassAdmin)


class TravelAdmin(admin.ModelAdmin):
    list_display = ['owner', 'travel_to']


admin.site.register(Travel, TravelAdmin)