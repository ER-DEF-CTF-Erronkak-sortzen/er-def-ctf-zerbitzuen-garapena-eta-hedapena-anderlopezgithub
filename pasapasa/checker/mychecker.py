#!/usr/bin/env python3

from ctf_gameserver import checkerlib
import logging
import http.client
import socket
import paramiko
import hashlib
import time

PORT_WEB = 80
PORT_SSH = 8822
PORT_FTP = 21
PORT_DB = 3306
def ssh_connect():
    def decorator(func):
        def wrapper(*args, **kwargs):
            # SSH connection setup
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rsa_key = paramiko.RSAKey.from_private_key_file(f'/keys/team{args[0].team}-sshkey')
            client.connect(args[0].ip, username = 'root', pkey=rsa_key)

            # Call the decorated function with the client parameter
            args[0].client = client
            result = func(*args, **kwargs)

            # SSH connection cleanup
            client.close()
            return result
        return wrapper
    return decorator

class MyChecker(checkerlib.BaseChecker):

    def __init__(self, ip, team):
        checkerlib.BaseChecker.__init__(self, ip, team)
        self._baseurl = f'http://[{self.ip}]:{PORT_WEB}'
        logging.info(f"URL: {self._baseurl}")

    @ssh_connect()
    def place_flag(self, tick):
        flag = checkerlib.get_flag(tick)
        creds = self._add_new_flag(self.client, flag)
        if not creds:
            return checkerlib.CheckResult.FAULTY
        logging.info('created')
        checkerlib.store_state(str(tick), creds)
        checkerlib.set_flagid(str(tick))
        return checkerlib.CheckResult.OK

    def check_service(self):
        # check if ports are open
        if not self._check_port_web(self.ip, PORT_WEB):
            return checkerlib.CheckResult.DOWN
        if not self._check_port(self.ip, PORT_SSH):
            return checkerlib.CheckResult.DOWN
        if not self._check_port(self.ip, PORT_FTP):
            return checkerlib.CheckResult.DOWN
        if not self._check_port(self.ip, PORT_DB):
            return checkerlib.CheckResult.DOWN
        
        # check if server is Apache 2.4.50
        if not self._check_apache_version():
            return checkerlib.CheckResult.FAULTY
        
        # check if shaktale user exists in pasapasa_ssh docker
        if not self._check_ssh_user('shaktale'):
            return checkerlib.CheckResult.FAULTY
        # check if shaktale user exists in pasapasa_ssh docker
        if not self._check_ftp_user('VgMY'):
            return checkerlib.CheckResult.FAULTY
        
        files = {'e4212090f6fff4da501a6e5d0fc7c44d': ('pasapasa_web_1','/var/www/html/index.html'), 
               '91a423017296dcf4c895d6e33dce73ae': ('pasapasa_web_1','/var/www/html/login.php'),
               '495ffdd47599886b854b7aa67dc2d210': ('pasapasa_ftp_1','/home/vsftpd/ftpuser/usernames.txt'),
               '93c120b4d757bec458a4bf0487d32390': ('pasapasa_ftp_1','/home/vsftpd/ftpuser/passlist.txt'),
               'ba55c65e08e320f1225c76f810f1328b': ('pasapasa_ssh_1','/etc/ssh/sshd_config')
               }
        # check if files has been changed by comparing its hash with the hash of the original file
        if not self._check_files_integrity(files):
            return checkerlib.CheckResult.FAULTY 
        
        
        return checkerlib.CheckResult.OK
    
    def check_flag(self, tick):
        if not self.check_service():
            return checkerlib.CheckResult.DOWN
        flag = checkerlib.get_flag(tick)
        #creds = checkerlib.load_state("flag_" + str(tick))
        # if not creds:
        #     logging.error(f"Cannot find creds for tick {tick}")
        #     return checkerlib.CheckResult.FLAG_NOT_FOUND
        flag_present = self._check_flag_present(flag)
        if not flag_present:
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        return checkerlib.CheckResult.OK
        
    #Function to check if an user exists in SSH docker
    @ssh_connect()
    def _check_ssh_user(self, username):
        ssh_session = self.client
        #command = f"docker exec pasapasa_ssh_1 sh -c 'id {username}'"
        command = f"docker exec pasapasa_ssh_1 sh -c 'grep {username} /etc/passwd'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        #if stderr.channel.recv_exit_status() != 0:
        if not stdout:
            return False
        return True
    
    #Function to check if an user exists in FTP docker
    @ssh_connect()
    def _check_ftp_user(self, username):
        ssh_session = self.client
        command = f"docker exec pasapasa_ftp_1 sh -c 'grep {username} /etc/vsftpd/virtual_users.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        #if stderr.channel.recv_exit_status() != 0:
        if not stdout:
            return False
        return True
    
    @ssh_connect()
    def _check_files_integrity(self, files):
        ssh_session = self.client
        for key, data in files.items():
            command = f"docker exec {data[0]} sh -c 'cat {data[1]}'"
            stdin, stdout, stderr = ssh_session.exec_command(command, timeout=0.9)
            if stderr.channel.recv_exit_status() != 0:
                return False
            output = stdout.read().decode().strip()
            if not hashlib.md5(output.encode()).hexdigest() == key:
                return False
        return True
    
    # Private Funcs - Return False if error
    def _add_new_flag(self, ssh_session, flag):
        ##### SSH CONTAINER ######
        # Execute the file creation command in the ssh container
        command = f"docker exec pasapasa_ssh_1 sh -c 'echo {flag} >> /tmp/flag.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)

        # Check if the command executed successfully
        if stderr.channel.recv_exit_status() != 0:
            return False
        
        ##### FTP CONTAINER ######
        # Execute the file creation command in the ftp container
        command = f"docker exec pasapasa_ftp_1 sh -c 'echo {flag} >> /home/vsftpd/ftpuser/flags.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)

        # Check if the command executed successfully
        if stderr.channel.recv_exit_status() != 0:
            return False
        
        ##### MARIADB CONTAINER #####
        sql = f"INSERT INTO flags (flag) VALUES ('{flag}');"
        # Comando para ejecutar el comando SQL dentro del contenedor MariaDB
        command = f"docker exec pasapasa_mariadb_1 sh -c \"mariadb -uroot -pht3ZklyypNce db -e \\\"{sql}\\\"\""
        stdin, stdout, stderr = ssh_session.exec_command(command)

        # Check if the command executed successfully
        if stderr.channel.recv_exit_status() != 0:
            return False
        # Return the result
        return {'flag': flag}

    @ssh_connect()
    def _check_flag_present(self, flag):
        ssh_session = self.client
        ## SSH Docker-en badago begiratu
        command = f"docker exec pasapasa_ssh_1 sh -c 'grep {flag} /tmp/flag.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        outputssh = stdout.read().decode().strip()
        ## FTP Docker-en badago begiratu
        command = f"docker exec pasapasa_ftp_1 sh -c 'grep {flag} /home/vsftpd/ftpuser/flags.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        outputftp = stdout.read().decode().strip()
        ## mariadb Docker-en badago begiratu
        sql = f"SELECT flag FROM flags WHERE flag = '{flag}';"
        print(sql)
        # Comando para ejecutar el comando SQL dentro del contenedor MariaDB
        command = f"docker exec pasapasa_mariadb_1 sh -c \"mariadb -uroot -pht3ZklyypNce db -e \\\"{sql}\\\"\""
        stdin, stdout, stderr = ssh_session.exec_command(command, timeout=0.9)
        if stderr.channel.recv_exit_status() != 0:
            return False
        outputdb = stdout.read().decode().strip()
        outputdb = outputdb[5:]
         
        return (flag == outputssh and outputssh == outputftp and outputssh == outputdb)

    def _check_port_web(self, ip, port):
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5)
            conn.request("GET", "/")
            response = conn.getresponse()
            return response.status == 200
        except (http.client.HTTPException, socket.error) as e:
            print(f"Exception: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def _check_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((ip, port))
            return result == 0
        except socket.error as e:
            print(f"Exception: {e}")
            return False
        finally:
            sock.close()

    @ssh_connect()
    def _check_apache_version(self):
        ssh_session = self.client
        command = f"docker exec pasapasa_web_1 sh -c 'httpd -v | grep \"Apache/2.4.50\'"
        stdin, stdout, stderr = ssh_session.exec_command(command)

        if stdout:
            return True
        else:
            return False
  
if __name__ == '__main__':
    checkerlib.run_check(MyChecker)




