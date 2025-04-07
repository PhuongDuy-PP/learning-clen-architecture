import smtplib
from email.mime.text import MIMEText
from application.interfaces.email_service import EmailService
from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, EMAIL_FROM


class SMTPEmailService(EmailService):
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = EMAIL_FROM
            msg['To'] = to_email

            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False