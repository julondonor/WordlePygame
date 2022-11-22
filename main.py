import pandas as pd
import re 
import colorama # Para colorear el texto en consola
from colorama import Fore, Back, Style


class Letra():
    """
    Esta clase permite manejar el color de las letras,
    y tiene un metodo que permite imprimir con ese color.
    """
    def __init__(self, letra= "-"):
        self.letra = letra 
        self.color = Fore.BLACK 

    def imprimir(self):
        print(self.color+Style.BRIGHT+self.letra+Style.RESET_ALL, end="")
        



def dibujar(attempts, letras): #O(num) -> ¿O(1)?
    """
    Dibuja el tablero considerando las palabras previamente ingresadas.
    Y también los colores de las letras en el teclado inferior.
    """

    renglones = len(attempts)
    columnas = len(attempts[0])
    tope = "\t" + " ___"*columnas
    vacio = "\t" + "|   "*columnas
    fin = "\t" + "|___"*columnas
    print(Fore.BLACK+ tope)

    # Attempts es una lista de listas. Donde cada sublista tiene un objeto de
    # tipo Letra(), attempts = [ [Lista(), Lista(), ...]]

    for attempt in attempts: # O(6*num) = O(num), pero 4<=num<=8
        print(Fore.BLACK + vacio+"|")
        new = "\t" + "| "
        print(Fore.BLACK + new, end="")
        for letra in attempt: # hay "num" letras en cada attempt
            letra.imprimir()
            print(Fore.BLACK+" | ", end="")
        print()
        print(Fore.BLACK+fin+"|")


    print()
    print(end="\t"+" "*0)
    for letra in letras[0]: #O(1), por ser constante la cantidad de letras en letras[0]
        letra.imprimir()
        print(end=" ")
    print()
    print(end="\t"+" "*1)
    for letra in letras[1]: #O(1)
        letra.imprimir()
        print(end=" ")
    print(end="\t   ")
    print()

    print(end="\t"+" "*3)
    for letra in letras[2]: #O(1)
        letra.imprimir()
        print(end=" ")
    print()

def valid(word, num):
    """Función para revisar si la palabra ingresada por el usuario es válida:
    1. Se revisa la longitud.
    2. Se revisa que solo tenga letras, nada de números ni signos especiales.
    """
    if len(word)!= num:
        return f"La palabra debe tener {num} caracteres."
    ans = re.search("[^a-zA-Z]", word)
    if ans:
        return "La palabra no debe contener numeros o caracteres especiales"
    else:
        return True


# Se carga el lemario en inglés
df = pd.read_excel("Lemario_ingles.xlsx")
ganadas = 0
perdidas = 0

# Comienza el ciclo del juego, hasta que la persona desee salir de la partida
while True:

    # Mensaje de bienvenida
    print(Fore.BLACK+"Bienvenido a una nueva partida.\n")
    print("Por favor indique el tamaño de la palabra a adivinar")
    print("Recuerde que debe ser un número entre 4 y 8")
    num = int(input("Longitud palabra: "))
    print(f"Usted ha escogido una palabra de tamaño {num}")

    # Se selecciona aleatoriamente una palabra
    word_serie = df[df["length"]==num].sample(n=1)
    word = word_serie["word"].iloc[0].upper()
    defi = word_serie["description"].iloc[0]

    # Aparte de la palabra, se crea un conjunto con las letras
    set_word = set(word) #O(num)


    freq_letters = {}
    for letra in word: #O(num)
        if letra not in freq_letters.keys():
            freq_letters[letra] = 1
        else:
            freq_letters[letra] +=1

    ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    letras = [ #O(26) = O(1)
        [Letra(letra) for letra in linea]
        for linea in ALPHABET
    ]
    #letras = [
    # [Letra(Q), Letra(W), ...],
    # [Letra(A), Letra(S),...],
    # [Letra(Z),...]
    # ]
  
    # Diccionario que permite acceder a la posicion de las letras del teclado inferior
    # en O(1), para evitar tener que iterar por fuerza bruta sobre `letras`
    dic_letras = {letras[i][j].letra:(i,j) for i in range(len(letras)) for j in range(len(letras[i])) }
    #dic_letras = {
    #  "A":(1,0), "U":(0,6), "L":(1,8), ...
    # }

    # Se crean las 6 palabras que adivinara el usuario.
    # Inicialmente todos los caracteres son "-"
    attempts = [ 
        [Letra() for i in range(num)]
        for j in range(6)
    ]
    intentos = ["Primer", "Segundo","Tercer","Cuarto","Quinto", "Sexto"]
    gano  =False

    for intento in range(len(intentos)):
        dic_temp = freq_letters.copy() #O(num) 
        print(f"{intentos[intento]} intento. Te quedan {6-intento} oportunidades...")
        dibujar(attempts, letras) #O(num)

        # Ciclo para solicitarle una palabra valida al usuario
        while True:
            curr = input(f"Por favor digita una palabra de {num} caracteres: ")
            ver = valid(curr, num)
            if ver==True:
                break
            else:
                print(Fore.RED+"ATENCION: ", end="")
                print(Fore.BLACK, end="")
                print(ver)


        curr = curr.upper()

        # Permite colorear correctamente letras repetidas:
        for i in range(num): #O(num)
            if word[i] == curr[i]:
                dic_temp[word[i]]-=1


        # Coloreando tanto las letras de los intentos
        # como del teclado:
        for i in range(num):
            attempts[intento][i].letra = curr[i]
            posi, posj = dic_letras[curr[i]]
            if word[i] == curr[i]:
                attempts[intento][i].color=Fore.GREEN
                letras[posi][posj].color = Fore.GREEN

            elif (curr[i] in set_word):
                if (dic_temp[curr[i]]>0):
                    attempts[intento][i].color=Fore.YELLOW
                    if letras[posi][posj].color == Fore.BLACK:
                        letras[posi][posj].color = Fore.YELLOW
                else:
                    attempts[intento][i].color=Fore.RED
                    if letras[posi][posj].color == Fore.BLACK:
                        letras[posi][posj].color = Fore.RED                    
            else:
                attempts[intento][i].color=Fore.RED
                letras[posi][posj].color = Fore.RED
        if curr==word:
            gano = True
            break
    dibujar(attempts, letras)
    if gano:
        ganadas += 1
        print(f"¡FELICITACIONES CAMPEON! Has adivinado la palabra en {intento+1} intentos.")
    else:
        perdidas +=1
        print(f"Hey, qué pasa vale mía. Has perdido.")
        print(f"La palabra correcta era {word}")
        print("Su definicion es: ")
        print(defi)
    print(f"Has jugado {ganadas+perdidas} partidas...")
    print(Fore.GREEN+f"\t-Has GANADO {ganadas} partidas hasta ahora.")
    print(Fore.RED+f"\t-Has PERDIDO {perdidas} partidas hasta ahora.")
    Fore.BLACK
    print("\n\n")
    comando = True
    while True:
        con = input("¿Deseas seguir jugando? [S/N]")
        if con.upper() == "N":
            comando = False
            break
        elif con.upper() == "S":
            break
        else:
            print("Ingresa una opción válida")
    if comando:
        continue
    else:
        break
    
