import os
import random

# ==========================================
# CÓDIGOS DE COLOR ANSI PARA LA TERMINAL
# ==========================================
VERDE = '\033[92m'
ROJO = '\033[91m'
CYAN = '\033[96m'
AMARILLO = '\033[93m'
RESET = '\033[0m'

# ==========================================
# CONSTANTES DE ARCHIVOS
# ==========================================
FILE_MUJERES = 'IntegrantesMujeres.txt'
FILE_HOMBRES = 'IntegrantesHombres.txt'
FILE_NOPASAN = 'NoPasan.txt'
FILE_PAREJAS = 'ParejasEchas.txt'

# ==========================================
# FUNCIONES DE UTILIDAD (I/O Y ARCHIVOS)
# ==========================================

def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def asegurar_archivos():
    """Crea los archivos .txt si no existen."""
    archivos = [FILE_MUJERES, FILE_HOMBRES, FILE_NOPASAN, FILE_PAREJAS]
    for archivo in archivos:
        if not os.path.exists(archivo):
            with open(archivo, 'w', encoding='utf-8') as f:
                pass

def leer_lista(archivo):
    """Lee un archivo y devuelve una lista de líneas limpias."""
    if not os.path.exists(archivo):
        return []
    with open(archivo, 'r', encoding='utf-8') as f:
        return [linea.strip() for linea in f.readlines() if linea.strip()]

def guardar_lista(archivo, lista):
    """Sobreescribe un archivo con la lista proporcionada."""
    with open(archivo, 'w', encoding='utf-8') as f:
        for item in lista:
            f.write(item + '\n')

def agregar_a_archivo(archivo, linea):
    """Añade una sola línea al final de un archivo."""
    with open(archivo, 'a', encoding='utf-8') as f:
        f.write(linea + '\n')

def cargar_historial_parejas():
    """Lee ParejasEchas.txt y devuelve un set de tuplas."""
    historial = []
    lineas = leer_lista(FILE_PAREJAS)
    for linea in lineas:
        partes = linea.split(',')
        if len(partes) == 2:
            historial.append((partes[0].strip(), partes[1].strip()))
    return historial

# ==========================================
# LÓGICA DE MENÚS Y GESTIÓN
# ==========================================

def mostrar_banner():
    """Imprime el arte ASCII del sistema."""
    print(f"{CYAN}")
    print("  ____  _     _                        ")
    print(" / ___|(_)___| |_ ___ _ __ ___   __ _  ")
    print(" \___ \| / __| __/ _ \ '_ ` _ \ / _` | ")
    print("  ___) | \__ \ ||  __/ | | | | | (_| | ")
    print(" |____/|_|___/\__\___|_| |_| |_|\__,_| ")
    print("          D E  P A R E J A S           ")
    print(f"{RESET}")

def gestionar_lista(titulo, archivo_objetivo, archivo_nopasan):
    """Submenú para Mujeres u Hombres con opción de agregar a NoPasan."""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        print(f"--- {titulo} ---")
        
        lista_actual = sorted(leer_lista(archivo_objetivo))
        lista_nopasan = set(leer_lista(archivo_nopasan))

        if not lista_actual:
            print(f"{AMARILLO}La lista está vacía.{RESET}")
        else:
            for i, nombre in enumerate(lista_actual, 1):
                color = ROJO if nombre in lista_nopasan else VERDE
                print(f"{i}.- {color}{nombre}{RESET}")
        
        print("\nOpciones:")
        print("1.- Agregar integrante")
        print("2.- Quitar integrante")
        print("3.- Agregar integrante que no pasa")
        print("4.- Regresar")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == '1':
            nuevo = input("Nombre del nuevo integrante: ").strip()
            if nuevo:
                lista_actual.append(nuevo)
                guardar_lista(archivo_objetivo, lista_actual)
        
        elif opcion == '2':
            try:
                num = int(input("Número del integrante a quitar: "))
                if 1 <= num <= len(lista_actual):
                    lista_actual.pop(num - 1)
                    guardar_lista(archivo_objetivo, lista_actual)
            except ValueError: pass

        elif opcion == '3':
            try:
                num = int(input("Número del integrante que no pasa: "))
                if 1 <= num <= len(lista_actual):
                    nombre = lista_actual[num - 1]
                    if nombre not in lista_nopasan:
                        agregar_a_archivo(FILE_NOPASAN, nombre)
                        print(f"{ROJO}{nombre} agregado a NoPasan.txt{RESET}")
                        input("Presiona Enter...")
            except ValueError: pass
            
        elif opcion == '4':
            break

def gestionar_no_pasan():
    """Submenú para ver y quitar integrantes de la lista NoPasan."""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        print("--- Integrantes que no pasan ---")
        lista = sorted(leer_lista(FILE_NOPASAN))
        
        if not lista:
            print(f"{VERDE}Nadie está en esta lista.{RESET}")
        else:
            for i, nombre in enumerate(lista, 1):
                print(f"{i}.- {ROJO}{nombre}{RESET}")
        
        print("\nOpciones:")
        print("1.- Quitar Integrante de esta lista")
        print("2.- Regresar")
        
        opcion = input("\nOpción: ")
        if opcion == '1' and lista:
            try:
                num = int(input("Número a quitar: "))
                if 1 <= num <= len(lista):
                    lista.pop(num - 1)
                    guardar_lista(FILE_NOPASAN, lista)
            except ValueError: pass
        elif opcion == '2':
            break

def consultar_parejas():
    """Muestra todas las parejas registradas en el historial."""
    limpiar_pantalla()
    mostrar_banner()
    print(f"{CYAN}--- Historial Completo de Parejas ---{RESET}\n")
    historial = leer_lista(FILE_PAREJAS)
    if not historial:
        print("No hay parejas registradas aún.")
    else:
        for i, registro in enumerate(historial, 1):
            p = registro.split(',')
            print(f"{i}. [Estudiante] {VERDE}{p[0]}{RESET} -- [Acompañante] {AMARILLO}{p[1]}{RESET}")
    input("\nPresiona Enter para regresar...")

def generar_parejas_optimizadas(pool, historial, num_parejas):
    """Intenta generar parejas únicas comparando con el historial."""
    mejor_intento = []
    min_repeticiones = float('inf')
    historial_set = set(historial)

    for _ in range(2000):
        random.shuffle(pool)
        actuales = []
        repeticiones = 0
        for i in range(num_parejas):
            p = (pool[2*i], pool[2*i+1])
            actuales.append(p)
            if p in historial_set:
                repeticiones += 1
        
        if repeticiones < min_repeticiones:
            min_repeticiones = repeticiones
            mejor_intento = actuales
        if min_repeticiones == 0: break

    return mejor_intento, min_repeticiones

def menu_crear_parejas():
    """Lógica principal de creación con verificación matemática."""
    limpiar_pantalla()
    mostrar_banner()
    print("--- Crear Parejas ---")
    print("1.- Mujeres\n2.- Hombres\n3.- Cancelar")
    op = input("Opción: ")
    
    archivo = FILE_MUJERES if op == '1' else FILE_HOMBRES if op == '2' else None
    if not archivo: return

    todos = leer_lista(archivo)
    no_pasan = set(leer_lista(FILE_NOPASAN))
    disponibles = [p for p in todos if p not in no_pasan]
    historial = cargar_historial_parejas()

    # --- VERIFICACIÓN MATEMÁTICA ---
    # Una pareja es (A, B). Total de combinaciones ordenadas es N * (N-1)
    n = len(disponibles)
    if n < 2:
        print(f"{ROJO}No hay suficientes personas disponibles.{RESET}")
        input(); return

    max_posibles = n * (n - 1)
    # Filtramos el historial para ver cuántas de esta lista específica ya se hicieron
    historial_filtrado = [p for p in historial if p[0] in disponibles and p[1] in disponibles]
    
    if len(set(historial_filtrado)) >= max_posibles:
        print(f"\n{ROJO}Matemáticamente, todas las parejas posibles han sido creadas.{RESET}")
        print(f"{CYAN}Parejas históricas de esta lista:{RESET}")
        for p in set(historial_filtrado):
            print(f"- {p[0]} y {p[1]}")
        input("\nPresiona Enter..."); return

    try:
        cant = int(input(f"¿Cuántas parejas generar? (Máx sugerido {n//2}): "))
    except: return

    if n < (cant * 2):
        print(f"{ROJO}Insuificientes integrantes.{RESET}"); input(); return

    # Mostrar anteriores
    print(f"\n{AMARILLO}Parejas creadas anteriormente:{RESET}")
    for p in historial[-10:]: # Mostramos las últimas 10 por brevedad
        print(f" [H] {p[0]} -- {p[1]}")

    # Generar y mostrar nuevas
    nuevas, reps = generar_parejas_optimizadas(disponibles, historial, cant)
    
    print(f"\n{VERDE}Parejas creadas ahora:{RESET}")
    for i, p in enumerate(nuevas, 1):
        print(f" {i}. [Estudiante] {VERDE}{p[0]}{RESET} -- [Acompañante] {AMARILLO}{p[1]}{RESET}")
        agregar_a_archivo(FILE_PAREJAS, f"{p[0]},{p[1]}")

    input("\nPresiona Enter para finalizar...")

# ==========================================
# FLUJO PRINCIPAL
# ==========================================

def main():
    asegurar_archivos()
    while True:
        limpiar_pantalla()
        mostrar_banner()
        print("Menú Principal:")
        print("1.- Ver Integrantes mujeres")
        print("2.- Ver Integrantes hombres")
        print("3.- Ver Integrantes que no pasan")
        print("4.- Crear parejas")
        print("5.- Consultar parejas creadas")
        print("6.- Salir")
        
        opcion = input("\n[Terminal] ~ $ ")
        
        if opcion == '1':
            gestionar_lista("Integrantes Mujeres", FILE_MUJERES, FILE_NOPASAN)
        elif opcion == '2':
            gestionar_lista("Integrantes Hombres", FILE_HOMBRES, FILE_NOPASAN)
        elif opcion == '3':
            gestionar_no_pasan()
        elif opcion == '4':
            menu_crear_parejas()
        elif opcion == '5':
            consultar_parejas()
        elif opcion == '6':
            print(f"{VERDE}Sincronización finalizada. Saliendo...{RESET}")
            break

if __name__ == "__main__":
    if os.name == 'nt': os.system('') 
    main()