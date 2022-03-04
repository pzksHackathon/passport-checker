from django.contrib import admin
from records.models import Record, FileUpload


@admin.register(Record)
class RecordModelAdmin(admin.ModelAdmin):
    list_display = (
        "series",
        "number",
        "uploaded",
        "updated",
    )

    list_filter = (
        "series",
        "uploaded",
    )


@admin.register(FileUpload)
class FileUploadModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "uploaded",
        "media",
    )
    list_filter = ("user", "uploaded", )
