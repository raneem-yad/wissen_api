from django.contrib import admin

from .models import Learner


@admin.register(Learner)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created_date")
