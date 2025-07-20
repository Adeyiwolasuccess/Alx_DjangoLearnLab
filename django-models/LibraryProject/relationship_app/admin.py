from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Book, Author, Library, Librarian, UserProfile

# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ['role']


# Extend UserAdmin to include UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userprofile__role')
    
    def get_role(self, obj):
        try:
            return obj.userprofile.role
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'


# UserProfile admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

# ======================================================================
# START: Key Change for Role-Based Admin Access
# ======================================================================

# We no longer need the RoleBasedAdminSite class.
# Instead, we define a function to check for permission.
def has_admin_permission(request):
    """
    Allows access only to active staff members who have the 'Admin' role.
    """
    if not request.user.is_active or not request.user.is_staff:
        return False
    try:
        return request.user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False

# Override the default admin site's permission method with our custom one.
admin.site.has_permission = has_admin_permission



# Re-register User with the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile, UserProfileAdmin)