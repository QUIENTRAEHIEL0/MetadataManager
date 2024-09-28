# Metadata Manager

Este script en Python permite gestionar los metadatos de archivos, incluyendo la visualización y modificación de metadatos como fechas de creación, modificación, último acceso y nombre del archivo. Además, puede extraer y mostrar los metadatos EXIF de imágenes JPEG, incluyendo la geolocalización y los datos del móvil con el que se tomó la foto.

## Funcionalidades

- **Obtener la ruta del archivo**: Permite seleccionar un archivo desde una ventana de diálogo (en Windows) o ingresando la ruta absoluta (en otros sistemas operativos).
- **Mostrar metadatos del archivo**: Muestra los metadatos del archivo seleccionado.
- **Modificar metadatos del archivo**: Permite modificar la fecha de creación, modificación, último acceso y el nombre del archivo.
- **Mostrar metadatos EXIF de imágenes JPEG**: Extrae y muestra los metadatos EXIF de imágenes JPEG, incluyendo la geolocalización y los datos del móvil.

## Requisitos

Para ejecutar este script, necesitas tener instaladas las siguientes bibliotecas de Python:

- `Pillow`
- `exifread`

Puedes instalarlas usando `pip`:

```sh
pip install Pillow exifread
```

Clona este repositorio o descarga el script con

```sh
git clone https://github.com/QUIENTRAEHIEL0/MetadataManager.git
```

