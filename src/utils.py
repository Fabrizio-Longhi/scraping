# Funciones auxiliares, como conversion e fecha y manejo de errores
from datetime import datetime
import locale

class DataConverter():

    @staticmethod
    def convert_to_iso8601(data_text: str) -> str:
        """Convierte una fecha en formato texto a ISO 8601"""
        try:
            parsed_data = datetime.strptime(data_text, "%d de %B de %Y - %H:%M")
            return parsed_data.isoformat()
        except ValueError as e:
            print(f"Error al parsear fecha: {e}")
        return data_text
    
    @staticmethod
    def set_spanish_locales():
        """Establece el locale en español"""
        try:
            locale.setlocale(locale.LC_TIME, "es_ES.utf8")  # Linux/macOS 
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, "es_ES")  # Windows
            except locale.Error:
                print("No se pudo establecer el locale en español, el parser de fechas podría fallar.")