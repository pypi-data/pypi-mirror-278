### Package name is SFTP-SMTP-IMAP.

    This package will simplify to work with SFTP, IMAP and SMTP server with the commonly used functionalities.
    This package includes 3 classes (sftp, smtp and imap) to work with.

#### Dependency
     pip install mail-parser==3.15.0
     pip install pysftp==0.2.9

### Class sftp:-
        This class includes all the functions required to work with SFTP server.

        setup_credentials(self, sftp_host, sftp_port, sftp_username, sftp_password, sftp_remote_locatio)
            As a first step, user need to pass SFTP credentials for setting details in variables.

        list_files_directories(self, remote_location, extension, prefix, postfix, within)
            This will give list of files and directories based on criteria passed in
            extension, prefix, postfix and within parameters.

        create_remote_folder(self, remote_location, foldername)
            This function can be used to create a folder on SFTP server.

        delete_remote_folder(self, remote_location, foldername)
            This function can be used to delete a folder on SFTP server.

        rename_remote_folder(self, remote_location, old_foldername, new_foldername)
            This function can be used to rename a folder on SFTP server.

        upload_local_files(self, local_folder, remote_folder, list_of_filenames)
            This function can be used to upload single or list of files on SFTP server.

        download_remote_files(self, remote_folder, local_folder, list_of_filenames)
            This function can be used to download single or list of files from SFTP server to local server/machine.

        rename_remote_file(self, remote_location, old_filename, new_filename)
            This function can be used to rename a file on SFTP server.

        delete_remote_files(self, remote_location, list_of_filenames)
            This function can be used to delete a single or list of files on SFTP server.



### Class smtp:-
        This class includes all the functions required to work with SMTP server.

        setup_credentials(self, smtp_host, smtp_port, smtp_username, smtp_password)
            As a first step, user need to pass SMTP credentials for setting details in variables.

        sendmail_without_attachment(self, TO, CC, BCC, SUBJECT, BODY, FROM_EMAIL)
            Use this function when you want to send email without any attachment.

        sendmail_with_attachment(self, TO, CC, BCC, SUBJECT, BODY, ATTACHMENTS, FROM_EMAIL)
            Use this function when you want to send email with single or multiple attachments.



### Class imap:-
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



## How to use this project: 

### For SFTP
   - from sftp.sftp import sftp

   - sftp.setup_credentials(sftp, "", , "", "")  #Mandatory to use

   - sftp.list_files_directories(sftp, "")
   - sftp.create_remote_folder(sftp,"/","")
   - sftp.delete_remote_files(sftp, "", [""])
   - sftp.rename_remote_folder(sftp, "", "", "")
   - sftp.download_remote_files(sftp, "", "", [""])
   - sftp.upload_local_files(sftp, "", "", [""])
   - sftp.rename_remote_file(sftp, "","","")
   - sftp.delete_remote_files(sftp, "", [""])

### For SMTP
   - from smtp.smtp import smtp

   - smtp.setup_credentials(smtp,"", , "", "")    #Mandatory to use

   - smtp.sendmail_without_attachment(smtp, "", "", "", "", "", "")
   - smtp.sendmail_with_attachment(smtp, "", "", "", "", "", [""], "")

### For IMAP
   - from imap.imap import imap

   - imap.setup_credentials(imap, "","" , "", "")   #Mandatory to use

   - imap.download_attachments_only(imap, "", "", filter_for="", prefix="", postfix="", within="")
   - imap.purge_email(imap, "", "")
   - imap.move_emails(imap, "", "AIR", "")
   - imap.save_email_data_in_xml(imap, "", "", filter_for="", prefix="", postfix="", within="")
   - imap.save_email_data_in_xml_with_attachment_in_folder(imap, "", "", "", filter_for="", prefix="", postfix="", within="")



This package is developed by Sunesh Pandita.
GitHub repo:- [Link](https://github.com/SUNESHPANDITA/sftp-smtp-imap-package.git) 
