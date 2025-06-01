class Gasto:
    def __init__(self, fecha, valor_original, metodo_pago, tipo, moneda='COP'):
        self.fecha = fecha
        self.valor_original = valor_original
        self.metodo_pago = metodo_pago  # 'efectivo' o 'tarjeta'
        self.tipo = tipo  # 'transporte', 'alimentación', etc.
        self.moneda = moneda
        self.valor_en_pesos = None

    def to_dict(self):
        return {
            "fecha": self.fecha,
            "valor_original": self.valor_original,
            "metodo_pago": self.metodo_pago,
            "tipo": self.tipo,
            "moneda": self.moneda,
            "valor_en_pesos": self.valor_en_pesos
        }

    @classmethod
    def from_dict(cls, data):
        g = cls(
            data["fecha"],
            data["valor_original"],
            data["metodo_pago"],
            data["tipo"],
            data.get("moneda", "COP")
        )
        g.valor_en_pesos = data.get("valor_en_pesos")
        return g

    def __repr__(self):
        return (f"<Gasto fecha={self.fecha}, tipo={self.tipo}, "
                f"valor={self.valor_en_pesos} COP, pago={self.metodo_pago}>")