import subprocess
## mariadb Docker-en badago begiratu
sql = f"SELECT flag FROM flags ORDER BY id DESC LIMIT 1;"
# Comando para ejecutar el comando SQL dentro del contenedor MariaDB
command = f"docker exec pasapasa_mariadb_1 sh -c \"mariadb -uroot -pht3ZklyypNce db -e \\\"{sql}\\\"\""
print(command)
result = subprocess.run(command, shell=True, capture_output=True, text=True)
output = result.stdout
print(output[5:])
#outputdb = output.read().decode().strip()