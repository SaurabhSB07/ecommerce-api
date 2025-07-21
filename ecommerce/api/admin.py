from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product,Cart,CartIteam


class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "tc", "is_admin","created_at", "updated_at","phone","address_line1","address_line2","city","state","country","postal_code","date_of_birth","gender","profile_image"]
    list_filter = ["is_admin", "id"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("User Info", {"fields": ["name", "tc","profile_image","state"]}),
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
    search_fields = ["email","id"]
    ordering = ["id"]
    filter_horizontal = []

admin.site.register(User, UserModelAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["name", "category","description","image","price", "stock", "is_active","created_at"]
    list_filter=["category","name","price"]
    ordering = ["created_at"]
    search_fields=["category","name"]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=["user","created_at"]
    search_fields=["user"]
    ordering = ["id"]

        