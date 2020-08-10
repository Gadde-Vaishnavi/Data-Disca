# Importing the libraries required
import os
from os import path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders


class EmailClient:

    def __init__(self, server: str, server_port: int, user_name: str, password: str):
        """
        This method is used for initialising and declaring variables
        required for sending an email using smtp library

        @server: The address of the smtp email server provider
        @server_port: A networking port number
        @username: Username of the client
        @password: Password of the client

        """
        # Server information
        self.server = server
        self.server_port = server_port

        # The client Email credentials
        self.user_name = user_name
        self.password = password

        # This can be used to send messages which has different contents
        self.email = MIMEMultipart()

        # Initialising the variables
        self.subject = False
        self.body = False
        self.attached = False
        self.signature = False

    def set_subject(self, subject: str):
        """
        In this method we add the subject to the email
        @subject: The subject in an email
        """
        if (subject is not None) & (len(subject) > 0):  # An if condition to check the user does not send an email with
            # an empty subject
            self.subject = True
            self.email['Subject'] = subject

    def set_body(self, body: str):
        """
        In this method we add the body to the email
        @body: The content of the mail
        """
        if (body is not None) & (len(body) > 0):  # An if condition to check the user does not send an email with an
            # empty body
            self.body = True
            self.email.attach(MIMEText(body))

    def set_signature(self, signature: str):
        """
        In this method we add the clients signature to the email
        @signature: Email signature
        """
        if (signature is not None) & (len(signature) > 0):  # An if condition to check the user does not send an
            # email with an empty signature
            self.signature = True
            self.email.attach(MIMEText(signature, 'plain'))  # Using MIME text we attach the clients signature to the
            # email the signature can be in any formats such as either text or html.

    def add_attachment(self, attachment_path: str):
        """
        In this method we add the attachments to the email
        @attachment_path: The path of the attachments file
        """
        if path.exists(attachment_path):  # Using if condition we check if the given attachment path exists
            self.attached = True
            if path.isfile(attachment_path):  # Using if condition we check if the given path is a file
                part = MIMEBase('application', "octet-stream")
                with open(attachment_path, 'rb') as input_file:  # Opening and reading the file in binary format
                    part.set_payload(input_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(attachment_path))
                self.email.attach(part)
            else:
                raise Exception("Please give a file as input")
        else:
            raise Exception("FileNotFoundError:")  # If the given path is incorrect we raise an error

    def send(self, recipient: str) -> bool:
        """
        In this Method we send the email to the recipient
        @recipient: The email address of the receiver
        """
        if self.attached and not self.subject:  # If condition to check that the mail has a subject and attachment
            raise Exception('Error: There is No subject')

        elif not self.subject and not self.body and not self.signature:  # If condition to check that the mail has
            # subject, body and signature
            raise Exception('Error: Email can not send without subject, body or signature')

        # Sender and receiver information
        self.email['From'] = self.user_name
        self.email['To'] = recipient
        self.email['Date'] = formatdate(localtime=True)

        try:
            with smtplib.SMTP_SSL(host=self.server, port=self.server_port) as mail_service:
                mail_service.login(self.user_name, self.password)
                mail_service.send_message(self.email)
                return True
        except OSError as e:
            print('Could\'t send email something went wrong please check your email credentials. \n', e)

    def reset_email(self):
        """
        In this method we reset all the variables
        """
        self.email = MIMEMultipart()  # This can be used to send messages which has different contents
        self.email['From'] = self.user_name  # Clients user email

        # Initialising the variables
        self.subject = False
        self.body = False
        self.attached = False
        self.signature = False


if __name__ == "__main__":

    # The Server details
    server = 'smtp.zoho.com.au'
    port = 535

    # Opening the client credentials
    with open('client_credentials.txt', 'r') as input_file:
        username, password = input_file.read().split(',')

    # The contents to be emailed
    mail_subject = "Server Performance"

    # The body of the email
    mail_body = '*********** #CPU Information ***********'
    os.system('cat /proc/cpuinfo > cpu_info.txt')
    with open('cpu_info.txt', 'r') as cpu_info:
        for line in cpu_info.readlines():
            mail_body += line

    mail_body += '*********** #Memory Information ***********'
    os.system('cat /proc/meminfo > memory_info.txt')
    with open('memory_info.txt', 'r') as memory_info:
        for line in memory_info.readlines():
            mail_body += line

    # The email attachment
    os.system('ps -aux > running_process.txt')
    mail_attachment = 'running_process.txt'

    # Calling the class to send an email.
    email_client = EmailClient(server, port, username, password)
    email_client.set_subject(mail_subject)
    email_client.set_body(mail_body)
    email_client.set_signature('\n\nRegards, \nGadde Vaishnavi.')
    email_client.add_attachment(mail_attachment)

    # The recipient
    recipient = 'gaddevaishnavi12@gmail.com'

    if email_client.send(recipient):
        print('Message Sent')
        email_client.reset_email()
    else:
        raise Exception('Failed to send the message.')
