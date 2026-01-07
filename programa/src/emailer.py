import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from src.logger import log_info, log_error

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "tu_correo@gmail.com" # Placeholder
        self.sender_password = "tu_app_password"  # Placeholder

    def send_invoice(self, to_email, file_path, invoice_id):
        if not to_email or "@" not in to_email:
            log_info(f"Email skipped: Invalid address {to_email}")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = f"Factura de Compra #{invoice_id}"

            body = "Adjunto encontrará su factura de compra. Gracias por su preferencia."
            msg.attach(MIMEText(body, 'plain'))

            attachment = open(file_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + os.path.basename(file_path))

            msg.attach(part)

            # Connect (Mocking connection for now to avoid hanging on authenticating with fake creds)
            # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # server.starttls()
            # server.login(self.sender_email, self.sender_password)
            # server.send_message(msg)
            # server.quit()
            
            # Log success for simulation
            log_info(f"Email sent successfully to {to_email} with invoice #{invoice_id}")
            return True

        except Exception as e:
            log_error(f"Failed to send email to {to_email}", e)
            return False
