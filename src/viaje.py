from src.conversor_divisa import ConversorDivisa
from src.gasto import Gasto

class Viaje:
    def __init__(self, es_internacional, fecha_inicio, fecha_fin, presupuesto_diario, moneda='COP', finalizado=False):
        self.es_internacional = es_internacional
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.moneda = moneda
        self.gastos = []
        self.finalizado = finalizado

    def registrar_gasto(self, gasto):
        if self.es_internacional:
            gasto.valor_en_pesos = ConversorDivisa.convertir(gasto.valor_original, gasto.moneda, 'COP')
        else:
            gasto.valor_en_pesos = gasto.valor_original
        self.gastos.append(gasto)

    def calcular_diferencia_presupuesto(self, fecha):
        total = sum(g.valor_en_pesos for g in self.gastos if g.fecha == fecha)
        return self.presupuesto_diario - total

    def to_dict(self):
        return {
            "es_internacional": self.es_internacional,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "presupuesto_diario": self.presupuesto_diario,
            "moneda": self.moneda,
            "finalizado": self.finalizado,
            "gastos": [g.to_dict() for g in self.gastos]
        }

    @classmethod
    def from_dict(cls, data):
        v = cls(
            data["es_internacional"],
            data["fecha_inicio"],
            data["fecha_fin"],
            data["presupuesto_diario"],
            data.get("moneda", "COP"),
            data.get("finalizado", False)
        )
        v.gastos = [Gasto.from_dict(g) for g in data.get("gastos", [])]
        return v

    def __repr__(self):
        return f"<Viaje del {self.fecha_inicio} al {self.fecha_fin} - Gastos: {len(self.gastos)}>"