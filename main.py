from src.viaje import Viaje
from src.gasto import Gasto
from src.persistencia import cargar_viajes, guardar_viajes

TIPOS_GASTO = ['transporte', 'alojamiento', 'alimentación', 'entretenimiento', 'compras']
METODOS = ['efectivo', 'tarjeta']

def seleccionar_viaje(viajes):
    activos = [v for v in viajes if not v.finalizado]
    if not activos:
        print("No hay viajes activos. Debes crear uno nuevo.")
        return None
    print("\nViajes activos:")
    for idx, v in enumerate(activos):
        print(f"{idx+1}. {v}")
    op = int(input("Selecciona un viaje (número): "))
    return activos[op-1]

def crear_viaje():
    print("\n=== Crear nuevo viaje ===")
    internacional = input("¿El viaje es internacional? (s/n): ").strip().lower() == 's'
    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
    presupuesto = float(input("Presupuesto diario en COP: "))
    moneda = input("Moneda del país (por defecto COP): ").upper() if internacional else "COP"
    viaje = Viaje(internacional, fecha_inicio, fecha_fin, presupuesto, moneda)
    print("Viaje creado.")
    return viaje

def registrar_gasto(viaje):
    if viaje.finalizado:
        print("Este viaje ya está finalizado, no se pueden agregar más gastos.")
        return
    fecha = input("Fecha del gasto (YYYY-MM-DD): ")
    if not (viaje.fecha_inicio <= fecha <= viaje.fecha_fin):
        print("Fecha fuera del rango del viaje.")
        return
    valor = float(input(f"Valor gastado en {viaje.moneda}: "))
    metodo = input("Método de pago (efectivo/tarjeta): ").lower()
    if metodo not in METODOS:
        print("Método inválido.")
        return
    print("Tipos de gasto:", ", ".join(TIPOS_GASTO))
    tipo = input("Tipo de gasto: ").lower()
    if tipo not in TIPOS_GASTO:
        print("Tipo de gasto inválido.")
        return
    gasto = Gasto(fecha, valor, metodo, tipo, viaje.moneda)
    viaje.registrar_gasto(gasto)
    print(f"Gasto registrado: {gasto}")
    # Mostrar diferencia con presupuesto diario
    diferencia = viaje.calcular_diferencia_presupuesto(fecha)
    if diferencia > 0:
        print(f"Te quedan {diferencia:.2f} COP para el {fecha}.")
    elif diferencia == 0:
        print(f"¡Exacto! Has gastado justo tu presupuesto del día {fecha}.")
    else:
        print(f"Te pasaste por {abs(diferencia):.2f} COP el {fecha}.")

def finalizar_viaje(viaje):
    viaje.finalizado = True
    print("Viaje finalizado. Ya no podrás registrar más gastos en este viaje.")

def reporte_diario(viaje):
    print("\n--- Reporte Diario ---")
    fechas = sorted(set(g.fecha for g in viaje.gastos))
    if not fechas:
        print("No hay gastos registrados.")
        return
    for fecha in fechas:
        efectivo = sum(g.valor_en_pesos for g in viaje.gastos if g.fecha == fecha and g.metodo_pago == "efectivo")
        tarjeta = sum(g.valor_en_pesos for g in viaje.gastos if g.fecha == fecha and g.metodo_pago == "tarjeta")
        total = efectivo + tarjeta
        print(f"{fecha}: Efectivo: {efectivo:.2f} - Tarjeta: {tarjeta:.2f} - Total: {total:.2f}")

def reporte_tipo(viaje):
    print("\n--- Reporte por Tipo de Gasto ---")
    if not viaje.gastos:
        print("No hay gastos registrados.")
        return
    for tipo in TIPOS_GASTO:
        efectivo = sum(g.valor_en_pesos for g in viaje.gastos if g.tipo == tipo and g.metodo_pago == "efectivo")
        tarjeta = sum(g.valor_en_pesos for g in viaje.gastos if g.tipo == tipo and g.metodo_pago == "tarjeta")
        total = efectivo + tarjeta
        print(f"{tipo.capitalize()}: Efectivo: {efectivo:.2f} - Tarjeta: {tarjeta:.2f} - Total: {total:.2f}")

def menu_viaje(viaje, viajes):
    while True:
        print("\n=== Menú viaje activo ===")
        print("1. Registrar gasto")
        print("2. Ver diferencia con presupuesto diario")
        print("3. Finalizar viaje")
        print("4. Ver reporte diario")
        print("5. Ver reporte por tipo de gasto")
        print("6. Guardar y salir a menú principal")
        opcion = input("Opción: ")

        if opcion == "1":
            registrar_gasto(viaje)
            guardar_viajes(viajes)
        elif opcion == "2":
            fecha = input("Fecha (YYYY-MM-DD): ")
            diferencia = viaje.calcular_diferencia_presupuesto(fecha)
            if diferencia > 0:
                print(f"Te quedan {diferencia:.2f} COP para el {fecha}.")
            elif diferencia == 0:
                print(f"¡Exacto! Has gastado justo tu presupuesto del día {fecha}.")
            else:
                print(f"Te pasaste por {abs(diferencia):.2f} COP el {fecha}.")
        elif opcion == "3":
            finalizar_viaje(viaje)
            guardar_viajes(viajes)
        elif opcion == "4":
            reporte_diario(viaje)
        elif opcion == "5":
            reporte_tipo(viaje)
        elif opcion == "6":
            guardar_viajes(viajes)
            print("Datos guardados.")
            break
        else:
            print("Opción no válida.")

def main():
    viajes = cargar_viajes()
    while True:
        print("\n=== Registro de Gastos de Viaje ===")
        print("1. Crear nuevo viaje")
        print("2. Seleccionar viaje activo")
        print("3. Salir")
        op = input("Opción: ")
        if op == "1":
            viaje = crear_viaje()
            viajes.append(viaje)
            guardar_viajes(viajes)
            menu_viaje(viaje, viajes)
        elif op == "2":
            viaje = seleccionar_viaje(viajes)
            if viaje:
                menu_viaje(viaje, viajes)
        elif op == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()