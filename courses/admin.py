from django.contrib import admin

from .models import Course


# Register your models here.
@admin.register(Course)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("course_name", "level", "image")
    list_filter = ("level",)
