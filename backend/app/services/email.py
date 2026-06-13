import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import get_settings

settings = get_settings()

def send_email(to_email: str, subject: str, html_content: str):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.from_email
    msg['To'] = to_email
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.from_email, to_email, msg.as_string())

def send_verification_email(email: str, token: str, name: str):
    verify_url = f"{settings.frontend_url}/auth/verify?token={token}"
    send_email(
        to_email=email,
        subject="Verify your Sathya account",
        html_content=f"""
        <div style="font-family: Georgia, serif; max-width: 520px; margin: 0 auto; padding: 40px 20px; color: #2c2c2a;">
            <h1 style="font-size: 24px; font-weight: 400; margin-bottom: 8px;">Welcome, {name}</h1>
            <p style="color: #6b6b68; font-size: 15px; line-height: 1.6; margin-bottom: 32px;">
                "A journey of a thousand miles begins with a single step." Verify your account to begin.
            </p>
            <a href="{verify_url}" style="display: inline-block; background: #2c2c2a; color: #f5f0e8; padding: 14px 28px; text-decoration: none; font-size: 14px; letter-spacing: 0.5px;">
                Verify my account
            </a>
            <p style="margin-top: 32px; font-size: 13px; color: #9b9b98;">
                This link expires in 24 hours. If you did not create an account, ignore this email.
            </p>
        </div>
        """
    )

def send_password_reset_email(email: str, token: str):
    reset_url = f"{settings.frontend_url}/auth/reset-password?token={token}"
    send_email(
        to_email=email,
        subject="Reset your Sathya password",
        html_content=f"""
        <div style="font-family: Georgia, serif; max-width: 520px; margin: 0 auto; padding: 40px 20px; color: #2c2c2a;">
            <h1 style="font-size: 24px; font-weight: 400; margin-bottom: 8px;">Password reset</h1>
            <p style="color: #6b6b68; font-size: 15px; line-height: 1.6; margin-bottom: 32px;">
                Click below to choose a new password. This link expires in 1 hour.
            </p>
            <a href="{reset_url}" style="display: inline-block; background: #2c2c2a; color: #f5f0e8; padding: 14px 28px; text-decoration: none; font-size: 14px; letter-spacing: 0.5px;">
                Reset password
            </a>
            <p style="margin-top: 32px; font-size: 13px; color: #9b9b98;">
                If you did not request this, ignore this email.
            </p>
        </div>
        """
    )