from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product,Cart,CartItem,Order,OrderItem,Review

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

class ReviewInline(admin.TabularInline):  
    model = Review
    extra = 0 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display=["name", "category","description","image","price", "stock", "is_active","created_at"]
    list_filter=["category","name","price"]
    ordering = ["created_at"]
    search_fields=["category","name"]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=["user","created_at"]
    search_fields=["user"]
    ordering = ["id"]

@admin.register(CartItem)
class CartIteamAdmin(admin.ModelAdmin):
    list_display=['cart','product','added_at','quantity']
    search_fields=['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "shipping_address")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price_at_purchase")
    list_filter = ("product",)
    search_fields = ("order__id", "product__name")

class ReviewInline(admin.TabularInline):  
    model = Review
    extra = 0 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=["user","product","review","description",'created_at']
    list_filter=['product']
    search_fields=['product__name',"user__name"]
    filter_horizontal=[]
