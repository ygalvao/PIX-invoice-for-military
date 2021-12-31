import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_data = {
    'server' : 'smtp.gmail.com',
    'port' : '587',
    'sender' : 'yhgalvao@gmail.com',
    'password' : 'mlsqlrnfdkoyglzy',
    'receiver' : 'yuri@yurigalvao.com.br'
    }

def send_email(iteration, smtp_data):
    smtp_server = smtp_data['server']
    port = smtp_data['port']
    sender_email = smtp_data['sender']
    receiver_email = smtp_data['receiver']
    password = smtp_data['password']

    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "document.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        message = '''Subject: Test!!
This is a test! ;D'''
        
        with smtplib.SMTP(smtp_server, port) as server:
##            server.connect(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        
    else:
        print('Email ', iteration, ' sent!')
        
##    finally:
##        server.quit()

if __name__ == '__main__':
    send_email(0, smtp_data)
