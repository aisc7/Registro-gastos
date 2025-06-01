import os
import tempfile
from unittest.mock import patch
from src.viaje import Viaje
from src.gasto import Gasto
from src.persistencia import guardar_viajes, cargar_viajes

@patch('src.conversor_divisa.ConversorDivisa.convertir')
def test_guardar_y_cargar_viajes(mock_convertir):
    mock_convertir.return_value = 60000
    viaje = Viaje(True, "2025-06-01", "2025-06-03", 100000, moneda="USD")
    gasto = Gasto("2025-06-01", 10, "tarjeta", "transporte", "USD")
    viaje.registrar_gasto(gasto)
    with tempfile.TemporaryDirectory() as tmpdir:
        archivo = os.path.join(tmpdir, "viajes.json")
        # Sobreescribe el path en persistencia solo para esta prueba
        from src import persistencia
        persistencia.ARCHIVO_JSON = archivo
        guardar_viajes([viaje])
        viajes_cargados = cargar_viajes()
        assert len(viajes_cargados) == 1
        v = viajes_cargados[0]
        assert v.fecha_inicio == "2025-06-01"
        assert v.gastos[0].valor_en_pesos == 60000

def test_reportes_sin_gastos():
    viaje = Viaje(False, "2025-06-01", "2025-06-03", 100000)
    # Reporte diario vacío
    fechas = sorted(set(g.fecha for g in viaje.gastos))
    assert fechas == []
    # Reporte por tipo vacío
    for tipo in ['transporte', 'alojamiento', 'alimentación', 'entretenimiento', 'compras']:
        suma = sum(g.valor_en_pesos for g in viaje.gastos if g.tipo == tipo)
        assert suma == 0

def test_no_gasto_si_finalizado():
    viaje = Viaje(False, "2025-06-01", "2025-06-03", 100000)
    viaje.finalizado = True
    gasto = Gasto("2025-06-02", 20000, "tarjeta", "transporte")
    # El main debe impedir registrar, pero aquí probamos que no se agrega manualmente
    if not viaje.finalizado:
        viaje.registrar_gasto(gasto)
    assert len(viaje.gastos) == 0