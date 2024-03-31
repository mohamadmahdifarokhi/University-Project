import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from redis import Redis

from ..logger import logger

load_dotenv()


class EmailSender:
    """
    Service class for sending emails.

    Attributes:
        smtp_server (str): The SMTP server address.
        smtp_port (int): The SMTP server port.
        smtp_username (str): The SMTP server username.
        smtp_password (str): The SMTP server password.
        sender_email (str): The email address of the sender.
        frontend_server_url (str): The frontend server URL.

    Methods:
        send_email: Send a generic email with the specified subject, recipient, and body.
        send_otp_email: Send an OTP email to the specified email address.
        send_token_email: Send a password reset token email to the specified email address.
    """

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.frontend_server_url = os.getenv("FRONTEND_SERVER_URL")

    def send_email(self, subject: str, recipient: str, body: str) -> None:
        """
        Send an email with the specified subject, recipient, and body.

        Args:
            subject (str): The subject of the email.
            recipient (str): The email address of the recipient.
            body (str): The body of the email.

        Raises:
            HTTPException: If there is an issue with sending the email.
        """
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                text = message.as_string()
                server.sendmail(self.sender_email, recipient, text)
            logger.info(f"Email sent to {recipient}")
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            raise HTTPException(status_code=500, detail="Failed to send email")

    def send_otp_email(self, email: str, otp_code: int) -> None:
        """
        Send an OTP email to the specified email address.

        Args:
            email (str): The recipient's email address.
            otp_code (int): The OTP code to be sent.

        Raises:
            HTTPException: If there is an issue with sending the email.
        """
        subject = "OTP Code"
        body = f"Your OTP code is: {otp_code}"
        self.send_email(subject, email, body)

    def send_token_email(self, email: str, token: uuid) -> None:
        """
        Send a password reset token email to the specified email address.

        Args:
            email (str): The recipient's email address.
            token (uuid): The password reset token to be sent.

        Raises:
            HTTPException: If there is an issue with sending the email.
        """
        subject = "Password Reset Token"
        body = f"Use the following token to reset your password: {self.frontend_server_url}/recover/{token}"
        self.send_email(subject, email, body)


redis_instance = Redis()

