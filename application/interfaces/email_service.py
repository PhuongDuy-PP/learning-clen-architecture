from abc import ABC, abstractmethod

class EmailService(ABC):

    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str) -> None:
        """Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
            
        Raises:
            ValueError: If email sending fails
        """
        pass