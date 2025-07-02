import os

BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "Assets")
AUDIO_PATH = os.path.join(ASSETS_PATH, "audio")
IMG_PATH = os.path.join(ASSETS_PATH, "Imagenes")

def get_audio_path(nombre_archivo):
    return os.path.join(AUDIO_PATH, nombre_archivo)

def get_image_path(nombre_archivo):
    return os.path.join(IMG_PATH, nombre_archivo)

def get_cursor_path(nombre_archivo):  # usa la carpeta de imágenes
    return os.path.join(IMG_PATH, nombre_archivo)
