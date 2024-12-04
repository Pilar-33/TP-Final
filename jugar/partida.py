from jugar.jugador_humano import *
from jugar.jugador_aleatorio import *
from jugar.jugador_estrategico import *
from jugar.cartas import *
from jugar.envido import *
from jugar.historial import*

# === Funciones de inicialización === #
def crear_oponente(tipo_oponente: str, nombre_oponente: str) -> dict:
    """Crea el oponente según el tipo seleccionado"""
    oponentes = {
        "Jugador Aleatorio": crear_jugador_aleatorio,
        "Jugador Estratégico": crear_jugador_estrategico 
    }
    nuevo_oponente = oponentes[tipo_oponente](nombre_oponente)
    return nuevo_oponente

def seleccionar_oponente() -> tuple:
    """Permite seleccionar el tipo de oponente y retorna tipo y nombre"""
    print("""\nSELECCIONE UN OPONENTE:
    1. Jugador Aleatorio.
    2. Jugador Estratégico.""")
    
    # Variables inicializadas
    seleccion_activa = True
    datos_oponente = ("", "")  # (tipo_oponente, nombre_oponente)
    
    while seleccion_activa:
        opcion = input("Ingrese una opción (1 o 2): ").strip()
        if opcion == "1":
            datos_oponente = ("Jugador Aleatorio", random.choice(NOMBRES_MAQUINA))
            seleccion_activa = False
        elif opcion == "2":
            datos_oponente = ("Jugador Estratégico", "Estratégico")
            seleccion_activa = False
        else:
            print("Opción inválida. Intente nuevamente.")
    
    return datos_oponente

def inicializar_jugadores() -> tuple:
    """Inicializa los jugadores y retorna una tupla con ambos"""
    nombre_jugador = input("Ingrese su nombre: ").strip()
    jugador = crear_jugador_humano(nombre_jugador)

    tipo_oponente, nombre_oponente = seleccionar_oponente()
    oponente = crear_oponente(tipo_oponente, nombre_oponente)
    
    return jugador, oponente

def seleccionar_modo_juego() -> int:
    """
    Permite seleccionar el modo de juego y retorna los
    puntos seleccionados.
    """
    opcion_puntos = {
    "1": 15,
    "2": 30
    }

    seleccion = input("""\nSELECCIONE UN MODO DE JUEGO:
    1. 15 puntos.
    2. 30 puntos. 
    Ingrese una opción (1 o 2): """).strip()

    while seleccion not in opcion_puntos:
        seleccion = input("""Opción inválida. Ingrese una opción válida (1 o 2): """)
    puntos_seleccionados = opcion_puntos[seleccion]
    return puntos_seleccionados

def determinar_mano() -> bool:
    """Determina aleatoriamente quién es mano"""
    es_mano = random.choice([True, False])
    return es_mano


# === Funciones de visualización === #
def mostrar_jugada(nombre_jugador: str, carta: dict) -> None:
    """Muestra la carta jugada por un jugador"""
    print(f"\n{nombre_jugador} jugó: {carta['palo']} {carta['valor']}")

def mostrar_estado_partida(jugador: dict, oponente: dict, modo_juego: int) -> None:
    """Muestra el estado actual de la partida"""
    print(f""" 
    === Puntaje actual ===
    {jugador['nombre']}: {jugador['puntos']} puntos.
    {oponente['nombre']}: {oponente['puntos']} puntos.
    Puntos para ganar: {modo_juego}.
    =====================""")

# === Funciones de envido === #
def manejar_envido(
    jugador: dict, oponente: dict, 
    es_mano_jugador: bool, modo_juego: int) -> tuple:
    """Manejo completo del envido con todas sus variantes"""
    opciones_canto = {
        1: "envido",
        2: "real envido",
        3: "falta envido"
    }
    
    print("\nCARTAS DEL JUGADOR:")
    for carta in jugador["cartas"]:
        print(f"{carta['palo']} {carta['valor']}")
    
    envido_jugador = calcular_envido(jugador["cartas"])
    envido_oponente = calcular_envido(oponente["cartas"])
    
    if es_mano_jugador:
        print(f"Tus puntos de envido: {envido_jugador}")
        print("Opciones de canto:")
        for key, valor in opciones_canto.items():
            print(f"{key}. {valor}")
        
        opcion = int(input("Elige tu canto (0 para no cantar): "))
        if opcion == 0:
            return 0, 0
            
        canto = opciones_canto[opcion]
        
        # Respuesta según tipo de oponente
        if oponente["tipo"] == "Jugador Estratégico":
            respuesta = responder_canto_estrategico(oponente["cartas"], canto, 
                                            oponente["puntos"], jugador["puntos"], 
                                            modo_juego)
        else:
            # Jugador aleatorio siempre acepta si tiene envido
            if envido_oponente > 20:
                respuesta = "quiero"
            else:
                respuesta = "no_quiero"  
        return determinar_puntos_envido(canto, respuesta, envido_jugador, envido_oponente)     
    else:
        # Oponente canta primero
        if oponente["tipo"] == "Jugador Estratégico":
            canto = cantar_envido_estrategico(oponente["cartas"], 
                                        oponente["puntos"], 
                                        jugador["puntos"],
                                        modo_juego)
        else:
            # Jugador aleatorio canta si tiene buenos puntos
            if envido_oponente > 25:
                canto = "envido"
            else:
                canto = "nada"
            
        if canto == "nada":
            return 0, 0
            
        # Jugador humano responde
        print(f"Oponente cantó: {canto}")
        print(f"Tus puntos de envido: {envido_jugador}")
        respuesta = input("¿Querés? (si/no): ").lower()
        respuesta = "quiero" if respuesta == "si" else "no_quiero"
        
        return determinar_puntos_envido(canto, respuesta, envido_oponente, envido_jugador)

# === Funciones de rondas === #
def manejar_ronda(jugador: dict, oponente: dict, ronda: int, es_mano_jugador: bool) -> tuple:
    """Maneja una ronda completa de juego del truco.
    Flujo de juego:
    1. Si el oponente es estratégico:
        - Usa lógica avanzada para seleccionar cartas.
        - Considera la carta del jugador si no es mano.
    2. Si el oponente es aleatorio:
        - Selecciona cartas al azar.
    3. El orden de juego respeta quién es mano.
    4. Muestra las jugadas realizadas."""
    
    print(f"\n=== Ronda {ronda + 1} ===")
    
    if oponente["tipo"] == "Jugador Estratégico":
        if es_mano_jugador:
            # Turno jugador
            carta_jugador = seleccionar_carta(jugador["cartas"])
            mostrar_jugada(jugador["nombre"], carta_jugador)
            # Turno oponente estratégico
            carta_oponente = jugar_carta_estrategica(oponente["cartas"], False, carta_jugador)
            mostrar_jugada(oponente["nombre"], carta_oponente)
        else:
            # Turno oponente estratégico
            carta_oponente = jugar_carta_estrategica(oponente["cartas"], True)
            mostrar_jugada(oponente["nombre"], carta_oponente)
            # Turno jugador
            carta_jugador = seleccionar_carta(jugador["cartas"])
            mostrar_jugada(jugador["nombre"], carta_jugador)
    else:
        # Lógica para jugador aleatorio
        if es_mano_jugador:
            # Turno jugador
            carta_jugador = seleccionar_carta(jugador["cartas"])
            mostrar_jugada(jugador["nombre"], carta_jugador)
            # Turno oponente aleatorio
            carta_oponente = jugar_carta_aleatoria(oponente["cartas"])
            mostrar_jugada(oponente["nombre"], carta_oponente)
        else:
            # Turno oponente aleatorio
            carta_oponente = jugar_carta_aleatoria(oponente["cartas"])
            mostrar_jugada(oponente["nombre"], carta_oponente)
            # Turno jugador
            carta_jugador = seleccionar_carta(jugador["cartas"])
            mostrar_jugada(jugador["nombre"], carta_jugador)
    
    cartas_jugadas = (carta_jugador, carta_oponente)
    return cartas_jugadas


# === Funciones de rondas === #
def determinar_ganador_ronda(carta_jugador: dict, carta_oponente: dict) -> int:
    """Determina el ganador de la ronda. Retorna 1 (jugador), -1 
    (oponente) o 0 (empate)"""
    resultado = 0
    if carta_jugador["jerarquia"] > carta_oponente["jerarquia"]:
        resultado = 1
    elif carta_jugador["jerarquia"] < carta_oponente["jerarquia"]:
        resultado = -1
    return resultado

def actualizar_puntajes(ganador: dict, puntos: int) -> None:
    """Actualiza los puntajes de los jugadores
    La función:
    1. Suma los nuevos puntos al total del ganador;
    2. Muestra mensaje con el resultado."""
    ganador["puntos"] += puntos
    print(f"\n{ganador['nombre']} gana {puntos} puntos!")
    
def mostrar_resultado_final(jugador: dict, oponente: dict) -> None:
    """Muestra el resumen final de la partida"""
    print(f"""\n\t=== Puntaje Final ===
    {jugador['nombre']}: {jugador['puntos']} puntos.
    {oponente['nombre']}: {oponente['puntos']} puntos.
    Ganó {jugador['nombre'] if jugador['puntos'] > oponente['puntos'] else oponente['nombre']}.
    =====================""")


# === Funciones principales === #
def jugar_partida(nombre_jugador: str, tipo_oponente: str, max_puntos: int) -> dict:
    """Maneja el flujo completo de una partida de truco."""
    
    # Inicialización del estado
    nombre_oponente = random.choice(NOMBRES_MAQUINA)
    
    estado_partida = {
        "jugador": {
            "nombre": nombre_jugador,
            "puntos": 0,
            "cartas": []
        },
        "oponente": {
            "nombre": nombre_oponente,
            "puntos": 0,
            "tipo": tipo_oponente,
            "cartas": []
        },
        "rondas_jugadas": [],
        "ganador": None
    }
    
    while estado_partida["jugador"]["puntos"] < max_puntos and estado_partida["oponente"]["puntos"] < max_puntos:
        mazo = crear_mazo(VALORES, PALOS)
        # Repartir cartas al inicio de cada mano
        repartir_cartas(estado_partida["jugador"], estado_partida["oponente"], mazo)
        
        # Determinar quién es mano
        es_mano_jugador = determinar_mano()
        
        mostrar_estado_partida(estado_partida["jugador"], estado_partida["oponente"], max_puntos)
        
        # Manejar el envido y sus variantes
        puntos_jugador, puntos_oponente = manejar_envido(
            estado_partida["jugador"],
            estado_partida["oponente"],
            es_mano_jugador,
            max_puntos
        )
        
        # Actualizar puntos del envido
        if puntos_jugador > 0:
            actualizar_puntajes(estado_partida["jugador"], puntos_jugador)
        if puntos_oponente > 0:
            actualizar_puntajes(estado_partida["oponente"], puntos_oponente)
        
        # Jugar las rondas si no se ganó por envido
        if estado_partida["jugador"]["puntos"] < max_puntos and estado_partida["oponente"]["puntos"] < max_puntos:
            for ronda in range(3):
                cartas_jugadas = manejar_ronda(
                    estado_partida["jugador"],
                    estado_partida["oponente"],
                    ronda,
                    es_mano_jugador
                )
                resultado_ronda = determinar_ganador_ronda(cartas_jugadas[0], cartas_jugadas[1])
                
                # Actualizar puntos de la ronda
                if resultado_ronda == 1:
                    actualizar_puntajes(estado_partida["jugador"], 1)
                elif resultado_ronda == -1:
                    actualizar_puntajes(estado_partida["oponente"], 1)
                
                estado_partida["rondas_jugadas"].append(cartas_jugadas)
    
    # Determinar ganador final
    estado_partida["ganador"] = estado_partida["jugador"] if estado_partida["jugador"]["puntos"] >= max_puntos else estado_partida["oponente"]
    guardar_resultado_partida(estado_partida["jugador"], estado_partida["oponente"], max_puntos)
    
    mostrar_resultado_final(estado_partida["jugador"], estado_partida["oponente"])
    return estado_partida


def iniciar_partida() -> dict:
    """Inicia una nueva partida"""
    nombre_jugador = input("Ingrese su nombre: ")
    tipo_oponente, _ = seleccionar_oponente()
    modo_juego = seleccionar_modo_juego()
    
    resultado_partida = jugar_partida(nombre_jugador, tipo_oponente, modo_juego)
    return resultado_partida
