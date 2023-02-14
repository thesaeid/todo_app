from django.contrib import admin
from .models import Profile, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = (
        "title",
        "status",
        "created",
        "updated",
    )
    readonly_fields = (
        "created",
        "updated",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "created",
        "updated",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    list_display_links = (
        "id",
        "title",
    )

    search_fields = ("title",)
    list_filter = (
        "status",
        "created",
        "updated",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "bio",
        "birth_date",
    )
    list_display = (
        "user",
        "bio",
        "birth_date",
    )
    list_filter = ("user",)

    list_select_related = ("user",)

    inlines = (TaskInline,)
