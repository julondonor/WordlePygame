import pandas as pd
import colorama
import re
from colorama import Fore, Back, Style


class Letra():
    def __init__(self, letra= "-"):
        self.letra = letra
        self.color = Fore.BLACK

    def imprimir(self):
        print(self.color+Style.BRIGHT+self.letra+Style.RESET_ALL, end="")
        



def dibujar(attempts, letras):
    renglones = len(attempts)
    columnas = len(attempts[0])
    tope = "\t" + " ___"*columnas
    vacio = "\t" + "|   "*columnas
    fin = "\t" + "|___"*columnas
    print(Fore.BLACK+ tope)

    for attempt in attempts:
        print(Fore.BLACK + vacio+"|")
        new = "\t" + "| "
        print(Fore.BLACK + new, end="")
        for letra in attempt:
            letra.imprimir()
            print(Fore.BLACK+" | ", end="")
        print()
        print(Fore.BLACK+fin+"|")

    print()
    print(end="\t"+" "*0)
    for letra in letras[0]:
        letra.imprimir()
        print(end=" ")
    print()
    print(end="\t"+" "*1)
    for letra in letras[1]:
        letra.imprimir()
        print(end=" ")
    print(end="\t   ")
    print()

    print(end="\t"+" "*3)
    for letra in letras[2]:
        letra.imprimir()
        print(end=" ")
    print()

def valid(word, num):
    if len(word)!= num:
        return f"La palabra debe tener {num} caracteres."
    ans = re.search("[^a-zA-Z]", word)
    if ans:
        return "La palabra no debe contener numeros o caracteres especiales"
    else:
        return True


df = pd.read_excel("Lemario_ingles.xlsx")
#print(Fore.GREEN+"Hola, ensayando")
ganadas = 0
perdidas = 0
while True:
    print(Fore.BLACK+"Bienvenido a una nueva partida.\n")
    print("Por favor indique el tamaño de la palabra a adivinar")
    print("Recuerde que debe ser un número entre 4 y 8")
    num = int(input("Longitud palabra: "))
    print(f"Usted ha escogido una palabra de tamaño {num}")


    word_serie = df[df["length"]==num].sample(n=1)

    word = word_serie["word"].iloc[0].upper()
    #print("La palabra a adivinar es", word)
    defi = word_serie["description"].iloc[0]
    set_word = set(word)
    freq_letters = {}
    for letra in word:
        if letra not in freq_letters.keys():
            freq_letters[letra] = 1
        else:
            freq_letters[letra] +=1

    ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    letras = [
        [Letra(letra) for letra in linea]
        for linea in ALPHABET
    ]
    dic_letras = {letras[i][j].letra:(i,j) for i in range(len(letras)) for j in range(len(letras[i])) }
    #print(dic_letras)
    attempts = [ 
        [Letra() for i in range(num)]
        for j in range(6)
    ]
    intentos = ["Primer", "Segundo","Tercer","Cuarto","Quinto", "Sexto"]
    gano  =False
    for intento in range(len(intentos)):
        dic_temp = freq_letters.copy()
        print(f"{intentos[intento]} intento. Te quedan {6-intento} oportunidades...")
        dibujar(attempts, letras)
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
        #print(dic_temp)
        for i in range(num):
            if word[i] == curr[i]:
                dic_temp[word[i]]-=1
        #print(dic_temp)
        for i in range(num):
            attempts[intento][i].letra = curr[i]
            posi, posj = dic_letras[curr[i]]
            if word[i] == curr[i]:
                attempts[intento][i].color=Fore.GREEN
                letras[posi][posj].color = Fore.GREEN
                #attempts[intento][i].bg = Fore.GREEN
            elif (curr[i] in set_word):
                if (dic_temp[curr[i]]>0):
                    #print("Lo que quiero saber es",dic_temp[word[i]]>0)
                    #print(dic_temp)
                    #print(word[i], dic_temp[word[i]])
                    attempts[intento][i].color=Fore.YELLOW
                    if letras[posi][posj].color == Fore.BLACK:
                        letras[posi][posj].color = Fore.YELLOW
                    #attempts[intento][i].bg = Back.YELLOW
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
    
