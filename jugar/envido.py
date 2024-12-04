from jugar.cartas import*
from jugar.auxiliares import*

def determinar_puntos_envido(canto: str, respuesta: str, puntos_jugador: int, puntos_oponente: int) -> tuple:
    """Determina los puntos a asignar según el canto y la respuesta"""
    puntos = {
        "envido": 2,
        "real envido": 3,
        "falta envido": 4
    }
    
    if respuesta == "no_quiero":
        return 1, 0
    elif respuesta == "quiero":
        puntos_ronda = puntos[canto]
        if puntos_jugador > puntos_oponente:
            return puntos_ronda, 0
        else:
            return 0, puntos_ronda


def calcular_envido(cartas: list) -> int:
    """
    Calcula el puntaje de envido para una mano.
    Retorna el puntaje máximo considerando cartas del mismo palo.
    """
    grupos_por_palo = {}
    
    # Agrupar las cartas por palo
    for carta in cartas:
        palo = carta["palo"]
        valor = carta["valor"]
        
        if valor <= 7:  
            if palo not in grupos_por_palo:
                grupos_por_palo[palo] = []
            grupos_por_palo[palo].append(valor)
        
    # Calcular el puntaje máximo de los grupos de cartas
    puntos_maximos = 0
    for valores in grupos_por_palo.values():
        if len(valores) > 1:  
            valores_ordenados = sorted(valores, reverse=True)  
            dos_mayores = valores_ordenados[:2]  
            suma = sum(dos_mayores)
            puntos = suma + 20
            if puntos > puntos_maximos:
                puntos_maximos = puntos
                
    return puntos_maximos

def calcular_puntaje_real_envido(cartas: list) -> int:
    """Calcula el puntaje del real envido."""
    real_envido = calcular_envido(cartas) + 3
    return  real_envido

def calcular_puntaje_falta_envido(puntos_jugador: int, modo_juego: int) -> int:
    """Calcula el puntaje de una falta envido usando los puntos restantes.
    
    Args:
        puntos_jugador: Puntos actuales del jugador
        modo_juego: Modo de juego (15 o 30 puntos)
    
    Returns:
        Puntaje del falta envido
    """
    falta_envido = calcular_puntos_restantes(puntos_jugador, modo_juego)
    return falta_envido