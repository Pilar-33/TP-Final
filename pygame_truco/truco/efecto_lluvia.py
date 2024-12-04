import pygame
import random
import os

def crear_carta(x):
    """Crea un diccionario con los datos de una carta"""
    return {
        'x': x,
        'y': -100,
        'velocidad': random.uniform(1, 3),
        'rotacion': random.randint(0, 360),
        'vel_rotacion': random.uniform(-2, 2),
        'imagen': None
    }

def cargar_imagenes_cartas(ruta_cartas):
    """Carga las imágenes de las cartas y retorna una lista"""
    return [pygame.transform.scale(
            pygame.image.load(os.path.join(ruta_cartas, archivo)), 
            (50, 70)
        ) 
        for archivo in os.listdir(ruta_cartas) 
        if archivo.endswith('.jpg')]

def crear_lluvia_cartas():
    """Crea una lista de diccionarios representando las cartas"""
    imagenes_cartas = cargar_imagenes_cartas("./assets/cartas/")
    cartas = []
    
    for _ in range(15):
        carta = crear_carta(random.randint(0, 800))
        carta['imagen'] = random.choice(imagenes_cartas)
        cartas.append(carta)
    
    return cartas

def actualizar_posicion_carta(carta):
    """Actualiza la posición de una carta"""
    carta['y'] += carta['velocidad']
    carta['rotacion'] += carta['vel_rotacion']
    
    if carta['y'] > 600:
        carta['y'] = -100
        carta['x'] = random.randint(0, 800)
    
    return carta

def dibujar_carta(ventana, carta):
    """Dibuja una carta en la ventana"""
    imagen_rotada = pygame.transform.rotate(carta['imagen'], carta['rotacion'])
    rect = imagen_rotada.get_rect(center=(carta['x'], carta['y']))
    ventana.blit(imagen_rotada, rect)

def actualizar_lluvia(cartas, ventana):
    """Actualiza y dibuja todas las cartas"""
    for carta in cartas:
        carta = actualizar_posicion_carta(carta)
        dibujar_carta(ventana, carta)
