from abc import ABC, abstractmethod

class EmailService(ABC):

    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send an email to a recipient

        Args:
            to_email: The recipient's email address
            subject: The email subject
            body: The email body content

        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        pass