import requests

class ConversorDivisa:
    @staticmethod
    def convertir(valor, moneda_origen, moneda_destino='COP'):
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
