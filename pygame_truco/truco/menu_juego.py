import pygame

def init_botones():
    botones = {
        'jugar': {'texto': 'Jugar Partida', 'rect': pygame.Rect(250, 250, 300, 50)},
        'ranking': {'texto': 'Ranking de Jugadores', 'rect': pygame.Rect(250, 320, 300, 50)}, 
        'salir': {'texto': 'Salir', 'rect': pygame.Rect(250, 390, 300, 50)}
    }
    return botones


def dibujar_menu(ventana, botones):
    # Colores
    COLOR_BOTON = (50, 50, 50)
    COLOR_HOVER = (100, 100, 100)
    COLOR_TEXTO = (255, 255, 255)
    
    # Título
    fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
    titulo = fuente_titulo.render("TRUCO ARGENTINO", True, COLOR_TEXTO)
    ventana.blit(titulo, (250, 150))
    
    # Botones
    fuente_botones = pygame.font.SysFont("Arial", 24)
    mouse_pos = pygame.mouse.get_pos()
    
    for boton in botones.values():
        color = COLOR_HOVER if boton['rect'].collidepoint(mouse_pos) else COLOR_BOTON
        pygame.draw.rect(ventana, color, boton['rect'], border_radius=10)
        texto = fuente_botones.render(boton['texto'], True, COLOR_TEXTO)
        texto_rect = texto.get_rect(center=boton['rect'].center)
        ventana.blit(texto, texto_rect)

def manejar_eventos_menu(botones):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for accion, boton in botones.items():
                if boton['rect'].collidepoint(mouse_pos):
                    return accion
    return None
