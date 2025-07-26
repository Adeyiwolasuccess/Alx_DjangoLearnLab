# advanced_features_and_security/LibraryProject/bookshelf/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model
    """
    # Add the custom fields to the admin interface
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Add custom fields to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Display these fields in the list view
    list_display = UserAdmin.list_display + ('date_of_birth',)

# Register the CustomUser with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models
admin.site.register(Book)