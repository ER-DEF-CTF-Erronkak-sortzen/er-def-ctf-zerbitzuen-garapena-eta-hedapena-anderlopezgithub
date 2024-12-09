import random
import string

def generar_usuario_y_contraseña():
    letras = string.ascii_letters
    numeros = string.digits
    caracteres = letras + numeros
    password = ''.join(random.choice(caracteres) for i in range(8))
    username = ''.join(random.choice(letras) for i in range(4))
    return username, password

# Generar y mostrar 50 usuarios y contraseñas
for _ in range(50):
    usuario, contraseña = generar_usuario_y_contraseña()
    print(f"('{usuario}', '{contraseña}'),")