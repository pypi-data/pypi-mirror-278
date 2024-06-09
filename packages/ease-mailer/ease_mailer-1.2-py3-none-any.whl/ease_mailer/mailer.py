import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    """This class is used to send emails to users
    :param source_mail: The email address of the user that will send the email
    :param passwd: The password of the user that will send the email
    """
    def __init__(self, source_mail, passwd):
        self.source_mail = source_mail
        self.passwd = passwd
        self.conn_status = None
        self.mail_status = None
        self.server = None

    def send_mail(self, to_email, subject, body):
        """This function sends an email to the user
        :param to_email: The email address of the user to send the email to
        :param subject: The subject of the email
        :param body: The body of the email
        :return: True if the email was sent successfully, False otherwise
        """
        try:
            if self.conn_status:
                msg = MIMEMultipart()
                msg['From'] = self.source_mail
                msg['To'] = self.source_mail
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))  # Change 'html' to 'plain'
                text = msg.as_string()
                self.server.sendmail(self.source_mail, to_email, text)
                self.server.quit()
                self.mail_status = True
            else:
                raise Exception(
                    "Connection to server failed. Please check your credentials and try again\nFor Help, type help()")
        except Exception as e:
            print(e)
            self.mail_status = False
        finally:
            return self.mail_status

    def show_status(self):
        """This function shows the conn_status of the email
        :param conn_status: The conn_status of the email
        :return: The conn_status of the email
        """
        if self.mail_status:
            return "Email sent successfully"
        else:
            return "Email failed to send"

    def login(self):
        """This function checks the connection to the server checks the user's credentials and logs the user in
        :return: True if the connection was successful, False otherwise
        """
        try:
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.source_mail, self.passwd)
            self.conn_status = True
        except Exception as e:
            print(e)
            self.conn_status = False
        finally:
            return self.conn_status

    @staticmethod
    def help():
        """This function shows the documentation of the class
        :return: The documentation of the class
        """
        print("""class Mail parameters:
        source_mail: The email address of the user that will send the email
        passwd: The password of the user that will send the email
        password should be an app password if you can't access your account 
        Visit https://myaccount.google.com/apppasswords for more information on how to generate an app password
        
        class Mail functions:
        send_mail(to_email, subject, body): This function sends an email to the user
        show_status(): This function shows the mail status of the email
        login(): This function checks the connection to the server checks the user's credentials and logs the user in
        help(): This function shows the documentation of the class""")

