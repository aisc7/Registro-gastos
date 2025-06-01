import json
import os
from src.viaje import Viaje

ARCHIVO_JSON = "viajes.json"

def guardar_viajes(viajes):
    """Recibe una lista de objetos Viaje y los guarda en JSON."""
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump([v.to_dict() for v in viajes], f, indent=2, ensure_ascii=False)

def cargar_viajes():
    """Devuelve una lista de objetos Viaje desde el archivo JSON, o lista vacía si no existe."""
    if not os.path.exists(ARCHIVO_JSON):
        return []
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        datos = json.load(f)
        return [Viaje.from_dict(v) for v in datos]