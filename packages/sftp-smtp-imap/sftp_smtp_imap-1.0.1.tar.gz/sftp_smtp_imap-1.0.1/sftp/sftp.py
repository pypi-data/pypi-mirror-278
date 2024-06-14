import pysftp  # pip install pysftp=0.2.9


class sftp:
    """
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
    """

    sftphost = None
    sftpport = None
    sftpusername = None
    sftppassword = None

    def split_filename_extention(filename):
        filename_dirname = ""
        filename_dirname_extension = ""
        if filename.find(".") > 0:
            filename_dirname = filename[0:filename.find(".")]
            filename_dirname_extension = filename[filename.find("."):]
        else:
            filename_dirname = filename
        return filename_dirname, filename_dirname_extension

    def setup_credentials(self, sftp_host, sftp_port, sftp_username, sftp_password):
        """
        Args:
            self:- Pass SFTP object.
            sftp_host:- Pass SFTP hostname.
            sftp_port:- Pass SFTP port.
            sftp_username:- Pass SFTP username.
            sftp_password:- Pass SFTP password.
            sftp_remote_location:- Pass SFTP remote location.
        """

        self.sftphost = sftp_host
        self.sftpport = sftp_port
        self.sftpusername = sftp_username
        self.sftppassword = sftp_password

    def list_files_directories(self, remote_location, extension="", prefix="", postfix="", within=""):
        """
            Args:
                self:- Pass SFTP object.
                extension:- filter is used for files extension.
                prefix:- filter is used to match the starting of files or folders name.
                postfix:- filter is used to match the ending of files or folders name.
                within:- filter is used to match within the files or folders name.
        """
        cnopts = pysftp.CnOpts()
        list_files_directory = []
        cnopts.hostkeys = None
        SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                 password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
        SFTP.chdir(remote_location)
        for i in SFTP.listdir():
            filename = ""
            file_extension = ""
            filename, file_extension = self.split_filename_extention(i)

            if file_extension == extension and extension.strip() != "":
                list_files_directory.append(i)
            if filename.startswith(prefix.strip()) and prefix.strip() != "":
                list_files_directory.append(i)
            if filename.endswith(postfix.strip()) and postfix.strip() != "":
                list_files_directory.append(i)
            if i.__contains__(within.strip()) and within.strip() != "":
                list_files_directory.append(i)

            if extension.strip() == "" and prefix.strip() == "" and postfix.strip() == "" and within.strip() == "":
                list_files_directory.append(i)

            list_files_directory = list(set(list_files_directory))
        SFTP.close()
        return list_files_directory

    def create_remote_folder(self, remote_location, foldername):
        """
            Args:
                self:- Pass SFTP object.
                remote_location:- remote location on SFTP server.
                foldername:- folder name which you want to create.
        """
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                     password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
            SFTP.chdir(remote_location)
            try:
                SFTP.mkdir(foldername)
                print("Folder created successfully on SFTP server")
            except Exception as E:
                print("Unable to create folder on SFTP! " + str(E))
            finally:
                SFTP.close()
        except Exception as E:
            print("Invalid details. Please verify your credentials! "+str(E))

    def delete_remote_folder(self, remote_location, foldername):
        """
            Args:
                self:- Pass SFTP object.
                remote_location:- remote location on SFTP server.
                foldername:- folder name which you want to delete. Note: folder should be blank.
        """
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                     password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
            SFTP.chdir(remote_location)
            try:
                SFTP.rmdir(foldername)
                print("Folder removed successfully on SFTP server")
            except Exception as E:
                print("Unable to remove folder on SFTP! " + str(E))
            finally:
                SFTP.close()
        except Exception as E:
            print("Invalid details. Please verify your credentials! "+str(E))

    def rename_remote_folder(self, remote_location, old_foldername, new_foldername):
        """
            Args:
                self:- Pass SFTP object.
                remote_location:- remote location on SFTP server.
                old_foldername:- existing foldername on server.
                new_foldername:- new foldername on server.
        """
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                     password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
            SFTP.chdir(remote_location)
            try:
                SFTP.rename(old_foldername, new_foldername)
                print("Folder rename successfully done on SFTP server")
            except Exception as E:
                print("Unable to rename folder on SFTP! " + str(E))
            finally:
                SFTP.close()
        except Exception as E:
            print("Invalid details. Please verify your credentials! "+str(E))

    def upload_local_files(self, local_folder, remote_folder, list_of_filenames):
        """
            Args:
                self:- Pass SFTP object.
                local_folder:- local folder on your system/server.
                remote_folder:- remote location on SFTP server.
                list_of_filenames:- This is a list[]. This can have a single or multiple file names
                                    with "," as a seperator.
                                    Example:- ["filename1", "filename2",.......] 
        """
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                     password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
            for filename in list_of_filenames:
                try:
                    SFTP.put(str(local_folder+'/').replace("//", "/")+filename,
                             str(remote_folder+'/').replace("//", "/")+filename)
                    print("File "+(str(local_folder+"/").replace("//", "/") +
                          filename)+" uploaded successfully on SFTP server.")
                except Exception as E:
                    print("Unable to upload file on SFTP! " + str(E))
            SFTP.close()
        except Exception as E:
            print("Invalid details. Please verify your credentials! "+str(E))

    def download_remote_files(self, remote_folder, local_folder, list_of_filenames):
        """
            Args:
                self:- Pass SFTP object.
                local_folder:- local folder on your system/server.
                remote_folder:- remote location on SFTP server.
                list_of_filenames:- This is a list[]. This can have a single or multiple file names
                                    with "," as a seperator.
                                    Example:- ["filename1", "filename2",.......] 
        """
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                     password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
            for filename in list_of_filenames:
                try:
                    if SFTP.exists(str(remote_folder+'/').replace("//", "/")+filename):
                        SFTP.get(str(remote_folder+'/').replace("//", "/")+filename,
                                 str(local_folder+'/').replace("//", "/")+filename)
                        print("File "+(str(remote_folder+"/").replace("//", "/") +
                              filename)+" downloaded successfully on local server.")
                    else:
                        print("Filename ("+str(remote_folder+"/").replace("//",
                              "/")+filename+") does not exists on SFTP.")
                except Exception as E:
                    print("Unable to download file on local server! " + str(E))
            SFTP.close()
        except Exception as E:
            print("Invalid details. Please verify your credentials! "+str(E))

    def rename_remote_file(self, remote_location, old_filename, new_filename):
        """
            Args:
                self:- Pass SFTP object.
                remote_location:- remote location on SFTP server.
                old_filename:- existing filename on server.
                new_filename:- new filename on server.
        """
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                     password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
            SFTP.chdir(remote_location)
            try:
                SFTP.rename(old_filename, new_filename)
                print("File ("+str(old_filename)+" renamed to " +
                      new_filename+") successfully done on SFTP server")
            except Exception as E:
                print("Unable to rename file on SFTP! " + str(E))
            finally:
                SFTP.close()
        except Exception as E:
            print("Invalid details. Please verify your credentials! "+str(E))

    def delete_remote_files(self, remote_location, list_of_filenames):
        """
            Args:
                self:- Pass SFTP object.
                remote_location:- remote location on SFTP server.
                list_of_filenames:- This is a list[]. This can have a single or multiple file names
                                    with "," as a seperator.
                                    Example:- ["filename1", "filename2",.......] 
        """
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            SFTP = pysftp.Connection(host=self.sftphost, username=self.sftpusername,
                                     password=self.sftppassword, cnopts=cnopts, port=int(self.sftpport))
            for filename in list_of_filenames:
                try:
                    SFTP.remove(
                        str(remote_location+'/').replace("//", "/")+filename)
                    print("File deleted successfully on SFTP server")
                except Exception as E:
                    print("Unable to delete file on SFTP! " + str(E))
            SFTP.close()
        except Exception as E:
            print("Invalid details. Please verify your credentials! "+str(E))