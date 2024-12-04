import random
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

def crear_jugador_humano(nombre: str) -> dict:
    """Crea un jugador humano con un nombre y puntos iniciales"""
    jugador_humano = {
        "nombre": nombre,
        "puntos": 0,
        "cartas": [],
        "cantos": []
    }
    return jugador_humano
