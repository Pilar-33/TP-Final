import csv
import os

def inicializar_historial() -> None:
    """Crea el archivo de historial si no existe"""
    archivo = 'historial.csv'
    
    # Verifica si el archivo ya existe
    if not os.path.exists(archivo):

        with open(archivo, mode="a", newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow([
                "Jugador1",
                "Puntos1",
                "Jugador2", 
                "Puntos2",
                "Modo_Juego"
            ])
            
def guardar_resultado_partida(jugador: dict, oponente: dict, modo_juego: int, archivo: str = "historial.csv") -> None:
    """Guarda el resultado de la partida en un archivo CSV."""
    with open(archivo, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([
            jugador["nombre"], 
            jugador["puntos"],
            oponente["nombre"],
            oponente["puntos"],
            modo_juego
        ])
        

def obtener_ranking():
    from os.path import exists
    if not exists("historial.csv"):
        return False
        
    ranking = {}
    with open("historial.csv", "r", encoding='utf-8') as archivo:
        lineas = archivo.readlines()[1:]  # Saltamos encabezado
        
    for linea in lineas:
        datos = linea.strip().split(',')
        jugador1, puntos1, jugador2, puntos2 = datos[0:4]
        
        # Procesamos jugador1
        if jugador1 not in ranking:
            ranking[jugador1] = {'nombre': jugador1, 'victorias': 0, 'partidas': 0}
        ranking[jugador1]['partidas'] += 1
        if int(puntos1) > int(puntos2):
            ranking[jugador1]['victorias'] += 1
            
        # Procesamos jugador2
        if jugador2 not in ranking:
            ranking[jugador2] = {'nombre': jugador2, 'victorias': 0, 'partidas': 0}
        ranking[jugador2]['partidas'] += 1
        if int(puntos2) > int(puntos1):
            ranking[jugador2]['victorias'] += 1
    
    return list(ranking.values()) if ranking else False


def mostrar_historial_personal(nombre_jugador: str) -> None:
    print(f"\n⭐ RANKING PERSONAL DE {nombre_jugador.upper()} ⭐")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    partidas_encontradas = False
    
    with open("historial.csv", "r", encoding="utf-8") as archivo:
        reader = csv.reader(archivo)
        for partida in reader:
            # Si el jugador aparece como jugador1 o jugador2
            if nombre_jugador.lower() in [partida[0].lower(), partida[2].lower()]:
                partidas_encontradas = True
                
                # Determinar si ganó o perdió
                if nombre_jugador.lower() == partida[0].lower():
                    resultado = "🏆 VICTORIA" if int(partida[1]) > int(partida[3]) else "❌ DERROTA"
                    puntos_propios = partida[1]
                    oponente = partida[2]
                    puntos_oponente = partida[3]
                else:
                    resultado = "🏆 VICTORIA" if int(partida[3]) > int(partida[1]) else "❌ DERROTA"
                    puntos_propios = partida[3]
                    oponente = partida[0]
                    puntos_oponente = partida[1]
                
                print(f"\n    🤺 Contra: {oponente}")
                print(f"    ⚡ Resultado: {resultado}")
                print(f"    🎯 Puntuación: {puntos_propios}-{puntos_oponente}")
                print(f"    🎮 Modo: {partida[4]} puntos")
                print("    ──────────────────────────────")
    
    if not partidas_encontradas:
        print(f"\n❌ No se encontraron partidas para {nombre_jugador}")

def mostrar_estadisticas_detalladas() -> None:
    ranking = obtener_ranking()

    if not ranking:
        print("\nNo hay estadísticas disponibles todavía.")
        return
    
    # Historial de Partidas
    print("\n📜 HISTORIAL DE PARTIDAS 📜")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
    with open("historial.csv", "r", encoding="utf-8") as archivo:
        reader = csv.reader(archivo)
        for partida in reader:
            print(f"    🤺 {partida[0]} vs {partida[2]}")
            print(f"    🎯 Puntuación: {partida[1]} - {partida[3]}")
            print(f"    🎮 Modo: {partida[4]} puntos")
            print(f"    👑 Ganador: {partida[0] if int(partida[1]) > int(partida[3]) else partida[2]}")
            print("    ──────────────────────────────")
