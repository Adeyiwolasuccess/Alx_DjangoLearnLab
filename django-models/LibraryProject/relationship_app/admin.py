from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Book
from .models import Author
from .models import Library
from .models import Librarian
from .models import UserProfile
from .models import customUser

class CustomUserAdmin(UserAdmin):
    model = customUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']


# Custom Admin Site
class RoleBasedAdminSite(admin.AdminSite):
    def has_permission(self, request):
        user = request.user
        if user.is_active and user.is_authenticated:
            try:
                return user.is_superuser or user.userprofile.role == 'Admin'
            except UserProfile.DoesNotExist:
                return user.is_superuser
        return False

# Instantiate the custom admin site
role_based_admin_site = RoleBasedAdminSite(name='role_based_admin')

# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ['role']

# Extend UserAdmin to include UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'userprofile__role']

    def get_role(self, obj):
        try:
            return obj.userprofile.role
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'

# UserProfile admin
# UserProfile admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']
# Register models with the custom admin site
role_based_admin_site.register(User, UserAdmin)
role_based_admin_site.register(Author)
role_based_admin_site.register(Book)
role_based_admin_site.register(Library)
role_based_admin_site.register(Librarian)
role_based_admin_site.register(UserProfile, UserProfileAdmin)

# Register the custom user model
admin.site.register(customUser, CustomUserAdmin)