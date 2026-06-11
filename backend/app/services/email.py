import resend
from app.core.config import get_settings

settings = get_settings()
resend.api_key = settings.resend_api_key

def send_verification_email(email: str, token: str, name: str):
    verify_url = f"{settings.frontend_url}/auth/verify?token={token}"
    resend.Emails.send({
        "from": settings.from_email,
        "to": email,
        "subject": "Verify your Sathya account",
        "html": f"""
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
    })

def send_password_reset_email(email: str, token: str):
    reset_url = f"{settings.frontend_url}/auth/reset-password?token={token}"
    resend.Emails.send({
        "from": settings.from_email,
        "to": email,
        "subject": "Reset your Sathya password",
        "html": f"""
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
    })