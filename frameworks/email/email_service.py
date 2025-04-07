import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from application.interfaces.email_service import EmailService

class SMTPEmailService(EmailService):
    def __init__(self):
        self.smtp_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('EMAIL_PORT', '587'))
        self.smtp_user = os.getenv('EMAIL_USER')
        self.smtp_password = os.getenv('EMAIL_PASSWORD')
        self.from_email = os.getenv('EMAIL_FROM')

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            message = MIMEMultipart()
            message["From"] = self.from_email
            message["To"] = to_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)

            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def send_welcome_email(self, to_email: str, username: str) -> bool:
        subject = "Welcome to Our Service!"
        body = f"""
        Hi {username},

        Welcome to our service! We're excited to have you on board.

        Best regards,
        The Team
        """
        return self.send_email(to_email, subject, body) 