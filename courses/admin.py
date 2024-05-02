from django.contrib import admin

from .models import Course, VideoContent


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_name", "level", "image")
    list_filter = ("level",)


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ("video", "title", "duration")
