from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Subject

class CustomUserAdmin(UserAdmin):
    # Display these fields in the list view
    list_display = ('username', 'full_name', 'user_type', 'email', 'phone_number', 'district', 'nic_photo_thumbnail', 'alevel_result_sheet_thumbnail', 'display_subjects', 'description')

    # Add filters for user type (student, teacher, admin) and district
    list_filter = ('user_type', 'district', 'medium')

    # Add fields that are editable directly in the list view
    list_editable = ('user_type', 'description',  'district','phone_number')


    # Fields to search by in the admin panel
    search_fields = ('username', 'full_name', 'email', 'phone_number')

    # Organize fieldsets in the detail view of the admin panel
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type')}),
        ('Personal Info', {'fields': ('full_name', 'age', 'phone_number', 'email', 'town', 'district', 'medium')}),
        ('Teacher Info', {'fields': ('nic_photo', 'alevel_result_sheet', 'subject', 'description')}),
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

    # Custom method to display nic_photo as a thumbnail in the admin list view
    def nic_photo_thumbnail(self, obj):
        if obj.nic_photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.nic_photo.url)
        return "No photo"
    nic_photo_thumbnail.short_description = 'NIC Photo'

    # Custom method to display alevel_result_sheet as a thumbnail in the admin list view
    def alevel_result_sheet_thumbnail(self, obj):
        if obj.alevel_result_sheet:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.alevel_result_sheet.url)
        return "No sheet"
    alevel_result_sheet_thumbnail.short_description = 'A-Level Result Sheet'

    # Custom method to display subjects as a comma-separated string
    def display_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subject.all()])
    display_subjects.short_description = 'Subjects'

# Register the custom admin for the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

# Register the Subject model if needed
admin.site.register(Subject)
