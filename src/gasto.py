class Gasto:
    def __init__(self, fecha, valor_original, metodo_pago, tipo, moneda='COP'):
        self.fecha = fecha
        self.valor_original = valor_original
        self.metodo_pago = metodo_pago  # 'efectivo' o 'tarjeta'
        self.tipo = tipo  # 'transporte', 'alimentación', etc.
        self.moneda = moneda
        self.valor_en_pesos = None

    def __repr__(self):
        return (f"<Gasto fecha={self.fecha}, tipo={self.tipo}, "
                f"valor={self.valor_en_pesos} COP, pago={self.metodo_pago}>")
