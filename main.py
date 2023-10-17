#Simulación

#Importaciones
import simpy
import random

# Parámetros de la simulación
M = 1 # Número de cajas
llegada_clientes_por_hora = 30  # Tasa de llegada de clientes por hora
despacho_cajero_por_hora = 5  # Tasa de despacho por cajero por hora

tiempo_simulacion = 24 * 60  # Tiempo de simulación en minutos (8 horas)

def llegada_clientes(env, cajas):
    i = 0
    while True:
        i += 1
        c = Cliente(env, f'Cliente {i}', cajas)  # Crear un nuevo cliente con un nombre único
        env.process(c())  # Iniciar el proceso del cliente
        t = random.expovariate(1 / llegada_clientes_por_hora)  # Calcular el tiempo hasta la próxima llegada
        yield env.timeout(t)  # Esperar el tiempo de llegada

class Cliente:
    def __init__(self, env, nombre, cajas):
        self.env = env
        self.nombre = nombre
        self.cajas = cajas

    def __call__(self):
        with self.cajas.request() as req:  # Solicitar acceso a una caja
            yield req  # Esperar hasta que haya una caja disponible
            tiempo_llegada_cola = self.env.now
            yield self.env.process(self.despacho(req))  # Iniciar el proceso de despacho
            tiempo_salida_cola = self.env.now
            tiempo_en_cola = tiempo_salida_cola - tiempo_llegada_cola  # Calcular el tiempo en cola
            print(f'{self.nombre} fue atendido en {tiempo_en_cola:.2f} minutos.')

    def despacho(self, req):
        tiempo_despacho = random.expovariate(1 / despacho_cajero_por_hora)  # Calcular el tiempo de despacho
        yield self.env.timeout(tiempo_despacho)  # Esperar hasta que se complete el despacho


# Inicializar el entorno de SimPy
env = simpy.Environment()

# Inicializar las cajas
cajas = simpy.Resource(env, capacity=M)

# ...

# Iniciar el proceso de llegada de clientes
env.process(llegada_clientes(env, cajas))

# Simulación
env.run(until=tiempo_simulacion)

# Inicializar la lista para almacenar los tiempos en cola
tiempos_en_cola = []

# Calcular tiempos en cola
def calcular_tiempos_en_cola(env, caja):
    while True:
        for cliente in caja.queue:
            tiempos_en_cola.append(env.now - cliente[0])  # cliente[0] es el momento en que el cliente llegó a la cola
        yield env.timeout(0.5)  # Esperar 1 minuto

env.process(calcular_tiempos_en_cola(env, cajas))

# Resultados
# Resultados
# Verificamos si hay tiempos en cola antes de calcular el tiempo promedio
if tiempos_en_cola:
    tiempo_promedio_cola = sum(tiempos_en_cola) / len(tiempos_en_cola)
    num_clientes_promedio_cola = tiempo_promedio_cola * llegada_clientes_por_hora / 60  # Convertir a clientes por hora
    grado_utilizacion_cajeros = [(cajero.name, cajero.count / tiempo_simulacion) for cajero in cajas.users]

    print(f'\nTiempo promedio de un cliente en la cola: {tiempo_promedio_cola:.2f} minutos')
    print(f'Número de clientes en la cola en promedio: {num_clientes_promedio_cola:.2f}')
    print('\nGrado de utilización de cada cajero:')
    for cajero, utilizacion in grado_utilizacion_cajeros:
        print(f'{cajero}: {utilizacion:.2f}')
else:
    print("\nNingún cliente estuvo en cola durante la simulación.")
    
print("Tiempos en cola recopilados:", tiempos_en_cola)  # Agregar esta línea para depuración

