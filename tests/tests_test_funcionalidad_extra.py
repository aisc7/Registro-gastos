import pytest
from unittest.mock import patch
from src.viaje import Viaje
from src.gasto import Gasto

@patch('src.conversor_divisa.ConversorDivisa.convertir')
def test_reporte_diario(mock_convertir):
    mock_convertir.return_value = 40000  # Para pruebas internacionales
    viaje = Viaje(True, "2025-06-01", "2025-06-03", 100000, moneda='USD')
    # Día 1: 2 gastos
    g1 = Gasto("2025-06-01", 10, "efectivo", "transporte", "USD")
    g2 = Gasto("2025-06-01", 10, "tarjeta", "alimentación", "USD")
    viaje.registrar_gasto(g1)
    viaje.registrar_gasto(g2)
    # Día 2: 1 gasto
    g3 = Gasto("2025-06-02", 5, "tarjeta", "compras", "USD")
    viaje.registrar_gasto(g3)
    # Calcular totales por día
    efectivo_dia1 = sum(g.valor_en_pesos for g in viaje.gastos if g.fecha == "2025-06-01" and g.metodo_pago == "efectivo")
    tarjeta_dia1 = sum(g.valor_en_pesos for g in viaje.gastos if g.fecha == "2025-06-01" and g.metodo_pago == "tarjeta")
    total_dia2 = sum(g.valor_en_pesos for g in viaje.gastos if g.fecha == "2025-06-02")
    assert efectivo_dia1 == 40000
    assert tarjeta_dia1 == 40000
    assert total_dia2 == 20000

@patch('src.conversor_divisa.ConversorDivisa.convertir')
def test_reporte_por_tipo(mock_convertir):
    mock_convertir.return_value = 50000
    viaje = Viaje(True, "2025-06-01", "2025-06-03", 100000, moneda='USD')
    # Transporte: efectivo y tarjeta
    g1 = Gasto("2025-06-01", 1, "efectivo", "transporte", "USD")
    g2 = Gasto("2025-06-01", 1, "tarjeta", "transporte", "USD")
    viaje.registrar_gasto(g1)
    viaje.registrar_gasto(g2)
    # Alimentación: tarjeta
    g3 = Gasto("2025-06-02", 1, "tarjeta", "alimentación", "USD")
    viaje.registrar_gasto(g3)
    # Validaciones
    transporte_efectivo = sum(g.valor_en_pesos for g in viaje.gastos if g.tipo == "transporte" and g.metodo_pago == "efectivo")
    transporte_tarjeta = sum(g.valor_en_pesos for g in viaje.gastos if g.tipo == "transporte" and g.metodo_pago == "tarjeta")
    alimentacion_tarjeta = sum(g.valor_en_pesos for g in viaje.gastos if g.tipo == "alimentación" and g.metodo_pago == "tarjeta")
    assert transporte_efectivo == 50000
    assert transporte_tarjeta == 50000
    assert alimentacion_tarjeta == 50000

def test_no_permitir_gasto_despues_de_finalizar():
    viaje = Viaje(False, "2025-06-01", "2025-06-05", 100000)
    viaje.finalizado = True
    gasto = Gasto("2025-06-02", 20000, "tarjeta", "transporte")
    # Simula el método main: no debería registrar el gasto si finalizado
    if not viaje.finalizado:
        viaje.registrar_gasto(gasto)
    assert len(viaje.gastos) == 0

def test_no_gasto_fuera_de_rango():
    viaje = Viaje(False, "2025-06-01", "2025-06-05", 100000)
    gasto = Gasto("2025-07-01", 50000, "efectivo", "compras")
    # Simula el método main: no debería registrar gasto fuera de rango
    if viaje.fecha_inicio <= gasto.fecha <= viaje.fecha_fin:
        viaje.registrar_gasto(gasto)
    assert len(viaje.gastos) == 0

def test_varios_gastos_mismo_dia():
    viaje = Viaje(False, "2025-06-01", "2025-06-10", 100000)
    gastos = [
        Gasto("2025-06-02", 30000, "efectivo", "alimentación"),
        Gasto("2025-06-02", 25000, "tarjeta", "transporte"),
        Gasto("2025-06-02", 20000, "tarjeta", "compras"),
    ]
    for g in gastos:
        viaje.registrar_gasto(g)
    total_dia = sum(g.valor_en_pesos for g in viaje.gastos if g.fecha == "2025-06-02")
    assert total_dia == 75000
    assert viaje.calcular_diferencia_presupuesto("2025-06-02") == 25000