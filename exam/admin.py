from django.contrib import admin

from .models import ExamApplication, ExamCenter, ExamConfig


@admin.register(ExamConfig)
class ExamConfigAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "applications_open", "admit_download_open"]


@admin.register(ExamCenter)
class ExamCenterAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "order", "is_active"]


@admin.register(ExamApplication)
class ExamApplicationAdmin(admin.ModelAdmin):
    list_display = ["application_no", "name_en", "class_level", "status", "roll_no", "exam_year"]
    list_filter = ["exam_year", "status", "class_level", "center"]
    search_fields = ["application_no", "name_bn", "name_en", "phone", "trx_id"]
