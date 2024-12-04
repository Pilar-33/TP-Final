import pygame
from truco.historial import*

def mostrar_ranking_pygame(pantalla, fondo):
    # Colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    DORADO = (218, 165, 32)
    DORADO_HOVER = (238, 185, 52)
    
    # Inicializar fuentes
    pygame.font.init()
    
    # Configurar fuentes con tamaños reducidos
    fuente_titulo = pygame.font.SysFont('segoe ui emoji', 25)  # Reducido de 45
    fuente_texto = pygame.font.SysFont('segoe ui emoji', 20)   # Reducido de 36
    fuente_boton = pygame.font.SysFont('segoe ui emoji', 20)   # Nueva fuente para botón
    
    # Dibujar fondo
    pantalla.blit(fondo, (0, 0))
    
    # Superficie semi-transparente más pequeña
    superficie = pygame.Surface((450, 350))  # Reducida de (500, 400)
    superficie.set_alpha(200)
    superficie.fill(NEGRO)
    superficie_rect = superficie.get_rect(center=(pantalla.get_width()//2, pantalla.get_height()//2))
    pantalla.blit(superficie, superficie_rect)
    
    # Título con emojis
    titulo = fuente_titulo.render("🏆 RANKING DE JUGADORES 🏆", True, DORADO)
    titulo_rect = titulo.get_rect(center=(pantalla.get_width()//2, superficie_rect.top + 30))
    pantalla.blit(titulo, titulo_rect)
    
    # Mostrar ranking con espaciado reducido
    ranking = obtener_ranking()
    if not ranking:
        texto = fuente_texto.render("No hay ranking disponible", True, BLANCO)
        texto_rect = texto.get_rect(center=(pantalla.get_width()//2, pantalla.get_height()//2))
        pantalla.blit(texto, texto_rect)
    else:
        y_pos = superficie_rect.top + 70  # Ajustado el punto de inicio
        for pos, jugador in enumerate(ranking, 1):
            icono = "⭐" if jugador['victorias'] > jugador['partidas']/2 else "❌"
            texto = f"{pos}. {jugador['nombre']} - {icono} {jugador['victorias']} victorias"
            linea = fuente_texto.render(texto, True, BLANCO)
            linea_rect = linea.get_rect(center=(pantalla.get_width()//2, y_pos))
            pantalla.blit(linea, linea_rect)
            y_pos += 35  # Reducido el espaciado entre líneas
    
    # Botón Volver ajustado
    boton_volver = pygame.Rect(
        pantalla.get_width()//2 - 50,  # Más estrecho
        superficie_rect.bottom - 60,    # Ajustada la posición
        100,                           # Ancho reducido
        30                             # Alto reducido
    )
    
    color_boton = DORADO
    if boton_volver.collidepoint(pygame.mouse.get_pos()):
        color_boton = DORADO_HOVER
        pygame.draw.rect(pantalla, NEGRO, boton_volver.inflate(4, 4), border_radius=8)
    
    pygame.draw.rect(pantalla, color_boton, boton_volver, border_radius=8)
    
    texto_volver = fuente_boton.render("Volver", True, NEGRO)
    texto_rect = texto_volver.get_rect(center=boton_volver.center)
    
    if pygame.mouse.get_pressed()[0] and boton_volver.collidepoint(pygame.mouse.get_pos()):
        texto_rect.y += 2
        
    pantalla.blit(texto_volver, texto_rect)
    
    return boton_volver

def manejar_eventos_ranking(evento, boton_volver):
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if boton_volver.collidepoint(evento.pos):
            return True
    return False

