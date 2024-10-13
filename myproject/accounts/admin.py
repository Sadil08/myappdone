from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subject

class CustomUserAdmin(UserAdmin):
    # Display these fields in the list view
    list_display = ('username', 'full_name', 'user_type', 'email', 'phone_number', 'district')

    # Add filters for user type (student, teacher, admin) and district
    list_filter = ('user_type', 'district', 'medium')

    # Add fields that are editable directly in the list view
    list_editable = ('user_type',)

    # Fields to search by in the admin panel
    search_fields = ('username', 'full_name', 'email', 'phone_number')

    # Organize fieldsets in the detail view of the admin panel
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type')}),
        ('Personal Info', {'fields': ('full_name', 'age', 'phone_number', 'email', 'town', 'district', 'medium')}),
        ('Teacher Info', {'fields': ('nic_photo', 'alevel_result_sheet', 'subject')}),
        ('Student Info', {'fields': ('alevel_batch_year',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Configure the 'Add user' form fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )

# Register the custom admin for the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

# Register the Subject model if needed
admin.site.register(Subject)
