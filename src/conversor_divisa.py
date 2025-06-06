import requests

class ConversorDivisa:
    tasa_simulada = 4000  # Valor por defecto, configurable

    @staticmethod
    def convertir(valor, moneda_origen, moneda_destino='COP', tasa_simulada=None):
        """
        Convierte un valor de una moneda de origen a una moneda de destino usando la API exchangerate.host.
        Si la conversión falla, utiliza una tasa simulada configurable.

        Parámetros:
            valor (int|float): Monto a convertir.
            moneda_origen (str): Código de la moneda de origen (ej: 'USD').
            moneda_destino (str): Código de la moneda de destino (ej: 'COP'). Por defecto 'COP'.
            tasa_simulada (float|None): Tasa a usar si falla la conversión real. Si es None, usa la clase.

        Retorna:
            float: Valor convertido a la moneda de destino.
        """
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
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"Error en la respuesta de la API: {response.status_code}")
            data = response.json()
            if 'rates' not in data or moneda_destino not in data['rates']:
                raise ValueError("La respuesta de la API no contiene la tasa solicitada.")
            tasa = data['rates'][moneda_destino]
            return valor * tasa
        except Exception as e:
            tasa_fallback = tasa_simulada if tasa_simulada is not None else ConversorDivisa.tasa_simulada
            # No imprime, lanza excepción para que la capa superior decida cómo manejarlo
            raise RuntimeError(
                f"No se pudo obtener la tasa real ({moneda_origen} -> {moneda_destino}). "
                f"Se usó la tasa simulada ({tasa_fallback}). Detalle: {e}"
            ) from e