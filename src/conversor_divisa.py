import requests

class ConversorDivisa:
    @staticmethod
    def convertir(valor, moneda_origen, moneda_destino='COP'):
        # Validación de parámetros de entrada
        if not isinstance(valor, (int, float)):
            raise ValueError("El valor a convertir debe ser un número (int o float).")
        if not isinstance(moneda_origen, str) or not moneda_origen:
            raise ValueError("La moneda de origen debe ser una cadena no vacía.")
        if not isinstance(moneda_destino, str) or not moneda_destino:
            raise ValueError("La moneda de destino debe ser una cadena no vacía.")

        if moneda_origen == moneda_destino:
            return valor
        try:
            url = f"https://api.exchangerate.host/latest?base={moneda_origen}&symbols={moneda_destino}"
            response = requests.get(url)
            tasa = response.json()['rates'][moneda_destino]
            return valor * tasa
        except Exception as e:
            print(f"Error al convertir moneda. Usando tasa simulada. Detalle: {e}")
            return valor * 4000  # tasa simulada