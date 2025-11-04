from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ('server', 'Server Həlləri / Server Solutions'),
        ('network', 'Şəbəkə / Network'),
        ('repair', 'Təmir / Repair'),
        ('web', 'Web Development'),
        ('security', 'IT Təhlükəsizliyi / IT Security'),
        ('cloud', 'Cloud Həlləri / Cloud Solutions'),
        ('mobile', 'Mobil Tətbiqlər / Mobile Apps'),
        ('other', 'Digər / Other'),
    ]
    
    full_name = models.CharField(max_length=200, verbose_name='Ad və Soyad')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name='Xidmət Növü')
    message = models.TextField(verbose_name='Mesaj')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Göndərilmə Tarixi')
    is_read = models.BooleanField(default=False, verbose_name='Oxunub')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Ünvan')
    
    class Meta:
        verbose_name = 'Əlaqə Mesajı'
        verbose_name_plural = 'Əlaqə Mesajları'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.service_type} - {self.created_at.strftime('%d.%m.%Y')}"
