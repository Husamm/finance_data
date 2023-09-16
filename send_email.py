import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PASSWORD = 'jobtkqatnghccmoy'


class EmailReport:
    sender_email = 'husamdevacc183@gmail.com'
    receiver_email = ''
    subject = ''
    attached_file_path = ''
    email_body = ''

    def send(self):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject
        message["Bcc"] = self.receiver_email

        if self.email_body != '':
            message.attach(MIMEText(self.email_body, "plain"))

        with open(self.attached_file_path, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {self.attached_file_path}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, PASSWORD)
            server.sendmail(self.sender_email, self.receiver_email, text)
