from django.contrib import admin

# Register your models here.

from rango.models import Category
from rango.models import Page

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'date')




admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
