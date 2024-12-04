from os import system
system("cls")
import pygame
import sys
from truco.menu_juego import *
from truco.barra_titulo import*
from truco.salida_juego import *
from truco.efecto_lluvia import *
from truco.ranking_pygame import *
from truco.jugar_inicio import *

# Inicialización de Pygame
pygame.init()
pygame.font.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.NOFRAME)
pygame.display.set_caption("TRUCO")
imagen_fondo = pygame.image.load("./assets/fondos/mesa.jpg")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
icono_grande = pygame.image.load("./assets/cartas/1_basto.jpg")
icono_grande = pygame.transform.scale(icono_grande, (32, 35))

# Configuración de colores
color_barra = (50, 50, 50)
color_texto = (255, 255, 255)
color_boton_cerrar = (200, 50, 50)
color_boton_cerrar_hower = (255, 80, 80)

# Inicialización de elementos
botones = init_botones()
correr = True  

while correr:
    ventana.blit(imagen_fondo, (0, 0))

    # Dibujar barra de título
    dibujar_barra_titulo(
        ventana,
        ANCHO,
        color_barra,
        icono_grande,
        color_boton_cerrar,
        color_boton_cerrar_hower,
        color_texto,
    )
    
    # Dibujar menú
    dibujar_menu(ventana, botones)
    accion = manejar_eventos_menu(botones)
    
    if accion == "salir":
        mostrar_mensaje_despedida(ventana)
        correr = False
    elif accion == "jugar":
        jugar()
    elif accion == "ranking":
        mostrar_ranking = True
        while mostrar_ranking:
            fondo = pygame.image.load("./assets/fondos/mesa.jpg")
            fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
            boton_volver = mostrar_ranking_pygame(ventana, fondo)
            pygame.display.flip()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if manejar_eventos_ranking(evento, boton_volver):
                    accion = "menu"
                    mostrar_ranking = False
                    break
            
            if accion == "menu":
                break
    
    pygame.display.flip()

pygame.quit()
