import os
import platform
import tkinter as tk
from tkinter import filedialog
import subprocess
import time
import exifread # type: ignore
from PIL import Image # type: ignore
from PIL.ExifTags import TAGS, GPSTAGS # type: ignore

# pip install Pillow exifread
# pip install exifread Pillow

# Función para obtener la ruta del archivo
def get_file_path():
    if platform.system() == "Windows":
        root = tk.Tk()  # Crea una ventana principal
        root.withdraw()  # Oculta la ventana principal
        file_path = filedialog.askopenfilename(title="Selecciona un archivo")  # Declara la variable file_path y le asigna el archivo seleccionado
    else:
        file_path = input("Introduce la ruta absoluta del archivo: ")
    return file_path

# Función para mostrar los metadatos del archivo
def show_metadata(file_path):
    print(f"Metadatos del archivo: {file_path}")
    if platform.system() == "Windows":
        # Obtener propiedades extendidas del archivo en Windows usando PowerShell
        subprocess.run(["powershell", "-Command", f"Get-ItemProperty -Path '{file_path}' | Format-List"])
    else:
        subprocess.run(["stat", file_path])

# Función para validar el nombre del archivo
def is_valid_name(name):
    return not any(char in name for char in r'\/:*?"<>|')

# Función para modificar los metadatos del archivo en Windows
def modify_metadata(file_path):
    if platform.system() == "Windows":
        while True:
            print("\n¿Qué metadato deseas modificar?")
            print("1. Fecha de creación")
            print("2. Fecha de modificación")
            print("3. Fecha de último acceso")
            print("4. Nombre del archivo (recuerda incluir la extensión)")
            print("5. Ver datos modificados")
            print("6. Salir")
            choice = input("Selecciona una opción (1-6): ").strip()

            try:
                if choice == '1':
                    new_time = input("Introduce la nueva fecha de creación (YYYY-MM-DD HH:MM:SS): ")
                    if is_valid_date(new_time):
                        modify_time(file_path, new_time, 'CreationTime')
                    else:
                        print("Formato de fecha no válido. Inténtalo de nuevo.")
                elif choice == '2':
                    new_time = input("Introduce la nueva fecha de modificación (YYYY-MM-DD HH:MM:SS): ")
                    if is_valid_date(new_time):
                        modify_time(file_path, new_time, 'LastWriteTime')
                    else:
                        print("Formato de fecha no válido. Inténtalo de nuevo.")
                elif choice == '3':
                    new_time = input("Introduce la nueva fecha de último acceso (YYYY-MM-DD HH:MM:SS): ")
                    if is_valid_date(new_time):
                        modify_time(file_path, new_time, 'LastAccessTime')
                    else:
                        print("Formato de fecha no válido. Inténtalo de nuevo.")
                elif choice == '4':
                    new_name = input("Introduce el nuevo nombre del archivo: ")
                    if is_valid_name(new_name):
                        modify_name(file_path, new_name)
                        file_path = os.path.join(os.path.dirname(file_path), new_name)  # Actualiza la ruta del archivo
                    else:
                        print("Nombre de archivo no válido. Inténtalo de nuevo.")
                elif choice == '5':
                    show_metadata(file_path)
                elif choice == '6':
                    print("Recuerda modificar la fecha de ultimo adceso en el archivo para que se actualice la fecha de modificación")
                    exitShow = input("¿Estas seguro que deseas salir? (s/n): ").lower()
                    if exitShow == 's':
                        print("Saliendo del programa ...")
                        time.sleep(1)
                        break
                else:
                    print("Opción no válida. Inténtalo de nuevo.")
            except Exception as e:
                print(f"Se produjo un error: {e}")
                
# Función para modificar los metadatos del archivo en Linux                
    else:
        while True:
            print("\n¿Qué metadato deseas modificar?")
            print("1. Fecha de modificación")
            print("2. Fecha de último acceso")
            print("3. Nombre del archivo (recuerda incluir la extensión)")
            print("4. Ver datos modificados")
            print("5. Salir")
            choice = input("Selecciona una opción (1-5): \n").strip()

            try:
                if choice == '1':
                    new_time = input("Introduce la nueva fecha de modificación (YYYY-MM-DD HH:MM:SS): ")
                    if is_valid_date(new_time):
                        modify_time_linux(file_path, new_time, 'modification')
                    else:
                        print("Formato de fecha no válido. Inténtalo de nuevo.")
                elif choice == '2':
                    new_time = input("Introduce la nueva fecha de último acceso (YYYY-MM-DD HH:MM:SS): ")
                    if is_valid_date(new_time):
                        modify_time_linux(file_path, new_time, 'access')
                    else:
                        print("Formato de fecha no válido. Inténtalo de nuevo.")
                elif choice == '3':
                    new_name = input("Introduce el nuevo nombre del archivo: ")
                    if is_valid_name(new_name):
                        modify_name(file_path, new_name)
                        file_path = os.path.join(os.path.dirname(file_path), new_name)  # Actualiza la ruta del archivo
                    else:
                        print("Nombre de archivo no válido. Inténtalo de nuevo.")
                elif choice == '4':
                    show_metadata(file_path)
                elif choice == '5':
                    print("Recuerda modificar la fecha de ultimo adceso en el archivo para que se actualice la fecha de modificación")
                    exitShow = input("¿Estas seguro que deseas salir? (s/n): ")
                    if exitShow == 's':
                        print("Saliendo del programa ...").lower()
                        time.sleep(1)
                        break
                else:
                    print("Opción no válida. Inténtalo de nuevo.")
            except Exception as e:
                print(f"Se produjo un error: {e}")

# Función para validar el formato de la fecha
def is_valid_date(date_str):
    try:
        time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

# Función para modificar una fecha específica del archivo en Linux
def modify_time_linux(file_path, new_time, time_type):
    if not is_valid_date(new_time):
        print("Formato de fecha no válido. Inténtalo de nuevo.")
        return

    new_time_struct = time.strptime(new_time, "%Y-%m-%d %H:%M:%S")
    new_time_epoch = int(time.mktime(new_time_struct))
    formatted_time = time.strftime("%Y%m%d%H%M.%S", new_time_struct)

    if time_type == 'modification':
        subprocess.run(["touch", "-m", "-t", formatted_time, file_path])
    elif time_type == 'access':
        subprocess.run(["touch", "-a", "-t", formatted_time, file_path])
    else:
        print(f"Tipo de tiempo '{time_type}' no reconocido.")
        return

    print(f"Fecha de {time_type} modificada.")

# Función para modificar una fecha específica del archivo en Windows
def modify_time(file_path, new_time, time_type):
    new_time_struct = time.strptime(new_time, "%Y-%m-%d %H:%M:%S")
    new_time_epoch = time.mktime(new_time_struct)
    new_time_windows = int(new_time_epoch * 10000000) + 116444736000000000
    subprocess.run(["powershell", "-Command", f"(Get-Item '{file_path}').{time_type} = [datetime]::FromFileTime({new_time_windows})"])
    print(f"{time_type} modificada.")

# Función para modificar el nombre del archivo en Windows
def modify_name(file_path, new_name):
    directory = os.path.dirname(file_path)
    new_path = os.path.join(directory, new_name)
    os.rename(file_path, new_path)
    print(f"Nombre del archivo modificado a: {new_name}")

# Función para obtener los datos EXIF de una imagen
def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if not exif_data:
        return None

    exif = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        exif[decoded] = value

    return exif

# Función para obtener la información GPS de los datos EXIF
def get_gps_info(exif_data):
    gps_info = {}
    for key in exif_data['GPSInfo'].keys():
        decode = GPSTAGS.get(key, key)
        gps_info[decode] = exif_data['GPSInfo'][key]

    return gps_info

# Función para convertir las coordenadas GPS a grados decimales
def get_geolocation(gps_info):
    def convert_to_degrees(value):
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)

    lat = convert_to_degrees(gps_info['GPSLatitude'])
    if gps_info['GPSLatitudeRef'] != 'N':
        lat = -lat

    lon = convert_to_degrees(gps_info['GPSLongitude'])
    if gps_info['GPSLongitudeRef'] != 'E':
        lon = -lon

    return lat, lon

# Función para mostrar los metadatos de la imagen, incluyendo la geolocalización
def show_image_metadata(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)

    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print(f"{tag}: {tags[tag]}")

    exif_data = get_exif_data(image_path)
    if exif_data and 'GPSInfo' in exif_data:
        gps_info = get_gps_info(exif_data)
        lat, lon = get_geolocation(gps_info)
        print(f"Geolocation: Latitude = {lat}, Longitude = {lon}")
    else:
        print("No GPS data found.")

# Nueva función para mostrar los metadatos de GPS y datos del móvil
def show_gps_and_mobile_data(file_path):
    if file_path.lower().endswith(('.jpg', '.jpeg')):
        print("Mostrando metadatos de GPS y datos del móvil ...")
        show_image_metadata(file_path)
    else:
        print("El archivo seleccionado no es una imagen JPEG.")

# Función principal
def main():
    file_path = get_file_path()
    if not file_path:
        print("No se seleccionó ningún archivo.")
        return

    print(f"Archivo seleccionado: {file_path}")
    print("Mostrando metadatos del archivo  ...")
    print()  # Salto de línea
    show_metadata(file_path)

    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Mostrar metadatos avanzados (GPS y datos del móvil)")
        print("2. Modificar metadatos")
        print("3. Salir")
        choice = input("Selecciona una opción (1-3): ").strip()

        if choice == '1':
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                print("Mostrando metadatos de la imagen ...\n")
                show_image_metadata(file_path)
            else:
                print("El archivo seleccionado no es una imagen JPEG.")
        elif choice == '2':
            modify_metadata(file_path)
        elif choice == '3':
            print("Saliendo del programa ...")
            time.sleep(1)
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Punto de entrada del script
if __name__ == "__main__":
    main()
