"""
Script para convertir fotos JPG a WebP y contarlas
Convierte todas las fotos de las carpetas de origen a formato WebP
y las numera secuencialmente para el selector de fotos.
"""

import os
from PIL import Image
from pathlib import Path

# Configuración de directorios
carpeta_fiesta = r"F:\2025\08\09\fotos\fiesta\SI\SI\reencuadradas\editadas\descomprimidas"
carpeta_sesion = r"F:\2025\08\09\fotos\sesion\editar"
carpeta_destino = r"C:\Users\foro7\xv-anos-megan\images"

# Crear carpeta de destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

def convertir_a_webp(ruta_origen, ruta_destino, calidad=85):
    """Convierte una imagen JPG a WebP con la calidad especificada, respetando orientación EXIF"""
    try:
        with Image.open(ruta_origen) as img:
            # Aplicar orientación EXIF si existe
            try:
                # Obtener la orientación EXIF
                exif = img._getexif()
                if exif is not None:
                    orientation_key = 274  # Código EXIF para orientación
                    if orientation_key in exif:
                        orientation = exif[orientation_key]

                        # Aplicar la rotación según el valor EXIF
                        rotations = {
                            3: Image.ROTATE_180,
                            6: Image.ROTATE_270,
                            8: Image.ROTATE_90
                        }

                        if orientation in rotations:
                            img = img.transpose(rotations[orientation])
            except (AttributeError, KeyError, IndexError):
                # Si no hay EXIF o hay error, continuar sin rotar
                pass

            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            # Guardar como WebP
            img.save(ruta_destino, 'WEBP', quality=calidad, method=6)
            return True
    except Exception as e:
        print(f"Error al convertir {ruta_origen}: {e}")
        return False

# Obtener todas las fotos de ambas carpetas
fotos_sesion = []
fotos_fiesta = []

# Procesar fotos de sesión
if os.path.exists(carpeta_sesion):
    for archivo in sorted(os.listdir(carpeta_sesion)):
        if archivo.lower().endswith(('.jpg', '.jpeg')):
            fotos_sesion.append(os.path.join(carpeta_sesion, archivo))
    print(f"Fotos de sesión encontradas: {len(fotos_sesion)}")
else:
    print(f"Carpeta de sesión no encontrada: {carpeta_sesion}")

# Procesar fotos de fiesta
if os.path.exists(carpeta_fiesta):
    for archivo in sorted(os.listdir(carpeta_fiesta)):
        if archivo.lower().endswith(('.jpg', '.jpeg')):
            fotos_fiesta.append(os.path.join(carpeta_fiesta, archivo))
    print(f"Fotos de fiesta encontradas: {len(fotos_fiesta)}")
else:
    print(f"Carpeta de fiesta no encontrada: {carpeta_fiesta}")

# Combinar todas las fotos (primero sesión, luego fiesta)
todas_las_fotos = fotos_sesion + fotos_fiesta
total_fotos = len(todas_las_fotos)

print(f"\n{'='*60}")
print(f"TOTAL DE FOTOS A PROCESAR: {total_fotos}")
print(f"{'='*60}\n")

# Convertir todas las fotos a WebP con numeración secuencial
contador = 0
errores = 0

for i, ruta_origen in enumerate(todas_las_fotos, 1):
    nombre_destino = f"foto_{i:03d}.webp"
    ruta_destino = os.path.join(carpeta_destino, nombre_destino)

    print(f"[{i}/{total_fotos}] Convirtiendo: {os.path.basename(ruta_origen)} -> {nombre_destino}")

    if convertir_a_webp(ruta_origen, ruta_destino, calidad=85):
        contador += 1
    else:
        errores += 1

print(f"\n{'='*60}")
print(f"CONVERSIÓN COMPLETADA")
print(f"{'='*60}")
print(f"Fotos convertidas exitosamente: {contador}")
print(f"Errores: {errores}")
print(f"Carpeta de destino: {carpeta_destino}")
print(f"{'='*60}\n")

# Actualizar el archivo selector.js con el número correcto de fotos
selector_js_path = r"C:\Users\foro7\xv-anos-megan\js\selector.js"
if os.path.exists(selector_js_path):
    with open(selector_js_path, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Actualizar la línea que genera el array de fotos
    nuevo_contenido = contenido.replace(
        '// Generate photo paths - will be updated with actual count\nconst photos = [];',
        f'// Generate photo paths for {total_fotos} photos\nconst photos = Array.from({{length: {total_fotos}}}, (_, i) => `images/foto_${{String(i + 1).padStart(3, "0")}}.webp`);'
    )

    with open(selector_js_path, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)

    print(f"[OK] Archivo selector.js actualizado con {total_fotos} fotos")
else:
    print(f"[!] No se encontro el archivo selector.js en: {selector_js_path}")

print("\n¡Proceso completado! Ahora puedes abrir selector.html en tu navegador.")
