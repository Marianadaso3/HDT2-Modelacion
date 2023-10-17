import simpy  # Importa la librería SimPy para simulación de eventos discretos
import random  # Importa la librería random para generación de números aleatorios

M = 6  # Número de cajas disponibles en la tienda
LAMBDA = 50  # Tasa de llegada de clientes por hora
LAMBDA2 = 7  # Capacidad de atención en caja por hora
HORAS = 8  # Número de horas de trabajo para la simulación

log = []  # Lista para registrar información sobre la simulación
tiempo_promedio_espera = 0  # Inicialización de tiempo promedio de espera en cola
clientes_atendidos = 0  # Contador de clientes atendidos
clientes_en_cola_promedio = 0  # Variable para el número promedio de clientes en la cola
tiempos_servicio = [0 for _ in range(M)]  # Inicializar lista de tiempos de servicio por caja
num_cajero = 0  # Variable para llevar un seguimiento del número de cajero

def cliente(env, name, cashier):
    global tiempo_promedio_espera, clientes_atendidos, clientes_en_cola_promedio, log, num_cajero
    llegada = env.now
    print(f"{name} llega a la tienda en {llegada:.2f} minutos")
    
    with cashier.request() as req:  # Solicitar una caja (recurso)
        yield req  # Esperar hasta que se obtenga acceso a una caja
        espera = env.now - llegada  # Calcular el tiempo de espera en la cola
        tiempo_promedio_espera += espera  # Acumular el tiempo de espera
        clientes_atendidos += 1  # Aumentar el contador de clientes atendidos

        #print(f"{name} espera {espera:.2f} minutos")
        tiempo_servicio = random.expovariate(LAMBDA2 / 60)  # Generar el tiempo de servicio
        tiempos_servicio[num_cajero] += tiempo_servicio  # Acumular el tiempo de servicio real por caja
        yield env.timeout(tiempo_servicio)  # Simular el tiempo de servicio

        log.append(f"{name:<13} | {llegada:.2f} | {espera:.2f} | {env.now:.2f}")  # Registrar información del cliente
        num_cajero = (num_cajero + 1) % M  # Cambiar al siguiente cajero (asegurando que esté en el rango 0 a M-1)

def simulacion(env, num_cajeros):
    cajeros = simpy.Resource(env, num_cajeros)  # Crear recursos tipo caja
    cliente_id = 0
    while True:
        yield env.timeout(random.expovariate(LAMBDA / 60))  # Simular llegada de clientes
        cliente_id += 1
        env.process(cliente(env, f"Cliente {cliente_id}", cajeros))  # Iniciar el proceso de atención al cliente

if __name__ == "__main__":
    env = simpy.Environment()  # Inicializar el entorno de simulación
    env.process(simulacion(env, M))  # Iniciar la simulación
    env.run(until=HORAS * 60)  # Ejecutar la simulación durante el tiempo especificado (en minutos)

    tiempo_promedio_espera /= clientes_atendidos  # Calcular el tiempo promedio de espera
    clientes_en_cola_promedio = tiempo_promedio_espera * (LAMBDA / 60)  # Calcular el número promedio de clientes en la cola
    
    # Imprimir estadísticas de la simulación
    #print("Cliente".ljust(13) + " | " + "Llegada".ljust(13) + " | " + "Espera".ljust(13) + " | " + "Salida".ljust(13))
    #print("-" * 52)
    #for registro in log:
    #    print(registro)

    print(f"\nTiempo promedio de espera en la cola: {tiempo_promedio_espera:.2f} minutos")
    print(f"Número promedio de clientes en la cola: {clientes_en_cola_promedio:.2f}")

    # Calcular y mostrar el grado o factor de utilización de cada cajero
    print("\nGrado o Factor de Utilización de las Cajas:")
    for i, tiempo in enumerate(tiempos_servicio, 1):
        factor_utilizacion = tiempo / (HORAS * 60)
        print(f"Caja {i}: {factor_utilizacion:.2%}")
