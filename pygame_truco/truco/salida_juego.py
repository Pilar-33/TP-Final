import pygame
from truco.jugar_inicio import*
from truco.barra_titulo import*
from truco.efecto_lluvia import*

# Definición de constantes
COLOR_BARRA = (50, 50, 50)
COLOR_BOTON_CERRAR = (200, 0, 0)
COLOR_BOTON_CERRAR_HOVER = (255, 0, 0)
COLOR_TEXTO = (255, 255, 255)

# Definición de constantes para el botón
boton_x = 350  # Posición X del botón
boton_y = 400  # Posición Y del botón
boton_ancho = 100  # Ancho del botón
boton_alto = 40   # Alto del botón

# Cargar recursos
ICONO_ORIGINAL = pygame.image.load("assets/cartas/1_basto.jpg")
ICONO_GRANDE = pygame.transform.scale(ICONO_ORIGINAL, (40, 40))

def mostrar_mensaje_despedida(ventana):
    cartas = crear_lluvia_cartas()
    esperando = True
    
    while esperando:
        ventana.blit(imagen_fondo, (0,0))
        dibujar_barra_titulo(
            ventana,
            ANCHO,
            COLOR_BARRA,
            ICONO_GRANDE,
            COLOR_BOTON_CERRAR,
            COLOR_BOTON_CERRAR_HOVER,
            COLOR_TEXTO
        )
        
        # Actualizar y dibujar lluvia de cartas
        actualizar_lluvia(cartas, ventana)
        
        # Oscurecer área debajo de la barra de título
        s = pygame.Surface((800,560))
        s.set_alpha(128)
        s.fill((0,0,0))
        ventana.blit(s, (0,40))
        
        # Borde Negro
        fuente_grande = pygame.font.SysFont("Arial", 72)
        mensaje = fuente_grande.render("¡Gracias por jugar!", True, (0, 0, 0))
        rect = mensaje.get_rect(center=(402, 252))
        ventana.blit(mensaje, rect)
        
        # Texto principal
        mensaje = fuente_grande.render("¡Gracias por jugar!", True, (255, 215, 0))
        rect = mensaje.get_rect(center=(400, 250))
        ventana.blit(mensaje, rect)
        
        # Mensaje secundario
        fuente_pequeña = pygame.font.SysFont("Arial", 28)
        mensaje_continuar = fuente_pequeña.render("¡Hasta la próxima!", True, (255, 255, 255))
        rect_continuar = mensaje_continuar.get_rect(center=(400, 350))
        ventana.blit(mensaje_continuar, rect_continuar)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0] >= boton_x and mouse_pos[0] <= boton_x + boton_ancho) and \
                (mouse_pos[1] >= boton_y and mouse_pos[1] <= boton_y + boton_alto):
                    esperando = False
            if evento.type == pygame.QUIT:
                esperando = False
