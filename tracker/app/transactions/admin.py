from django.contrib import admin
from .models import User, Category, Transaction, Budget


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_superuser")


admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
