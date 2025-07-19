from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "tc", "is_admin", "created_at", "updated_at"]
    list_filter = ["is_admin", "id"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("User Info", {"fields": ["name", "tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(User, UserModelAdmin)