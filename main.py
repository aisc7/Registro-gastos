from src.viaje import Viaje
from src.gasto import Gasto

def main():
    print("¿El viaje es internacional? (s/n): ")
    internacional = input().strip().lower() == 's'

    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
    fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
    presupuesto = int(input("Presupuesto diario en COP: "))
    moneda = input("Moneda del país (por defecto COP): ") if internacional else "COP"

    viaje = Viaje(internacional, fecha_inicio, fecha_fin, presupuesto, moneda)

    while True:
        print("\n1. Registrar gasto\n2. Ver diferencia\n3. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            fecha = input("Fecha del gasto: ")
            valor = float(input("Valor: "))
            metodo = input("Método de pago (efectivo/tarjeta): ")
            tipo = input("Tipo (transporte, alojamiento, alimentación, etc.): ")
            gasto = Gasto(fecha, valor, metodo, tipo, moneda)
            viaje.registrar_gasto(gasto)
            print(f"Gasto registrado: {gasto}")

        elif opcion == "2":
            fecha = input("Fecha para verificar diferencia: ")
            dif = viaje.calcular_diferencia_presupuesto(fecha)
            print(f"Diferencia con el presupuesto del {fecha}: {dif} COP")

        elif opcion == "3":
            print("Fin del programa.")
            break

if __name__ == "__main__":
    main()
