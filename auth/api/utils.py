import random
from string import digits

def generar_cadena_aleatoria(longitud):
    cadena = ''
    for i in range(longitud):
        cadena += random.choice(digits)

    return cadena
