from django.contrib import admin

from apps.common.models import ProgrammingLanguage


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "short_name")
    prepopulated_fields = {"short_name": ("name",)}
