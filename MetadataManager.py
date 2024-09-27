import os
import platform
import tkinter as tk
from tkinter import filedialog
import subprocess
import time

# Función para obtener la ruta del archivo
def get_file_path():
    if platform.system() == "Windows":
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Selecciona un archivo")
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

# Función para modificar los metadatos del archivo en Windows
def modify_metadata(file_path):
    if platform.system() == "Windows":
        while True:
            print("\n¿Qué metadato deseas modificar?")
            print("1. Fecha de creación")
            print("2. Fecha de modificación")
            print("3. Fecha de último acceso")
            print("4. Nombre del archivo (recuerda incluir la extensión)")
            print("5. Salir")
            choice = input("Selecciona una opción (1-5): ").strip()
        
            if choice == '1':
                new_time = input("Introduce la nueva fecha de creación (YYYY-MM-DD HH:MM:SS): ")
                modify_time(file_path, new_time, 'CreationTime')
            elif choice == '2':
                new_time = input("Introduce la nueva fecha de modificación (YYYY-MM-DD HH:MM:SS): ")
                modify_time(file_path, new_time, 'LastWriteTime')
            elif choice == '3':
                new_time = input("Introduce la nueva fecha de último acceso (YYYY-MM-DD HH:MM:SS): ")
                modify_time(file_path, new_time, 'LastAccessTime')
            elif choice == '4':
                new_name = input("Introduce el nuevo nombre del archivo: ")
                modify_name(file_path, new_name)
                file_path = os.path.join(os.path.dirname(file_path), new_name)  # Actualiza la ruta del archivo
            elif choice == '5':
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
    else:
        print("Modificación de metadatos no implementada para Linux en este script.")

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

# Función principal
def main():
    file_path = get_file_path()
    if not file_path:
        print("No se seleccionó ningún archivo.")
        return
    
    print(f"Archivo seleccionado: {file_path}")
    print("Mostrando metadatos del archivo  ...")
    print() # Salto de línea
    show_metadata(file_path)

    modify = input("¿Deseas modificar algún metadato? (s/n): ").strip().lower()
    if modify == 's':
        print("Mostrando metadatos actualizados ...")
        modify_metadata(file_path)
        show_metadata(file_path)

# Punto de entrada del script
if __name__ == "__main__":
    main()
