from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'full_name', 'email', 'phone', 'service_type', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_email(self, value):
        """Email validasiyası"""
        if '@' not in value:
            raise serializers.ValidationError("Düzgün email daxil edin")
        return value.lower()
    
    def validate_phone(self, value):
        """Telefon validasiyası"""
        # Sadəcə rəqəmləri qəbul et
        phone_digits = ''.join(filter(str.isdigit, value))
        if len(phone_digits) < 9:
            raise serializers.ValidationError("Düzgün telefon nömrəsi daxil edin")
        return value