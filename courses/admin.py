from django.contrib import admin

from .models import Course, VideoContent, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_name", "level", "image")
    list_filter = ("level",)


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ("video", "title", "duration")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "enrolled_date")