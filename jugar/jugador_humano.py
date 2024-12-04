from jugar.cartas import*
from jugar.envido import*

OPCIONES_CANTO = ["envido", "real envido", "falta envido", "nada"]
def crear_jugador_humano(nombre: str) -> dict:
    """Crea un jugador humano con un nombre y puntos iniciales"""
    jugador_humano = {
        "nombre": nombre,
        "puntos": 0,
        "cartas": [],
        "cantos": []
    }
    return jugador_humano

def mostrar_cartas(cartas: list) -> None:
    """Muestra las cartas del jugador"""
    print("\nTus cartas son:")
    for i, carta in enumerate(cartas):
        print(f"{i + 1}. {carta['valor']} de {carta['palo']}")

def seleccionar_carta(cartas: list) -> dict:
    """Permite al jugador seleccionar una carta para jugar"""
    mostrar_cartas(cartas)
    seleccion_valida = False  
    
    while seleccion_valida == False:
        seleccion = input("\nSeleccione el número de la carta a jugar (1-3): ")
        
        if seleccion.isdigit():
            seleccion = int(seleccion)
            
            if 1 <= seleccion <= len(cartas):
                seleccion_valida = True
                carta_jugada = cartas.pop(seleccion - 1)
                return carta_jugada
        # Si no es válido, mostrar mensaje de error
        print("Selección inválida. Intente nuevamente.")

def mostrar_opciones(opciones: list) -> None:
    """Muestra las opciones disponibles al jugador."""
    print("\nOpciones disponibles:")
    for i, opcion in enumerate(opciones, start=1):
        print(f"{i}. {opcion.capitalize()}")

#Valida y procesa la selección numérica que hace el jugador 
#entre las opciones mostradas.        
def obtener_opcion(opciones: list) -> int:
    """
    Solicita al jugador seleccionar una opción válida.
    Retorna el índice de la opción seleccionada.
    """
    continuar = True
    while continuar == True:
        seleccion = input("\nSeleccione su decisión (1-4): ")
        if seleccion.isdigit():
            seleccion = int(seleccion)
            if seleccion > 0 and seleccion <= len(opciones):
                return seleccion
        print("Opción inválida. Intente nuevamente.")

def decidir_canto(opciones: list = OPCIONES_CANTO) -> str:
    """Permite al jugador decidir si quiere cantar envido."""
    
    mostrar_opciones(opciones)
    seleccion = obtener_opcion(opciones)
    
    opcion_seleccionada = opciones[seleccion - 1].replace(" ", "_")
    return opcion_seleccionada