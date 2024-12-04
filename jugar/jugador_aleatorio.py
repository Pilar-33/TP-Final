import random
from jugar.cartas import*
from jugar.envido import*

OPCIONES_CANTO = ["envido", "real_envido", "falta_envido", "nada"]
NOMBRES_MAQUINA = [
    
    "Bot Matador", 
    "Truquera",
    "El Envido Bot",
    "Bot Mentiroso",
    "La Máquina Maestra",
    "Bot Fullero",
    "El As Digital"
]
nombre = random.choice(NOMBRES_MAQUINA)

def crear_jugador_aleatorio(nombre: str) -> dict:
    """Crea  un jugador aleatorio con un nombre y puntos iniciales"""
    jugador_aleatorio = {
        "nombre": nombre,
        "puntos": 0,
        "cartas": [],
        "cantos": [],
        "tipo": "Jugador Aleatorio"
    }
    return jugador_aleatorio

def decidir_canto_envido(cartas: list, opciones: list = OPCIONES_CANTO) -> str:
    """Decide aleatoriamente si cantar envido/real envido/falta envido"""
    puntos_envido = calcular_envido(cartas)
    
    probabilidades = []
    
    if puntos_envido >= 25:
        probabilidades = [0.3, 0.4, 0.2, 0.1] 
    elif puntos_envido >= 20:
        probabilidades = [0.5, 0.3, 0.1, 0.1]
    else:
        probabilidades = [0.3, 0.1, 0.0, 0.6]
    decision = random.choices(opciones, probabilidades)[0]
    return decision

def jugar_carta_aleatoria(cartas_disponibles: list) -> dict:
    """Juega una carta aleatoria de las disponibles"""
    carta_jugada = None  
    if cartas_disponibles:  
        carta_jugada = random.choice(cartas_disponibles)  
        cartas_disponibles.remove(carta_jugada)  
    return carta_jugada