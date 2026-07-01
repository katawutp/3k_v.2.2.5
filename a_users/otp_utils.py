import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def generate_otp_code(length=6):
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(user_email, otp_code, username=None):
    """Send OTP via email using SendGrid"""
    subject = "Your 3kok Verification Code"
    message = f"""
Hello {username or 'User'},

Your verification code for 3kok is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
3kok Team
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False

def store_otp_in_session(request, otp_code, expiry_minutes=10):
    """Store OTP in session"""
    request.session['otp_code'] = otp_code
    request.session['otp_expiry'] = (timezone.now() + timedelta(minutes=expiry_minutes)).isoformat()

def verify_otp(request, user_input_otp):
    """Verify the OTP code from session"""
    stored_otp = request.session.get('otp_code')
    stored_expiry = request.session.get('otp_expiry')
    
    if not stored_otp or not stored_expiry:
        return False, "No OTP found. Please request a new code."
    
    try:
        expiry_time = timezone.datetime.fromisoformat(stored_expiry)
        if timezone.now() > expiry_time:
            request.session.pop('otp_code', None)
            request.session.pop('otp_expiry', None)
            return False, "OTP has expired. Please request a new code."
    except ValueError:
        return False, "Invalid session data. Please request a new code."
    
    if user_input_otp == stored_otp:
        request.session.pop('otp_code', None)
        request.session.pop('otp_expiry', None)
        return True, "OTP verified successfully"
    
    return False, "Invalid OTP code. Please try again."
