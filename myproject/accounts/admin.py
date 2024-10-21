from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Subject
from .models import Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'created_at')
    search_fields = ('text', 'author__username')
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'question', 'created_at')
    search_fields = ('text', 'author__username', 'question__text')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'user_type', 'email', 'phone_number', 'district', 'nic_photo_link', 'alevel_result_sheet_link', 'display_subjects', 'description')
    list_filter = ('user_type', 'district', 'medium')
    list_editable = ('user_type', 'description', 'district', 'phone_number')
    search_fields = ('username', 'full_name', 'email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type')}),
        ('Personal Info', {'fields': ('full_name', 'age', 'phone_number', 'email', 'town', 'district', 'medium')}),
        ('Teacher Info', {'fields': ('nic_photo', 'alevel_result_sheet', 'subject', 'description')}),
        ('Student Info', {'fields': ('alevel_batch_year',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )

    def nic_photo_link(self, obj):
        if obj.nic_photo:
            return format_html('<a href="{}" target="_blank">View NIC Photo</a>', obj.nic_photo.url)
        return "No photo"
    nic_photo_link.short_description = 'NIC Photo'

    def alevel_result_sheet_link(self, obj):
        if obj.alevel_result_sheet:
            return format_html('<a href="{}" target="_blank">View A-Level Result Sheet</a>', obj.alevel_result_sheet.url)
        return "No sheet"
    alevel_result_sheet_link.short_description = 'A-Level Result Sheet'

    def display_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subject.all()])
    display_subjects.short_description = 'Subjects'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)

