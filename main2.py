import simpy
import random

# Definición de la clase Supermercado
class Supermercado:
    def __init__(self, env, num_cajeros, tasa_llegada_clientes, tiempo_promedio_despacho):
        self.env = env
        self.cajeros = [simpy.Resource(env) for _ in range(num_cajeros)]
        self.tasa_llegada_clientes = tasa_llegada_clientes
        self.tiempo_promedio_despacho = tiempo_promedio_despacho
        self.clientes_en_cola = 0
        self.tiempo_total_en_cola = 0

    def llegada_cliente(self):
        llegada = self.env.now
        caja_elegida = self.seleccionar_caja()
        with caja_elegida.request() as req:
            yield req
            tiempo_en_cola = self.env.now - llegada
            self.clientes_en_cola += 1
            yield self.env.timeout(random.expovariate(1.0 / self.tiempo_promedio_despacho))
            self.clientes_en_cola -= 1
            self.tiempo_total_en_cola += tiempo_en_cola

    def seleccionar_caja(self):
        # Selecciona la caja con la menor cola
        cajas_disponibles = [(cajero, len(cajero.queue)) for cajero in self.cajeros]
        cajas_ordenadas = sorted(cajas_disponibles, key=lambda x: x[1])
        return cajas_ordenadas[0][0]

    def run(self, tiempo_simulacion):
        for _ in range(tiempo_simulacion):
            if random.random() < self.tasa_llegada_clientes:
                self.env.process(self.llegada_cliente())
            yield self.env.timeout(1)

def main():
    tiempo_simulacion = 1000  # Tiempo de simulación en minutos
    num_cajeros = 3
    tasa_llegada_clientes = 10 / 60  # Tasa de llegada de clientes por minuto
    tiempo_promedio_despacho = 5  # en minutos

    env = simpy.Environment()
    supermercado = Supermercado(env, num_cajeros, tasa_llegada_clientes, tiempo_promedio_despacho)

    env.process(supermercado.run(tiempo_simulacion))
    env.run(until=tiempo_simulacion)

    tiempo_promedio_en_cola = supermercado.tiempo_total_en_cola / (supermercado.clientes_en_cola if supermercado.clientes_en_cola > 0 else 1)
    clientes_promedio_en_cola = supermercado.clientes_en_cola / tiempo_simulacion
    utilizacion_cajeros = [1 - c.count / num_cajeros for c in supermercado.cajeros]

    print("1. El tiempo promedio de un cliente en la cola:", tiempo_promedio_en_cola)
    print("2. Número de clientes en la cola en promedio:", clientes_promedio_en_cola)
    print("3. Grado de utilización de cada cajero:")
    for i, uso in enumerate(utilizacion_cajeros, 1):
        print(f"   Cajero {i}: {uso:.2f}")

if __name__ == '__main__':
    main()
