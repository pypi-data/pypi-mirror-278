import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate


class smtp:
    """
        This class includes all the functions required to work with SMTP server.

        setup_credentials(self, smtp_host, smtp_port, smtp_username, smtp_password)
            As a first step, user need to pass SMTP credentials for setting details in variables.

        sendmail_without_attachment(self, TO, CC, BCC, SUBJECT, BODY, FROM_EMAIL)
            Use this function when you want to send email without any attachment.

        sendmail_with_attachment(self, TO, CC, BCC, SUBJECT, BODY, ATTACHMENTS, FROM_EMAIL)
            Use this function when you want to send email with single or multiple attachments.
    """

    smtphost = None
    smtpport = None
    smtpusername = None
    smtppassword = None

    def setup_credentials(self, smtp_host, smtp_port, smtp_username, smtp_password):
        """
        Args:
            self:- Pass smtp object.
            smtp_host:- Pass SMTP hostname.
            smtp_port:- Pass SMTP port.
            smtp_username:- Pass SMTP username.
            smtp_password:- Pass SMTP password.
        """
        self.smtphost = smtp_host
        self.smtpport = smtp_port
        self.smtpusername = smtp_username
        self.smtppassword = smtp_password
        

    def sendmail_without_attachment(self, TO, CC, BCC, SUBJECT, BODY, FROM_EMAIL):
        """
        Args:
            self:- Pass smtp object.
            TO:- Pass list of email addresses seperated by semicolon (;) in TO block.
            CC:- Pass list of email addresses seperated by semicolon (;) in CC block or set this as blank("").
            BCC:- Pass list of email addresses seperated by semicolon (;) in BCC block or set this as blank("").
            SUBJECT:- Pass email subject.
            BODY:-  Pass email body content. for HTML format, start with <HTML> else this will go as plain text. 
            FROM_EMAIL:- Pass email address what you want to use for sending your email.
        """
        msg = MIMEMultipart()
        msg['To'] = TO
        msg['Cc'] = CC
        msg['Bcc'] = BCC
        msg['Subject'] = SUBJECT
        msg['From'] = FROM_EMAIL
        msg['X-Priority'] = "0"
        msg["Date"] = formatdate(localtime=True)

        if (BODY.upper().__contains__("<HTML>")):
            msg.attach(MIMEText(BODY, 'html'))
        else:
            msg.attach(MIMEText(BODY, 'plain'))

        text = msg.as_string()
        receipient = []
        receipient = (msg['To']+";"+msg['Cc']+";"+msg['Bcc']).split(";")
        receipient = filter(lambda x: x != "", receipient)
        receipient = list(receipient)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        with smtplib.SMTP_SSL(self.smtphost, self.smtpport, context=context) as smtpObj:
            smtpObj.login(self.smtpusername, self.smtppassword)
            smtpObj.sendmail(msg['From'], receipient, text)

    def sendmail_with_attachment(self, TO, CC, BCC, SUBJECT, BODY, ATTACHMENTS, FROM_EMAIL):
        """
        Args:
            self:- Pass smtp object.
            TO:- Pass list of email addresses seperated by semicolon (;) in TO block.
            CC:- Pass list of email addresses seperated by semicolon (;) in CC block or set this as blank("").
            BCC:- Pass list of email addresses seperated by semicolon (;) in BCC block or set this as blank("").
            SUBJECT:- Pass email subject.
            BODY:-  Pass email body content. for HTML format, start with <HTML> else this will go as plain text. 
            ATTACHMENTS:- This is a list, so user can pass single or multiple files. If you don't want to pass any attachment, then set input as "".
                          example: ['dir/filename1','dir/filename2'.....].
            FROM_EMAIL:- Pass email address what you want to use for sending your email.
        """
        msg = MIMEMultipart()
        msg['To'] = TO
        msg['Cc'] = CC
        msg['Bcc'] = BCC
        msg['Subject'] = SUBJECT
        msg['From'] = FROM_EMAIL
        msg['X-Priority'] = "0"
        msg["Date"] = formatdate(localtime=True)

        if (BODY.upper().__contains__("<HTML>")):
            msg.attach(MIMEText(BODY, 'html'))
        else:
            msg.attach(MIMEText(BODY, 'plain'))

        for attachfilename in ATTACHMENTS:
            fullfilename = attachfilename
            _directory, filename = os.path.split(os.path.abspath(fullfilename))
            if fullfilename != "" and fullfilename.__len__() > 0:
                attachment = open(fullfilename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition',
                             "attachment; filename= %s" % filename)
                msg.attach(p)

        text = msg.as_string()
        receipient = []
        receipient = (msg['To']+";"+msg['Cc']+";"+msg['Bcc']).split(";")
        receipient = filter(lambda x: x != "", receipient)
        receipient = list(receipient)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        with smtplib.SMTP_SSL(self.smtphost, self.smtpport, context=context) as smtpObj:
            smtpObj.login(self.smtpusername, self.smtppassword)
            smtpObj.sendmail(msg['From'], receipient, text)