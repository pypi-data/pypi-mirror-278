import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use the appropriate port for your SMTP server
    smtp_username = 'sohamghadge0903@gmail.com'
    smtp_password = 'nnzq twzk lsuv hfvm'
    from_email = 'sohamghadge0903@gmail.com'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, message.as_string())

# Sample email body
email_body_html = """
<html>
<head></head>
<body>
    <h1>Test Notification</h1>
    <p>This is a test email notification to confirm the email setup is working correctly.</p>
</body>
</html>
"""

# Send consolidated email notification
subject = 'Email Notification'
to_email = 'ghadgesoham934@gmail.com'  # Replace with the recipient's email address
send_email(subject, email_body_html, to_email)
