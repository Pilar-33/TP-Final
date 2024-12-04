def calcular_puntos_restantes(puntos_jugador: int, modo_juego: int) -> int:
    """Calcula los puntos restantes para ganar según el modo de juego.
    
    Args:
        puntos_jugador: Puntos actuales del jugador.
        modo_juego: Modo de juego (15 o 30 puntos).
    
    Returns:
        Puntos restantes para ganar (0 si ya alcanzó el objetivo o si el modo es inválido).
    """
    modos_validos = [15, 30]
    
    if modo_juego not in modos_validos:
        return 0  
    
    puntos_restantes = modo_juego - puntos_jugador
    
    if puntos_restantes <= 0:
        return 0
    return puntos_restantes 

def menu() -> str:
    opcion = input("""
        TRUCO ARGENTINO
    =====================
    1. Jugar partida
    2. Ranking personal
    3. Estadisticas de jugadores
    4. Salir 
    Seleccione una opcion: """)
    return opcion