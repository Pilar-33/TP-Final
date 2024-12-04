from os import system
system("cls")

from jugar.auxiliares import*
from jugar.partida import*
from jugar.historial import*

juego = True
while juego == True:
    opcion = menu()
    match opcion:
        case "1":
            iniciar_partida()
        case "2":
            nombre = input("Ingrese el nombre del jugador: ")
            mostrar_historial_personal(nombre)
        case "3":
            mostrar_estadisticas_detalladas()
        case "4":
            print("Gracias por jugar!!!.")
            juego = False