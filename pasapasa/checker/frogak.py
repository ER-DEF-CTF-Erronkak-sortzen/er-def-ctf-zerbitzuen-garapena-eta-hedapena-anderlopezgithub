import subprocess
import hashlib

files = {'e4212090f6fff4da501a6e5d0fc7c44d': ('pasapasa_web_1','/var/www/html/index.html'), 
               'a7fe4d50a63d18df541cacb5ae43d0b8': ('pasapasa_web_1','/var/www/html/login.php'), 
               'bf0cf5154762078a36827e9e4b81326e': ('pasapasa_ftp_1','/home/vsftpd/ftpuser/usernames.txt'), 
               #'1e1ce45b5bb352fb922e6a06851b8d64': ('pasapasa_ftp_1','/home/vsftpd/ftpuser/passlist.txt'), 
               '2f51d5e415c8c7eaa8dcb3f995d4eff0': ('pasapasa_ftp_1','/home/vsftpd/ftpuser/passlist.txt'), 
               '6f264d7fac3dec49ed7f5f3bfbbff6b5': ('pasapasa_ssh_1','/etc/ssh/sshd_config')
               }
integrity = True

for key, data in files.items():
    print(key,data)
    

    # Comando que deseas ejecutar
    command = f"docker exec {data[0]} sh -c 'cat {data[1]}'"
    print(command)
    # Ejecutar el comando
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Imprimir la salida del comando
    #print("stdout:", result.stdout)
    #print("stderr:", result.stderr)
    #print("Return code:", result.returncode)

    #if result.stderr.channel.recv_exit_status() != 0:
    #    print(False)
    output = result.stdout
    
    hash = hashlib.md5(output.encode()).hexdigest()
    print(hash)
    integrity = integrity and hash == key
    print(integrity)

print(integrity)