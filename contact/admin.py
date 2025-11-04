from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'service_type', 'created_at', 'is_read']
    list_filter = ['service_type', 'is_read', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'message']
    readonly_fields = ['created_at', 'ip_address']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Əlaqə Məlumatları', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Mesaj Detalları', {
            'fields': ('service_type', 'message', 'is_read')
        }),
        ('Sistem Məlumatları', {
            'fields': ('created_at', 'ip_address'),
            'classes': ('collapse',)
        }),
    )
