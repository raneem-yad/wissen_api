from django.contrib import admin

from .models import Instructor


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created_date")
    list_filter = ("job_title",)
