import pygame

def dibujar_barra_titulo(
    ventana, ancho, color_barra, icono_grande, color_boton_cerrar, color_boton_cerrar_hower, color_texto
):
    """
    Dibuja la barra de título en la ventana.
    Parámetros:
        ventana: objeto pygame.Surface donde se dibuja.
        ancho: ancho de la ventana.
        color_barra: color de la barra superior.
        icono_grande: imagen del icono en tamaño reducido.
        color_boton_cerrar: color del botón de cerrar.
        color_boton_cerrar_hower: color del botón de cerrar al pasar el mouse.
        color_texto: color del texto en la barra.
    """
    fuente = pygame.font.SysFont("Arial", 24, bold=True)
    titulo = "JUEGO TRUCO"
    boton_x, boton_y, boton_ancho, boton_alto = 760, 5, 30, 30

    # Dibujar barra
    pygame.draw.rect(ventana, color_barra, (0, 0, ancho, 40))

    # Obtener posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Botón cerrar
    if boton_x <= mouse_x <= boton_x + boton_ancho and boton_y <= mouse_y <= boton_y + boton_alto:
        pygame.draw.rect(
            ventana, color_boton_cerrar_hower, (boton_x, boton_y, boton_ancho, boton_alto)
        )
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            exit()
    else:
        pygame.draw.rect(
            ventana, color_boton_cerrar, (boton_x, boton_y, boton_ancho, boton_alto)
        )

    # Dibujar X en el botón
    texto_cerrar = fuente.render("X", True, color_texto)
    texto_ancho, texto_alto = texto_cerrar.get_size()
    x_centrada = boton_x + (boton_ancho - texto_ancho) // 2
    y_centrada = boton_y + (boton_alto - texto_alto) // 2
    ventana.blit(texto_cerrar, (x_centrada, y_centrada))

    # Dibujar icono y título
    ventana.blit(icono_grande, (5, 4))
    texto_renderizado = fuente.render(titulo, True, color_texto)
    ventana.blit(texto_renderizado, (50, 5))
