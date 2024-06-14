import imaplib
import email
import os
from email.mime.multipart import MIMEMultipart
import email.header
import email.policy
from datetime import datetime
from email import utils
from email.header import Header, decode_header, make_header
import mailparser  # pip install mail-parser=3.15.0
import xml.etree.cElementTree as ET


class imap:
    """
        This class includes all the functions required to work with IMAP server.

        setup_credentials(self, imap_host, imap_port, imap_username, imap_password)
            As a first step, user need to pass IMAP credentials for setting details in variables.

        email_verification(EmailSubject, FromEmail, Messageid, filter_for, prefix, postfix, within)
            Use this function when you want to know the what mail to process from given mail folder.

        download_attachments_only(self, mail_foldername, attachment_folder_location, filter_for="", prefix="", postfix="", within="")
            Use this function when you want to download email attachments only.

        purge_email(self, mail_foldername, list_of_messageid)
            Use this function when you want to delete an email from mail folder.
            Example of mail_foldername can be Inbox, Processed, Sent etc.

        move_emails(self, source_mail_foldername, destination_mail_foldername, list_of_messageid)
            Use this function when you want to delete an email from mail folder.
            Example of source_mail_foldername/destination_mail_foldername can be Inbox, Processed, Sent etc.

        save_email_data_in_xml(self, mail_foldername, xml_folder_location, filter_for="", prefix="", postfix="", within="")
            Use this function when you want to download email details in a XML file.

        save_email_data_in_xml_with_attachment_in_folder(self, mail_foldername, xml_folder_location, attachment_folder_location,filter_for="", prefix="", postfix="", within="")
            Use this function when you want to download email details in a XML file along with attachments.
    """

    imaphost = None
    imapport = None
    imapusername = None
    imappassword = None

    def setup_credentials(self, imap_host, imap_port, imap_username, imap_password):
        """
        Args:
            self:- Pass imap object.
            imap_host:- Pass IMAP hostname.
            imap_port:- Pass IMAP port.
            imap_username:- Pass IMAP username.
            imap_password:- Pass IMAP password.
        """
        self.imaphost = imap_host
        self.imapport = imap_port
        self.imapusername = imap_username
        self.imappassword = imap_password

    def email_verification(EmailSubject, FromEmail, Messageid, filter_for, prefix, postfix, within):
        """
        Args:
            EmailSubject:- Pass subject of email.
            FromEmail:- Pass from email address.
            Messageid:- Message ID of email.
            filter_for:- This is a list[]. Filter is used for what attribute (SUBJECT, FROMEMAIL).
                1. If user choose "SUBJECT" then prefix, postfix, within filter can be applied on email subject. 
                2. If user choose "FROMEMAIL" then prefix, postfix, within filter can be applied on email received from.
            prefix:- filter is used to match the starting of email SUBJECT/FROMEMAIL value.
            postfix:- filter is used to match the ending of email SUBJECT/FROMEMAIL value.
            within:- filter is used to match within the email SUBJECT/FROMEMAIL value.

            Note:- Please make sure user set the value of "prefix" or "postfix" or "within" filter if value is set for "filter_for". Such as "SUBJECT" or "FROMEMAIL".
        """
        message_id = ""

        if str(filter_for).strip() == "SUBJECT":
            EmailSubject = str(EmailSubject).strip()
            if EmailSubject.startswith(prefix.strip()) and prefix.strip() == "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() == "" and EmailSubject.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid
            elif EmailSubject.startswith(prefix.strip()) and prefix.strip() != "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() != "" and EmailSubject.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif EmailSubject.startswith(prefix.strip()) and prefix.strip() != "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() != "" and EmailSubject.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid
            elif EmailSubject.startswith(prefix.strip()) and prefix.strip() != "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() == "" and EmailSubject.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid
            elif EmailSubject.startswith(prefix.strip()) and prefix.strip() == "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() != "" and EmailSubject.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif EmailSubject.startswith(prefix.strip()) and prefix.strip() != "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() == "" and EmailSubject.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif EmailSubject.startswith(prefix.strip()) and prefix.strip() == "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() == "" and EmailSubject.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif EmailSubject.startswith(prefix.strip()) and prefix.strip() == "" and EmailSubject.endswith(postfix.strip()) and postfix.strip() != "" and EmailSubject.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid

        if str(filter_for).strip() == "FROMEMAIL":
            FromEmail = str(FromEmail).strip()
            if FromEmail.startswith(prefix.strip()) and prefix.strip() == "" and FromEmail.endswith(postfix.strip()) and postfix.strip() == "" and FromEmail.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid
            elif FromEmail.startswith(prefix.strip()) and prefix.strip() != "" and FromEmail.endswith(postfix.strip()) and postfix.strip() != "" and FromEmail.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif FromEmail.startswith(prefix.strip()) and prefix.strip() != "" and FromEmail.endswith(postfix.strip()) and postfix.strip() != "" and FromEmail.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid
            elif FromEmail.startswith(prefix.strip()) and prefix.strip() != "" and FromEmail.endswith(postfix.strip()) and postfix.strip() == "" and FromEmail.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid
            elif FromEmail.startswith(prefix.strip()) and prefix.strip() == "" and FromEmail.endswith(postfix.strip()) and postfix.strip() != "" and FromEmail.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif FromEmail.startswith(prefix.strip()) and prefix.strip() != "" and FromEmail.endswith(postfix.strip()) and postfix.strip() == "" and FromEmail.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif FromEmail.startswith(prefix.strip()) and prefix.strip() == "" and FromEmail.endswith(postfix.strip()) and postfix.strip() == "" and FromEmail.__contains__(within.strip()) and within.strip() != "":
                message_id = Messageid
            elif FromEmail.startswith(prefix.strip()) and prefix.strip() == "" and FromEmail.endswith(postfix.strip()) and postfix.strip() != "" and FromEmail.__contains__(within.strip()) and within.strip() == "":
                message_id = Messageid

        if str(filter_for).strip() == "":
            message_id = Messageid
        return message_id

    def download_attachments_only(self, mail_foldername, attachment_folder_location, filter_for="", prefix="", postfix="", within=""):
        """
        Args:
            self:- Pass imap object.
            mail_foldername:- From which folder of mailbox to download attachments. Example: INBOX, PROCESSED, SENT etc.
            attachment_folder_location:- This is a location where attachments of an email will be saved.
            filter_for:- This is a list[]. Filter is used for what attribute (SUBJECT, FROMEMAIL).
                1. If user choose "SUBJECT" then prefix, postfix, within filter can be applied on email subject. 
                2. If user choose "FROMEMAIL" then prefix, postfix, within filter can be applied on email received from.
            prefix:- filter is used to match the starting of email SUBJECT/FROMEMAIL value.
            postfix:- filter is used to match the ending of email SUBJECT/FROMEMAIL value.
            within:- filter is used to match within the email SUBJECT/FROMEMAIL value.

            Note:- Please make sure user set the value of "prefix" or "postfix" or "within" filter if value is set for "filter_for". Such as "SUBJECT" or "FROMEMAIL".
        """
        subfolder = datetime.now().strftime("%Y%m")
        attachment_folder_location = os.path.join(attachment_folder_location, subfolder)
        client = imaplib.IMAP4_SSL(self.imaphost, self.imapport)
        client.login(self.imapusername, self.imappassword)
        client.select(mail_foldername)
        tmp, data = client.uid('search', None, "ALL")
        i = len(data[0].split())
        for x in range(i):
            latest_email_uid = data[0].split()[x]
            result, email_data = client.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            FromEmail = email_message["From"]
            EmailSubject = make_header(decode_header(email_message["Subject"]))
            Messageid = int(latest_email_uid)
            mid_list = self.email_verification(EmailSubject, FromEmail, Messageid, filter_for, prefix, postfix, within)
            if Messageid == mid_list:
                for part in email_message.walk():
                    # if part.get_content_maintype() == 'multipart' and part.get('Content-Disposition') is None:
                    #     continue
                    # if part.get_content_maintype() == 'text' and part.get('Content-Disposition') is None:
                    #     continue
                    if part.get_filename() is not None:
                        filename = str(Messageid)+"_"+str(make_header(decode_header(str(part.get_filename()))))
                        if os.path.exists(attachment_folder_location):
                            pass
                        else:
                            os.makedirs(attachment_folder_location)
                        att_path = os.path.join(attachment_folder_location, filename)
                        os.path.isfile(att_path)
                        fp = open(att_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
        client.close()
        client.logout()

    def purge_email(self, mail_foldername, list_of_messageid):
        """
        Args:
            self:- Pass imap object.
            mail_foldername:- This is a folder name in IMAP account.
                              Example of mail_foldername can be Inbox, Processed, Sent etc.
            list_of_messageid:- This is a comma (,) seperated string. Pass the messageid of emails you want to delete.
        """
        client = imaplib.IMAP4_SSL(self.imaphost, self.imapport)
        client.login(self.imapusername, self.imappassword)
        client.select(mail_foldername)
        for x in str(list_of_messageid).split(","):
            client.uid('STORE', x, '+FLAGS', '\\Deleted')
            client.expunge()
        client.close()
        client.logout()

    def move_emails(self, source_mail_foldername, destination_mail_foldername, list_of_messageid):
        """
        Args:
            self:- Pass imap object.
            source_mail_foldername:- This is a folder name in IMAP account of mail source.
                                     Example of mail_foldername can be Inbox, Processed, Sent etc.
            destination_mail_foldername:- This is a folder name in IMAP account of mail destination.
                                          Example of mail_foldername can be Inbox, Processed, Sent etc.
            list_of_messageid:- This is a comma (,) seperated string. Pass the messageid of emails you want to move.
        """
        client = imaplib.IMAP4_SSL(self.imaphost, self.imapport)
        client.login(self.imapusername, self.imappassword)
        client.select(source_mail_foldername)
        for x in str(list_of_messageid).split(","):
            result  = client.uid('COPY', x, destination_mail_foldername)
            if result[0] == 'OK':
                client.uid('STORE', x, '+FLAGS', '\\Deleted')
                client.expunge()
        client.close()
        client.logout()
                               
    def save_email_data_in_xml(self, mail_foldername, xml_folder_location, filter_for="", prefix="", postfix="", within=""):
        """
        Args:
            self:- Pass imap object.
            mail_foldername:- This is a folder name in IMAP account.
                              Example of mail_foldername can be Inbox, Processed, Sent etc. 
            xml_folder_location:- Path of folder where XML file will be stored with email data.
            filter_for:- This is a list[]. Filter is used for what attribute (SUBJECT, FROMEMAIL).
                         1. If user choose "SUBJECT" then prefix, postfix, within filter can be applied on email subject. 
                         2. If user choose "FROMEMAIL" then prefix, postfix, within filter can be applied on email received from.
            prefix:- filter is used to match the starting of email SUBJECT/FROMEMAIL value.
            postfix:- filter is used to match the ending of email SUBJECT/FROMEMAIL value.
            within:- filter is used to match within the email SUBJECT/FROMEMAIL value.
        """
        subfolder = datetime.now().strftime("%Y%m")
        xml_folder_location = os.path.join(xml_folder_location, subfolder)
        client = imaplib.IMAP4_SSL(self.imaphost, self.imapport)
        client.login(self.imapusername, self.imappassword)
        client.select(mail_foldername)
        tmp, data = client.uid('search', None, "ALL")
        i = len(data[0].split())
        for x in range(i):
            attachment = []
            email_body = ""
            latest_email_uid = data[0].split()[x]
            result, email_data = client.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            FromEmail = email_message["From"]
            ToEmail = email_message["To"]
            Datesent = utils.parsedate_to_datetime(email_message["Date"]) 
            EmailSubject = make_header(decode_header(email_message["Subject"]))
            Messageid = int(latest_email_uid)
            Emailbody = mailparser.parse_from_string(raw_email_string).body
            mid_list = self.email_verification(EmailSubject, FromEmail, Messageid, filter_for, prefix, postfix, within)
            if Messageid == mid_list:
                data_filename = str(Messageid)+"_"+"Email_Detail_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".xml"
                if os.path.exists(xml_folder_location):
                    pass
                else:
                    os.makedirs(xml_folder_location)
                for part in email_message.walk():
                    if part.get_content_maintype() == 'multipart' and part.get('Content-Disposition') is None:
                        continue
                    if part.get_content_maintype() == 'text' and part.get('Content-Disposition') is None:
                        continue
                    if part.get_filename() is not None:
                        attachment.append(str(make_header(decode_header(str(part.get_filename())))))
                # print(FromEmail, ToEmail, Datesent, EmailSubject, Messageid, Emailbody, attachment)
                root = ET.Element("Email")
                ET.SubElement(root, "Fromemail").text = str(FromEmail)
                ET.SubElement(root, "Toemail").text = str(ToEmail)
                ET.SubElement(root, "Datesent").text = str(Datesent)
                ET.SubElement(root, "Emailsubject").text = str(EmailSubject)
                ET.SubElement(root, "MessageID").text = str(Messageid)
                ET.SubElement(root, "Emailbody").text = str(Emailbody)
                ET.SubElement(root, "Emailattachments").text = str(attachment).replace("[","").replace("]","")
                tree = ET.ElementTree(root)
                tree.write(xml_folder_location+"/"+data_filename)

        client.close()
        client.logout()

    def save_email_data_in_xml_with_attachment_in_folder(self, mail_foldername, xml_folder_location, attachment_folder_location,filter_for="", prefix="", postfix="", within=""):
        """
        Args:
            self:- Pass imap object.
            mail_foldername:- This is a folder name in IMAP account.
                              Example of mail_foldername can be Inbox, Processed, Sent etc. 
            xml_folder_location:- Path of folder where XML file will be stored with email data.
            attachment_folder_location:- Path of folder where email attachments will be stored.
            filter_for:- This is a list[]. Filter is used for what attribute (SUBJECT, FROMEMAIL).
                         1. If user choose "SUBJECT" then prefix, postfix, within filter can be applied on email subject. 
                         2. If user choose "FROMEMAIL" then prefix, postfix, within filter can be applied on email received from.
            prefix:- filter is used to match the starting of email SUBJECT/FROMEMAIL value.
            postfix:- filter is used to match the ending of email SUBJECT/FROMEMAIL value.
            within:- filter is used to match within the email SUBJECT/FROMEMAIL value.
        """
        subfolder = datetime.now().strftime("%Y%m")
        xml_folder_location = os.path.join(xml_folder_location, subfolder)
        attachment_folder_location = os.path.join(attachment_folder_location, subfolder)
        client = imaplib.IMAP4_SSL(self.imaphost, self.imapport)
        client.login(self.imapusername, self.imappassword)
        client.select(mail_foldername)
        tmp, data = client.uid('search', None, "ALL")
        i = len(data[0].split())
        for x in range(i):
            attachment = []
            attachments_fullpath = []
            latest_email_uid = data[0].split()[x]
            result, email_data = client.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            FromEmail = email_message["From"]
            ToEmail = email_message["To"]
            Datesent = utils.parsedate_to_datetime(email_message["Date"]) 
            EmailSubject = make_header(decode_header(email_message["Subject"]))
            Messageid = int(latest_email_uid)
            Emailbody = mailparser.parse_from_string(raw_email_string).body
            mid_list = self.email_verification(EmailSubject, FromEmail, Messageid, filter_for, prefix, postfix, within)
            if Messageid == mid_list:
                data_filename = str(Messageid)+"_"+"Email_Detail_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".xml"
                if os.path.exists(xml_folder_location):
                    pass
                else:
                    os.makedirs(xml_folder_location)
                for part in email_message.walk():
                    if part.get_content_maintype() == 'multipart' and part.get('Content-Disposition') is None:
                        continue
                    if part.get_content_maintype() == 'text' and part.get('Content-Disposition') is None:
                        continue
                    if part.get_filename() is not None:
                        attachment.append(str(make_header(decode_header(str(part.get_filename())))))
                        if os.path.exists(attachment_folder_location):
                            pass
                        else:
                            os.makedirs(attachment_folder_location)
                        for filename in attachment: 
                            att_path = os.path.join(attachment_folder_location, str(Messageid)+"_"+filename)
                            attachments_fullpath.append(att_path)
                            os.path.isfile(att_path)
                            fp = open(att_path, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                root = ET.Element("Email")
                ET.SubElement(root, "Fromemail").text = str(FromEmail)
                ET.SubElement(root, "Toemail").text = str(ToEmail)
                ET.SubElement(root, "Datesent").text = str(Datesent)
                ET.SubElement(root, "Emailsubject").text = str(EmailSubject)
                ET.SubElement(root, "MessageID").text = str(Messageid)
                ET.SubElement(root, "Emailbody").text = str(Emailbody)
                ET.SubElement(root, "Emailattachments").text = str(attachments_fullpath).replace("[","").replace("]","").replace("//","/").replace("\\\\","\\")
                tree = ET.ElementTree(root)
                tree.write(xml_folder_location+"/"+data_filename)

        client.close()
        client.logout()