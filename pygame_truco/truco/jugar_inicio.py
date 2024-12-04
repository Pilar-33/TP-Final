
import pygame 
import os
import pygame_gui
from pygame_gui.elements import*
from pygame_gui.core import*
import random
from pygame.locals import*
from truco.barra_titulo import*
from truco.ronda_truco import*
from truco.jugadores import*


#  rutas absolutas para los assets
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_ASSETS = os.path.join(RUTA_BASE, "assets")
RUTA_CARTAS = os.path.join(RUTA_ASSETS, "cartas")

# Constantes para la barra de título
COLOR_BARRA = (50, 50, 50)
COLOR_BOTON_CERRAR = (200, 0, 0)
COLOR_BOTON_CERRAR_HOVER = (255, 0, 0)
COLOR_TEXTO = (255, 255, 255)

# Constantes de la ventana
ANCHO = 800
ALTO = 600

# Inicialización de pygame y la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))

# Cargar imágenes
ruta_assets = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
imagen_fondo = pygame.image.load(os.path.join(ruta_assets, 'fondos', 'mesa.jpg'))
dorso = pygame.image.load(os.path.join(ruta_assets, 'dorso', 'dorso1.jpg'))

# Cargar y redimensionar el icono
ICONO_ORIGINAL = pygame.image.load(os.path.join(ruta_assets, 'cartas', '1_basto.jpg'))
ICONO_GRANDE = pygame.transform.scale(ICONO_ORIGINAL, (40, 40))

# Ajustar tamaño de las imágenes
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

# Variables globales
puntos_objetivo = 0
mano_jugador = []
mano_maquina = []
puntos_jugador = 0
puntos_maquina = 0

def seleccionar_puntos():
    global puntos_objetivo
    fuente = pygame.font.Font(None, 48)  # Aumentado tamaño de fuente

    # Botones más grandes y centrados
    rect_15 = pygame.Rect(250, 250, 150, 80)  # Aumentado tamaño y ajustado posición
    rect_30 = pygame.Rect(450, 250, 150, 80)  # Aumentado tamaño y ajustado posición

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == MOUSEBUTTONDOWN:
                if rect_15.collidepoint(mouse_pos):
                    puntos_objetivo = 15
                    return
                if rect_30.collidepoint(mouse_pos):
                    puntos_objetivo = 30
                    return

        ventana.blit(imagen_fondo, (0, 0))
        dibujar_barra_titulo(
            ventana,
            ANCHO,
            COLOR_BARRA,
            ICONO_GRANDE,
            COLOR_BOTON_CERRAR,
            COLOR_BOTON_CERRAR_HOVER,
            COLOR_TEXTO
        )

        # Dibujar botones más grandes
        color_15 = (150, 150, 150) if rect_15.collidepoint(mouse_pos) else (100, 100, 100)
        color_30 = (150, 150, 150) if rect_30.collidepoint(mouse_pos) else (100, 100, 100)

        pygame.draw.rect(ventana, color_15, rect_15)
        pygame.draw.rect(ventana, color_30, rect_30)

        # Textos centrados
        texto_titulo = fuente.render("Seleccione los puntos para jugar:", True, (255, 255, 255))
        texto_15 = fuente.render("15", True, (255, 255, 255))
        texto_30 = fuente.render("30", True, (255, 255, 255))

        ventana.blit(texto_titulo, (150, 150))  # Ajustado posición
        ventana.blit(texto_15, (310, 275))  # Ajustado posición
        ventana.blit(texto_30, (510, 275))  # Ajustado posición

        pygame.display.flip()

def crear_mazo():
    palos = ['espada', 'basto', 'oro', 'copa']
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    mazo = []

    ruta_cartas = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'cartas')
    for palo in palos:
        for numero in numeros:
            nombre_archivo = f'{numero}_{palo}.jpg'
            ruta_imagen = os.path.join(ruta_cartas, nombre_archivo)

            if os.path.exists(ruta_imagen):
                mazo.append({'palo': palo, 'numero': numero, 'imagen': pygame.image.load(ruta_imagen)})
            else:
                print(f"Falta la carta: {nombre_archivo}")

    random.shuffle(mazo)
    return mazo

def repartir_cartas(jugadores):
    mazo = crear_mazo()
    random.shuffle(mazo)
    
    separacion_cartas = 120
    pos_jugador = [(200 + i * separacion_cartas, 400) for i in range(3)]
    pos_maquina = [(200 + i * separacion_cartas, 100) for i in range(3)]
    tamaño_carta = (100, 140)
    cartas_repartidas = []
    
    # Asignar cartas a los jugadores
    jugadores["jugador"]["cartas"] = mazo[0:3]
    jugadores["oponente"]["cartas"] = mazo[3:6]
    
    # Animación de repartir
    for i in range(6):
        carta_actual = mazo[i]
        pos_final = pos_jugador[i % 3] if i < 3 else pos_maquina[i % 3]
        cartas_repartidas.append((carta_actual, pos_final, i < 3))
        
        for paso in range(30):
            ventana.blit(imagen_fondo, (0, 0))
            dibujar_barra_titulo(
                ventana,
                ANCHO,
                COLOR_BARRA,
                ICONO_GRANDE,
                COLOR_BOTON_CERRAR,
                COLOR_BOTON_CERRAR_HOVER,
                COLOR_TEXTO
            )
            
            # Dibuja las cartas ya repartidas
            for carta, pos, es_jugador in cartas_repartidas[:-1]:
                if es_jugador:
                    ventana.blit(pygame.transform.scale(carta['imagen'], tamaño_carta), pos)
                else:
                    ventana.blit(pygame.transform.scale(dorso, tamaño_carta), pos)
            
            # Anima la carta actual
            pos_x = ANCHO // 2 + (pos_final[0] - ANCHO // 2) * paso / 30
            pos_y = ALTO // 2 + (pos_final[1] - ALTO // 2) * paso / 30
            
            if i < 3:
                ventana.blit(pygame.transform.scale(carta_actual['imagen'], tamaño_carta), (pos_x, pos_y))
            else:
                ventana.blit(pygame.transform.scale(dorso, tamaño_carta), (pos_x, pos_y))
            
            pygame.display.flip()
            pygame.time.delay(20)
    
    # Mantener las cartas visibles al final
    ventana.blit(imagen_fondo, (0, 0))
    dibujar_barra_titulo(
        ventana,
        ANCHO,
        COLOR_BARRA,
        ICONO_GRANDE,
        COLOR_BOTON_CERRAR,
        COLOR_BOTON_CERRAR_HOVER,
        COLOR_TEXTO
    )
    
    for carta, pos, es_jugador in cartas_repartidas:
        if es_jugador:
            ventana.blit(pygame.transform.scale(carta['imagen'], tamaño_carta), pos)
        else:
            ventana.blit(pygame.transform.scale(dorso, tamaño_carta), pos)
    
    pygame.display.flip()
    
    return jugadores

def obtener_nombre_jugador(ventana, manager):
    reloj = pygame.time.Clock()

    # Cargar la imagen de fondo
    fondo_imagen = pygame.image.load("assets/fondos/mesa.jpg")

    fondo_imagen = pygame.transform.scale(fondo_imagen, (ANCHO, ALTO))  

    # Texto del título "Ingrese su nombre"
    fuente_titulo = pygame.font.Font(None, 50)  
    texto_titulo = fuente_titulo.render("Ingrese su nombre:", True, (255, 255, 255))  

    # Crear entrada de texto con estilo
    entrada_texto = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((ANCHO // 2 - 150, ALTO // 2), (300, 40)),  
        manager=manager
    )

    # Personalización del tema
    manager.get_theme().load_theme({
        '#entrada_nombre': {
            'font': {
                'size': '24',  
                'bold': True
            },
            'colours': {
                'normal_text': '#FFFFFF',  
                'dark_bg': '#333333',  
            }
        }
    })

    esperando_nombre = True
    nombre = ""
    
    while esperando_nombre:
        tiempo_delta = reloj.tick(60) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and entrada_texto.get_text().strip():
                    nombre = entrada_texto.get_text()
                    esperando_nombre = False
            
            manager.process_events(evento)
        
        manager.update(tiempo_delta)
        
        # Dibujar fondo, título y la interfaz
        ventana.blit(fondo_imagen, (0, 0))  # Dibuja la imagen de fondo
        ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 2 - 100))  
        manager.draw_ui(ventana)
        pygame.display.update()
    
    entrada_texto.kill()
    return nombre


def dibujar_cartas_oponente(ventana, cartas):
    # Posiciones fijas para las cartas del oponente
    posiciones = [
        (ANCHO//2 - 120, 100),
        (ANCHO//2, 100),
        (ANCHO//2 + 120, 100)
    ]
    
    dorso = pygame.image.load("assets/dorso/dorso1.jpg")
    dorso = pygame.transform.scale(dorso, (80, 120))
    
    # Dibujar cada carta del oponente como dorso
    for i in range(len(cartas)):
        ventana.blit(dorso, posiciones[i])


def dibujar_cartas_jugador(ventana, cartas):
    """
    Dibuja las cartas del jugador en la ventana.
    """
    ANCHO = ventana.get_width()
    ALTO = ventana.get_height()

    posiciones = [
        (ANCHO // 2 - 120, ALTO - 180),  # Carta izquierda
        (ANCHO // 2, ALTO - 180),       # Carta central
        (ANCHO // 2 + 120, ALTO - 180)  # Carta derecha
    ]

    tamaño_carta = (80, 120)  
    for i, carta in enumerate(cartas):
        if i < len(posiciones):  
            ruta_carta = os.path.join(RUTA_CARTAS, f"{carta['numero']}_{carta['palo']}.jpg")
            if os.path.exists(ruta_carta):  # Verificar que la imagen existe
                imagen_carta = pygame.image.load(ruta_carta)
                imagen_carta = pygame.transform.scale(imagen_carta, tamaño_carta)
                ventana.blit(imagen_carta, posiciones[i])
            else:
                print(f"Error: No se encontró la imagen de la carta {carta['numero']}_{carta['palo']}.jpg")

def jugar():
    ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.NOFRAME)
    manager = pygame_gui.UIManager((ANCHO, ALTO))
    reloj = pygame.time.Clock()

    # Fondo
    imagen_fondo = pygame.image.load(os.path.join(RUTA_ASSETS, "fondos", "mesa.jpg"))
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

    # Barra de título
    barra_titulo = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect(0, 0, ANCHO, 40),
        manager=manager
    )
    titulo = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((ANCHO // 2 - 50, 5), (100, 30)),
        text="TRUCO",
        manager=manager,
        container=barra_titulo
    )
    
    boton_cerrar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((ANCHO - 40, 5), (30, 30)),
        text="X",
        manager=manager,
        container=barra_titulo
    )

    # Obtener nombre del jugador
    nombre_jugador = obtener_nombre_jugador(ventana, manager)
    if nombre_jugador is None:
        return False

    jugador = crear_jugador_humano(nombre_jugador)
    oponente = crear_jugador_aleatorio(random.choice(NOMBRES_MAQUINA))
    jugadores = {"jugador": jugador, "oponente": oponente}

    # Repartir cartas
    jugadores = repartir_cartas(jugadores)

    # Panel de cantos
    panel_envido = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((20, ALTO - 200), (150, 150)),
        manager=manager
    )
    boton_envido = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (130, 30)),
        text="Envido",
        container=panel_envido,
        manager=manager
    )
    boton_real_envido = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 50), (130, 30)),
        text="Real Envido",
        container=panel_envido,
        manager=manager
    )
    boton_falta_envido = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 90), (130, 30)),
        text="Falta Envido",
        container=panel_envido,
        manager=manager
    )

    jugando = True
    while jugando:
        tiempo_delta = reloj.tick(60) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            if evento.type == pygame.USEREVENT:
                if evento.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if evento.ui_element == boton_cerrar:
                        jugando = False
                    elif evento.ui_element == boton_envido:
                        print("Envido cantado")
                    elif evento.ui_element == boton_real_envido:
                        print("Real Envido cantado")
                    elif evento.ui_element == boton_falta_envido:
                        print("Falta Envido cantado")
            manager.process_events(evento)

        manager.update(tiempo_delta)

        # Dibujar fondo
        ventana.blit(imagen_fondo, (0, 0))

        # Dibujar cartas
        if "cartas" in jugadores["jugador"]:
            dibujar_cartas_jugador(ventana, jugadores["jugador"]["cartas"])
        if "cartas" in jugadores["oponente"]:
            dibujar_cartas_oponente(ventana, jugadores["oponente"]["cartas"])

        # Dibujar interfaz
        manager.draw_ui(ventana)
        pygame.display.update()

    return True
