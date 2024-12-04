import pygame
import random
from truco.jugar_inicio import*
from truco.constantes import*

def inicializar_ronda():
    """Inicializa el estado de la ronda"""
    return {
        "turno_actual": "jugador",
        "estado_envido": None,
        "ultimo_canto": None,
        "puntos_en_juego": 0
    }

def calcular_puntos_envido(cartas: list) -> int:
    """Calcula los puntos de envido de una mano"""
    palos = {}
    for carta in cartas:
        if carta['palo'] not in palos:
            palos[carta['palo']] = []
        palos[carta['palo']].append(carta['numero'])
    
    max_puntos = 0
    for numeros in palos.values():
        if len(numeros) >= 2:
            numeros = [n if n < 10 else 0 for n in numeros]
            for i in range(len(numeros)):
                for j in range(i + 1, len(numeros)):
                    puntos = 20 + numeros[i] + numeros[j]
                    max_puntos = max(max_puntos, puntos)
    
    return max_puntos

def procesar_canto_envido(
    canto: str, jugador: dict, 
    maquina: dict, estado_ronda: dict, modo_juego
    ) -> dict:
    """Procesa los cantos de envido y determina el resultado"""
    puntos_jugador = calcular_puntos_envido(jugador['cartas'])
    puntos_maquina = calcular_puntos_envido(maquina['cartas'])
    
    puntos = {
        "envido": 2,
        "real_envido": 3,
        "falta_envido": modo_juego - max(jugador['puntos'], maquina['puntos'])
    }
    
    estado_ronda["puntos_en_juego"] = puntos[canto]
    estado_ronda["ultimo_canto"] = canto
    
    return {
        "puntos_jugador": puntos_jugador,
        "puntos_maquina": puntos_maquina,
        "puntos_en_juego": puntos[canto]
    }

def decidir_respuesta_maquina(puntos_maquina: int, canto: str) -> str:
    """Decide si la máquina acepta el canto basado en sus puntos y algo de aleatoriedad"""
    umbral = {
        "envido": 25,
        "real_envido": 28,
        "falta_envido": 30
    }
    # Agrega un factor de aleatoriedad a la decisión
    factor_aleatorio = random.randint(-2, 2)
    return "quiero" if puntos_maquina + factor_aleatorio >= umbral[canto] else "no_quiero"


def mostrar_opciones_canto(ventana):
    """Muestra las opciones de canto disponibles"""
    opciones = ["Envido", "Real Envido", "Falta Envido"]
    botones = []
    y_pos = ALTO - 150
    
    # Definir posiciones de los botones
    rect_envido = pygame.Rect(50, y_pos, 180, 40)
    rect_real = pygame.Rect(ANCHO - 400, y_pos, 180, 40)
    rect_falta = pygame.Rect(ANCHO - 200, y_pos, 180, 40)
    
    # Lista de rectángulos para los botones
    rects = [rect_envido, rect_real, rect_falta]
    
    for i, opcion in enumerate(opciones):
        botones.append({"rect": rects[i], "texto": opcion})
        pygame.draw.rect(ventana, (200, 0, 0), rects[i])  # Color rojo
        texto = pygame.font.Font(None, 36).render(opcion, True, (255, 255, 255))
        # Centrar texto
        pos_x = rects[i].x + (rects[i].width - texto.get_width()) // 2
        pos_y = rects[i].y + (rects[i].height - texto.get_height()) // 2
        ventana.blit(texto, (pos_x, pos_y))
    
    return botones


def actualizar_puntos(jugador: dict, maquina: dict, resultado: dict):
    """Actualiza los puntos según el resultado del canto"""
    if resultado["ganador"] == "jugador":
        jugador["puntos"] += resultado["puntos"]
    else:
        maquina["puntos"] += resultado["puntos"]
    

