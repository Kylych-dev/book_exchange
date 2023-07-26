from django.contrib import admin
from . import models


@admin.register(models.UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'is_active')
    list_display_links = ('first_name', 'email')
    search_fields = ('email',)

