'''
Teoria de colas, utilizado para analizar sistemas con demanda y recursos limitados.

1. Proceso de Poisson: Los clientes llegan de manera aleatoria a una tasa constante promedio.
2. Distribucion exponencial: Describe el tiempo entre eventos en un proceso de Poisson. 
   En este ejercicio, el tiempo entre llegadas y el tiempo de servicio siguen esta distribucion.
3. Seleccion de caja: El cliente elige la caja con menos personas. Si hay empate, elige al azar.
4. Metricas:
   - Tiempo promedio en la cola: Tiempo que un cliente pasa esperando antes de ser atendido.
   - Numero promedio de clientes en la cola: Promedio de clientes esperando en cualquier momento.
   - Factor de utilizacion: Fraccion del tiempo que un cajero esta ocupado atendiendo clientes.

Si el numero promedio de clientes en la cola es 0.00, significa que, en promedio, no hay clientes esperando, 
posiblemente porque los cajeros atienden rapidamente en comparacion con la tasa de llegada.

El grado o factor de utilizacion de una caja (o de cualquier recurso en teoría de colas) representa la 
proporcion del tiempo que esa caja estuvo ocupada atendiendo a clientes, en relacion con el tiempo total 
de la simulacion. No es necesario que sumen 100%. Cada caja es un recurso independiente y su factor 
de utilizacion refleja cuanto estuvo ocupada en relacion con el tiempo total de la simulacion.
'''

'''

--- EXPLICACION DEL PROGRAMA ---

Proceso de Llegada de Clientes:

El programa simula la llegada de clientes a la sucursal mediante un proceso de Poisson. En matemáticas, un proceso de Poisson es un proceso estocástico que describe eventos aleatorios que ocurren a una tasa constante promedio (en este caso, λ clientes por hora).
Utiliza una distribución exponencial para modelar el tiempo entre llegadas de clientes. La distribución exponencial es comúnmente utilizada en teoría de colas y se caracteriza por tener una tasa λ. En este contexto, λ representa la tasa promedio de llegada de clientes por hora.
Selección de Caja:

Cuando un cliente llega a la sucursal, elige una de las cajas disponibles. La elección se basa en el principio de que el cliente seleccionará la caja con la menor cantidad de personas en espera.
Si hay varias cajas con la misma cantidad mínima de personas en espera, el cliente elige una de ellas al azar.
Atención al Cliente:

Cada caja se modela como un recurso de SimPy que representa a un cajero.
El tiempo que un cliente pasa siendo atendido en una caja sigue una distribución exponencial con una tasa λ1 (clientes atendidos por hora). En matemáticas, esto modela el tiempo que se necesita para servir a un cliente en una caja.
Recopilación de Estadísticas:

Durante la simulación, el programa recopila información importante:
Tiempo que cada cliente pasa en la cola antes de ser atendido.
Número de clientes en la cola en cada intervalo de tiempo.
Tiempo total de servicio por caja.
Resultados:

Al final de la simulación, el programa calcula y muestra estadísticas clave:
El tiempo promedio que un cliente pasa en la cola.
El número promedio de clientes en la cola.
El grado o factor de utilización de cada cajero, que representa la fracción de tiempo que cada cajero está ocupado atendiendo clientes en relación con el tiempo total de simulación.
'''


# Importación de librerías necesarias
import simpy  # Librería para simulación de eventos discretos
import random  # Librería para generación de números aleatorios

# Parámetros de la simulación
CLIENTES_HORA = 20  # Tasa de llegada de clientes por hora
CAJAS_HORA = 5  # Tasa de servicio en cajas por hora
NUM_CAJAS = 5  # Número de cajas en la sucursal
SIMULATION_TIME = 480  # Duración de la simulación en minutos

# Variables para recopilar estadísticas
tiempos_en_cola = []  # Lista para almacenar los tiempos que cada cliente pasó en la cola
tiempos_liberacion_cajas = [0 for _ in range(NUM_CAJAS)]  # Lista para los tiempos en que se liberarán las cajas
tiempos_servicio = [0 for _ in range(NUM_CAJAS)]  # Lista para los tiempos totales de servicio por caja
longitud_cola = []  # Lista para la longitud de la cola en cada intervalo de tiempo

# Definición de la función para simular el proceso de atención al cliente por un cajero
def cliente(env, caja, cliente_id, tiempo_llegada, indice_caja):
    with caja.request() as req:
        yield req  # Esperar hasta que el cajero esté disponible
        # Tiempo que tomará atender al cliente (distribución exponencial)
        servicio_time = random.expovariate(1/CAJAS_HORA)
        # Actualizar el tiempo total de servicio del cajero
        tiempos_servicio[indice_caja] += servicio_time
        yield env.timeout(servicio_time)  # Simular el tiempo de servicio
        salida = env.now
        # Actualizar el tiempo de liberación de la caja
        tiempos_liberacion_cajas[indice_caja] = salida
        # Imprimir el cliente atendido y el tiempo que pasó en la caja
        print(f"Cliente {cliente_id} atendido en {caja.name} en {salida - tiempo_llegada:.2f} minutos")
        # Guardar el tiempo que el cliente pasó en la cola
        tiempos_en_cola.append(salida - tiempo_llegada)

# Definición de la función para simular la llegada de clientes al supermercado
def llegada_clientes(env, cajas):
    cliente_id = 0
    while True:
        # Tiempo hasta la llegada del siguiente cliente (distribución exponencial)
        yield env.timeout(random.expovariate(1/CLIENTES_HORA))
        cliente_id += 1

        # Estimación del tiempo de espera en cada caja
        tiempos_espera = []
        for i, caja in enumerate(cajas):
            tiempo_espera = tiempos_liberacion_cajas[i] + (len(caja.queue) + 1) / CAJAS_HORA
            tiempos_espera.append(tiempo_espera)

        # Calcular la cantidad total de clientes en la cola
        total_clientes_cola = sum([len(caja.queue) for caja in cajas])
        longitud_cola.append(total_clientes_cola)  # Registrar la longitud de la cola en cada intervalo de tiempo

        # El cliente elige la caja con el tiempo de espera más corto
        indice_caja_disponible = tiempos_espera.index(min(tiempos_espera))
        caja_disponible = cajas[indice_caja_disponible]
        # Imprimir que el cliente se une a la cola de una caja específica
        print(f"Cliente {cliente_id} se une a la cola en {caja_disponible.name}")
        env.process(cliente(env, caja_disponible, cliente_id, env.now, indice_caja_disponible))

# Inicialización de la simulación
env = simpy.Environment()
cajas = [simpy.Resource(env) for i in range(NUM_CAJAS)]  # Crear las cajas como recursos

# Asignar nombres a cada caja
for i, caja in enumerate(cajas):
    caja.name = f"Caja {i + 1}"

# Iniciar el proceso de llegada de clientes y ejecutar la simulación
env.process(llegada_clientes(env, cajas))
env.run(until=SIMULATION_TIME)  # Ejecutar la simulación

# Calcular el tiempo promedio que un cliente pasa en la cola
tiempo_promedio_en_cola = sum(tiempos_en_cola) / len(tiempos_en_cola)
print(f"\nTiempo promedio en la cola: {tiempo_promedio_en_cola:.2f} minutos")

# Calcular y mostrar el número promedio de clientes en la cola
clientes_promedio_cola = sum(longitud_cola) / len(longitud_cola)
print(f"Número promedio de clientes en la cola: {clientes_promedio_cola:.2f}")

# Calcular y mostrar el grado o factor de utilización de cada cajero
print("\nGrado o Factor de Utilización de las Cajas:")
for i, tiempo in enumerate(tiempos_servicio, 1):
    factor_utilización = tiempo / SIMULATION_TIME
    print(f"Caja {i}: {factor_utilización:.2%}")
