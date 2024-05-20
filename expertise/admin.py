from django.contrib import admin

from .models import Expertise


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ("name",)
