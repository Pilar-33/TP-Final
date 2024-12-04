from jugar.cartas import*
from jugar.envido import*
import random

OPCIONES_CANTO = ["envido", "real_envido", "falta_envido", "nada"]
NOMBRES_MAQUINA = [
    "Bot Cantor",
    "Señor Truco",
    "Rey del envido", 
    "Bot Chanta",
    "El Chamuyador",
    "Bot Me la Juego",
    "Máquina de Mentir"
]

def crear_jugador_estrategico(nombre: str = None) -> dict:
    """Crea un jugador estratégico con un nombre aleatorio si no se proporciona uno"""
    if nombre is None:
        nombre = random.choice(NOMBRES_MAQUINA)
        
    jugador_estrategico = {
        "nombre": nombre,
        "puntos": 0,
        "cartas": [],
        "cantos": [],
        "tipo": "Jugador Estratégico"
    }
    return jugador_estrategico

def jugar_carta_estrategica(cartas: list, es_mano: bool, carta_rival: dict = None) -> dict:
    """Determina qué carta jugar según la estrategia"""
    if es_mano:
        # Juega la carta más alta cuando es mano
        return max(cartas, key=lambda x: x["jerarquia"])
    else:
        if carta_rival:
            # Busca cartas que puedan ganar
            cartas_ganadoras = [c for c in cartas if c["jerarquia"] > carta_rival["jerarquia"]]
            if cartas_ganadoras:
                # Si tiene cartas ganadoras, usa la menor de ellas
                return min(cartas_ganadoras, key=lambda x: x["jerarquia"])
            # Si no puede ganar, juega la más baja
            return min(cartas, key=lambda x: x["jerarquia"])

def responder_canto_estrategico(cartas: list, canto: str, puntos_propios: int, puntos_rival: int, modo_juego: int) -> str:
    """Decide la respuesta a los diferentes cantos según la estrategia"""
    puntos_envido = calcular_envido(cartas)
    puntos_faltantes = calcular_puntos_restantes(puntos_propios, modo_juego)
    
    match canto:
        case "envido":
            if puntos_envido > 27:
                if puntos_envido >= 30 and puntos_faltantes <= 2:
                    return "envido"
                return "quiero"
            return "no_quiero"
            
        case "real_envido":
            if puntos_envido > 32 or puntos_faltantes <= 3:
                return "quiero"
            return "no_quiero"
            
        case "falta_envido":
            if puntos_envido > 33 or (modo_juego - puntos_rival) <= 5:
                return "quiero"
            return "no_quiero"
            
        case "envido_envido":
            if puntos_envido > 29:
                if puntos_envido >= 32 and puntos_faltantes <= 3:
                    return "real_envido"
                return "quiero"
            return "no_quiero"

def cantar_envido_estrategico(cartas: list, puntos_propios: int, puntos_rival: int, modo_juego: int) -> str:
    """Decide si inicia un canto de envido según la estrategia y estado del juego"""
    puntos_envido = calcular_envido(cartas)
    puntos_faltantes = calcular_puntos_restantes(puntos_propios, modo_juego)
    
    if puntos_envido > 27:
        falta_envido = modo_juego - puntos_rival
        if puntos_envido >= 33 or falta_envido <= 5:
            return "falta_envido"
        elif puntos_envido >= 31 and puntos_faltantes <= 3:
            return "real_envido"
        elif puntos_envido >= 28:
            return "envido"
    return "nada"