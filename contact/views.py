from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactMessage
from .serializers import ContactMessageSerializer

def get_client_ip(request):
    """IP ünvanı əldə et"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['POST'])
def contact_submit(request):
    """Əlaqə formu göndərmə"""
    
    serializer = ContactMessageSerializer(data=request.data)
    
    if serializer.is_valid():
        # IP ünvanı əlavə et
        contact_message = serializer.save(ip_address=get_client_ip(request))
        
        # Email göndər
        try:
            send_contact_emails(contact_message)
            
            return Response({
                'success': True,
                'message': 'Mesajınız uğurla göndərildi! Tezliklə sizinlə əlaqə saxlayacağıq.',
                'message_en': 'Your message has been sent successfully! We will contact you soon.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception:
            # Email göndərilməsə belə, mesaj database-ə yazılır
            return Response({
                'success': True,
                'message': 'Mesajınız qeydə alındı.',
                'warning': 'Email göndərilməsində xəta',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Xəta baş verdi. Zəhmət olmasa məlumatları yoxlayın.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


def send_contact_emails(contact_message):
    """Admin və müştəriyə email göndər"""
    
    # 1. Admin üçün email
    admin_subject = f'Yeni Əlaqə Mesajı - {contact_message.service_type}'
    admin_message = f"""
    Yeni əlaqə mesajı alındı:
    
    Ad və Soyad: {contact_message.full_name}
    Email: {contact_message.email}
    Telefon: {contact_message.phone}
    Xidmət: {contact_message.get_service_type_display()}
    
    Mesaj:
    {contact_message.message}
    
    Tarix: {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}
    IP: {contact_message.ip_address}
    """
    
    send_mail(
        subject=admin_subject,
        message=admin_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )
    
    # 2. Müştəri üçün təsdiq emaili (HTML format)
    customer_subject = 'Oghuz Company - Mesajınız Alındı / Message Received'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; 
                        border-left: 4px solid #667eea; }}
            .footer {{ text-align: center; color: #666; padding: 20px; font-size: 14px; }}
            .btn {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none; 
                    border-radius: 5px; display: inline-block; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Oghuz Company</h1>
                <p>Professional IT Xidmətləri</p>
            </div>
            <div class="content">
                <h2>🎉 Hörmətli {contact_message.full_name},</h2>
                <p>Mesajınız bizə uğurla çatdı! Tezliklə sizinlə əlaqə saxlayacağıq.</p>
                
                <div class="info-box">
                    <h3>📋 Mesaj Məlumatları:</h3>
                    <p><strong>Xidmət:</strong> {contact_message.get_service_type_display()}</p>
                    <p><strong>Email:</strong> {contact_message.email}</p>
                    <p><strong>Telefon:</strong> {contact_message.phone}</p>
                    <p><strong>Tarix:</strong> {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}</p>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                
                <h2>🎉 Dear {contact_message.full_name},</h2>
                <p>Your message has been successfully received! We will contact you soon.</p>
                
                <div style="text-align: center;">
                    <a href="tel:+994508816613" class="btn">📞 Bizimlə Əlaqə / Contact Us</a>
                </div>
            </div>
            <div class="footer">
                <p>© 2025 Oghuz Company. Bütün hüquqlar qorunur.</p>
                <p>📧 info@techpro.az | 📱 +994 50 881 66 13</p>
                <p>📍 Bakı, Azərbaycan</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    email = EmailMultiAlternatives(
        subject=customer_subject,
        body=f"Hörmətli {contact_message.full_name}, mesajınız bizə çatdı!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[contact_message.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
