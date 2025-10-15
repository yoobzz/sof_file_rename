import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app
import sendgrid
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

class EmailService:
    def __init__(self):
        self.sendgrid_api_key = current_app.config.get('SENDGRID_API_KEY')
        self.from_email = current_app.config.get('FROM_EMAIL', 'noreply@studentfiles.com')
    
    def send_with_sendgrid(self, to_email, subject, message, file_path=None, filename=None):
        """Wyślij email przez SendGrid"""
        try:
            if not self.sendgrid_api_key:
                return False, "Brak konfiguracji SendGrid API"
            
            sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
            
            mail = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=message
            )
            
            # Dodaj załącznik jeśli podany
            if file_path and filename and os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    data = f.read()
                    f.close()
                
                encoded_file = base64.b64encode(data).decode()
                
                attached_file = Attachment(
                    FileContent(encoded_file),
                    FileName(filename),
                    FileType('application/octet-stream'),
                    Disposition('attachment')
                )
                mail.attachment = attached_file
            
            response = sg.send(mail)
            return True, "Email wysłany pomyślnie"
            
        except Exception as e:
            return False, f"Błąd wysyłania email: {str(e)}"
    
    def send_with_smtp(self, to_email, subject, message, smtp_config, file_path=None, filename=None):
        """Wyślij email przez SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'html'))
            
            # Dodaj załącznik jeśli podany
            if file_path and filename and os.path.exists(file_path):
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}',
                )
                msg.attach(part)
            
            # Połącz z serwerem SMTP i wyślij
            server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            return True, "Email wysłany pomyślnie"
            
        except Exception as e:
            return False, f"Błąd wysyłania email: {str(e)}"
    
    def send_file_notification(self, to_email, filename, download_link=None, drive_link=None):
        """Wyślij powiadomienie o przesłanym pliku"""
        subject = f"Plik {filename} został przetworzony"
        
        message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4facfe;">📝 Plik został przetworzony!</h2>
                
                <p>Witaj!</p>
                
                <p>Twój plik <strong>{filename}</strong> został pomyślnie przetworzony i nazwa została zmieniona.</p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style="color: #28a745; margin-top: 0;">📁 Dostępne opcje:</h3>
        """
        
        if download_link:
            message += f'<p><a href="{download_link}" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">📥 Pobierz plik</a></p>'
        
        if drive_link:
            message += f'<p><a href="{drive_link}" style="background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">☁️ Zobacz na Google Drive</a></p>'
        
        message += """
                </div>
                
                <p style="font-size: 0.9em; color: #666; margin-top: 30px;">
                    Pozdrawiamy,<br>
                    Zespół Student Files
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_with_sendgrid(to_email, subject, message)
