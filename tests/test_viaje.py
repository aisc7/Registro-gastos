import pytest
from unittest.mock import patch
from src.viaje import Viaje
from src.gasto import Gasto

@patch('src.conversor_divisa.ConversorDivisa.convertir')
def test_registrar_gasto_internacional(mock_convertir):
    mock_convertir.return_value = 200000
    viaje = Viaje(True, "2025-06-01", "2025-06-10", 100000, moneda='USD')
    gasto = Gasto("2025-06-02", 50, "tarjeta", "alimentación", moneda='USD')
    viaje.registrar_gasto(gasto)
    assert len(viaje.gastos) == 1
    assert gasto.valor_en_pesos == 200000

def test_registrar_gasto_nacional():
    viaje = Viaje(False, "2025-06-01", "2025-06-10", 100000)
    gasto = Gasto("2025-06-02", 80000, "efectivo", "transporte")
    viaje.registrar_gasto(gasto)
    assert len(viaje.gastos) == 1
    assert gasto.valor_en_pesos == 80000

def test_diferencia_positiva():
    viaje = Viaje(False, "2025-06-01", "2025-06-10", 100000)
    gasto = Gasto("2025-06-02", 70000, "tarjeta", "entretenimiento")
    viaje.registrar_gasto(gasto)
    assert viaje.calcular_diferencia_presupuesto("2025-06-02") == 30000

def test_diferencia_negativa():
    viaje = Viaje(False, "2025-06-01", "2025-06-10", 100000)
    gasto = Gasto("2025-06-02", 120000, "efectivo", "compras")
    viaje.registrar_gasto(gasto)
    assert viaje.calcular_diferencia_presupuesto("2025-06-02") == -20000

def test_diferencia_cero():
    viaje = Viaje(False, "2025-06-01", "2025-06-10", 100000)
    gasto = Gasto("2025-06-02", 100000, "tarjeta", "alojamiento")
    viaje.registrar_gasto(gasto)
    assert viaje.calcular_diferencia_presupuesto("2025-06-02") == 0
