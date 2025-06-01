from src.conversor_divisa import ConversorDivisa

class Viaje:
    def __init__(self, es_internacional, fecha_inicio, fecha_fin, presupuesto_diario, moneda='COP'):
        self.es_internacional = es_internacional
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.moneda = moneda
        self.gastos = []

    def registrar_gasto(self, gasto):
        if self.es_internacional:
            gasto.valor_en_pesos = ConversorDivisa.convertir(gasto.valor_original, gasto.moneda, 'COP')
        else:
            gasto.valor_en_pesos = gasto.valor_original
        self.gastos.append(gasto)

    def calcular_diferencia_presupuesto(self, fecha):
        total = sum(g.valor_en_pesos for g in self.gastos if g.fecha == fecha)
        return self.presupuesto_diario - total

    def __repr__(self):
        return f"<Viaje del {self.fecha_inicio} al {self.fecha_fin} - Gastos: {len(self.gastos)}>"
