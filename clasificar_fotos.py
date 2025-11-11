"""
Script para clasificar las fotos basándose en las selecciones del usuario
Lee el archivo JSON exportado del selector y organiza las fotos en carpetas.
"""

import os
import shutil
import json

# IMPORTANTE: Reemplaza esta ruta con la ruta del archivo JSON descargado del selector
# Ejemplo: r"C:\Users\foro7\Downloads\seleccion-megan-2025-11-11.json"
archivo_json = r"C:\Users\foro7\Downloads\seleccion-megan-[FECHA].json"

# Directorio donde están las fotos originales (en JPG)
carpeta_origen = r"F:\2025\08\09\fotos\fiesta\SI\SI\reencuadradas\editadas\descomprimidas"

# Directorio base donde se guardarán las fotos clasificadas
carpeta_destino_base = r"F:\2025\08\09\fotos\clasificadas"

def cargar_selecciones(ruta_json):
    """Carga las selecciones desde el archivo JSON"""
    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {ruta_json}")
        print("\nAsegúrate de:")
        print("1. Descargar el reporte desde el selector de fotos")
        print("2. Actualizar la variable 'archivo_json' con la ruta correcta")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: El archivo {ruta_json} no es un JSON válido")
        return None

# Cargar selecciones
print(f"Cargando selecciones desde: {archivo_json}")
selecciones_json = cargar_selecciones(archivo_json)

if selecciones_json is None:
    print("\nNo se pudo cargar el archivo de selecciones. Saliendo...")
    exit(1)

# Mostrar información del archivo
print(f"\n{'='*60}")
print(f"INFORMACIÓN DEL ARCHIVO")
print(f"{'='*60}")
print(f"Nombre: {selecciones_json.get('nombre', 'N/A')}")
print(f"Contratante: {selecciones_json.get('contratante', 'N/A')}")
print(f"Fecha del evento: {selecciones_json.get('fecha_evento', 'N/A')}")
print(f"Total de fotos: {selecciones_json.get('total_fotos', 0)}")
print(f"\nEstadísticas:")
stats = selecciones_json.get('estadisticas', {})
print(f"  - Ampliación: {stats.get('ampliacion', 0)}")
print(f"  - Impresión: {stats.get('impresion', 0)}")
print(f"  - Redes Sociales: {stats.get('redes_sociales', 0)}")
print(f"  - Descartadas: {stats.get('descartada', 0)}")
print(f"  - Sin clasificar: {stats.get('sinClasificar', 0)}")
print(f"{'='*60}\n")

# Crear carpetas de destino
categorias = ["ampliacion", "impresion", "redes_sociales", "invitacion", "descartada", "sin_clasificar"]
for categoria in categorias:
    carpeta = os.path.join(carpeta_destino_base, categoria)
    os.makedirs(carpeta, exist_ok=True)
    print(f"✓ Carpeta creada: {carpeta}")

# Crear diccionario de selecciones indexado por número de foto
selecciones_dict = {}
for sel in selecciones_json.get("selecciones", []):
    selecciones_dict[sel["numero_foto"]] = sel

# Procesar todas las fotos
total_fotos = selecciones_json.get("total_fotos", 0)
contador = {"ampliacion": 0, "impresion": 0, "redes_sociales": 0, "invitacion": 0, "descartada": 0, "sin_clasificar": 0}

print(f"\n{'='*60}")
print(f"PROCESANDO {total_fotos} FOTOS...")
print(f"{'='*60}\n")

for i in range(1, total_fotos + 1):
    # Buscar el archivo original (puede tener diferentes nombres)
    # Intentar varios patrones comunes
    posibles_nombres = [
        f"foto7_{i:04d}.jpg",
        f"DSC_{i:04d}.jpg",
        f"IMG_{i:04d}.jpg",
        f"foto_{i:04d}.jpg",
        f"{i:04d}.jpg",
        f"foto7_{i:04d}.JPG",
        f"DSC_{i:04d}.JPG",
        f"IMG_{i:04d}.JPG",
        f"foto_{i:04d}.JPG",
        f"{i:04d}.JPG"
    ]

    ruta_origen = None
    nombre_original = None

    for nombre in posibles_nombres:
        ruta_test = os.path.join(carpeta_origen, nombre)
        if os.path.exists(ruta_test):
            ruta_origen = ruta_test
            nombre_original = nombre
            break

    # Si no se encontró, intentar listar el directorio
    if ruta_origen is None:
        print(f"[!] Advertencia: No se encontró foto #{i} con ningún patrón conocido")
        continue

    # Verificar si la foto tiene clasificación
    if i in selecciones_dict:
        sel = selecciones_dict[i]

        # Determinar la(s) categoría(s) de la foto
        categorias_foto = []
        if sel.get("ampliacion"):
            categorias_foto.append("ampliacion")
        if sel.get("impresion"):
            categorias_foto.append("impresion")
        if sel.get("redes_sociales"):
            categorias_foto.append("redes_sociales")
        if sel.get("invitacion"):
            categorias_foto.append("invitacion")
        if sel.get("descartada"):
            categorias_foto.append("descartada")

        # Si no tiene ninguna categoría, clasificar como sin_clasificar
        if not categorias_foto:
            categorias_foto.append("sin_clasificar")

        # Copiar la foto a cada categoría correspondiente
        for categoria in categorias_foto:
            ruta_destino = os.path.join(carpeta_destino_base, categoria, nombre_original)
            shutil.copy2(ruta_origen, ruta_destino)
            contador[categoria] += 1
            print(f"[OK] Foto #{i:3d} ({nombre_original}) -> {categoria}")
    else:
        # Foto sin clasificación
        ruta_destino = os.path.join(carpeta_destino_base, "sin_clasificar", nombre_original)
        shutil.copy2(ruta_origen, ruta_destino)
        contador["sin_clasificar"] += 1
        print(f"[ ] Foto #{i:3d} ({nombre_original}) -> sin_clasificar")

# Resumen final
print(f"\n{'='*60}")
print("RESUMEN DE CLASIFICACIÓN")
print(f"{'='*60}")
print(f"Total de fotos procesadas: {total_fotos}")
print(f"\nFotos por categoría:")
for categoria, cantidad in contador.items():
    print(f"  - {categoria.ljust(20)}: {cantidad:3d} fotos")
print(f"\n[OK] ¡Clasificación completada!")
print(f"Carpeta de destino: {carpeta_destino_base}")
print(f"{'='*60}\n")

# Mostrar sugerencias de cambios si existen
cambios = selecciones_json.get("sugerencias_de_cambios", {})
if cambios.get("video") and cambios["video"] != "Sin cambios sugeridos":
    print("\n📹 SUGERENCIAS DE CAMBIOS EN EL VIDEO:")
    print("="*60)
    for cambio in cambios["video"]:
        print(f"  ⏱️  {cambio['minute']}: {cambio['change']}")

if cambios.get("fotos") and cambios["fotos"] != "Sin cambios sugeridos":
    print("\n📸 SUGERENCIAS DE CAMBIOS EN LAS FOTOS:")
    print("="*60)
    for cambio in cambios["fotos"]:
        print(f"  📷 Foto #{cambio['photoNumber']}: {cambio['change']}")
