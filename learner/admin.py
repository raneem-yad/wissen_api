from django.contrib import admin

from .models import Learner


@admin.register(Learner)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("full_name","get_owner_username", "created_date")

    def get_owner_username(self, obj):
        return obj.owner.username

    get_owner_username.short_description = 'Owner Username'
