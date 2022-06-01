import smtplib, ssl

def send_email(message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mahmoudredabs@gmail.com"
    receiver_email = "mahmoudreda457@gmail.com"
    # https://stackoverflow.com/questions/46445269/gmail-blocks-login-attempt-from-python-with-app-specific-password
    password = '*******' # "your email id's password"
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email, password)
            res = server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
            print('email sent!')
        except:
            raise
            print("could not login or send the mail.")