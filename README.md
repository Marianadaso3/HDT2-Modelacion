# HDT2-Modelacion

## Autores

- Mariana David
- Angel Higueros
- Jorge Caballeros
- Fredy Velasquez

## Librerias 

Existen dos formas de instalar simpy 

1. `pip install simpy`
2. En terminal ejecutar ` /opt/homebrew/opt/python@3.11/bin/pip3 install simpy`

## Ejecucion

Correr el comando `python3 tarea.py`

## Explicacion del programa

### Proceso de Llegada de Clientes:

- El programa simula la llegada de clientes a la sucursal mediante un proceso de Poisson. En matemáticas, un proceso de Poisson es un proceso estocástico que describe eventos aleatorios que ocurren a una tasa constante promedio (en este caso, λ clientes por hora).
- Utiliza una distribución exponencial para modelar el tiempo entre llegadas de clientes. La distribución exponencial es comúnmente utilizada en teoría de colas y se caracteriza por tener una tasa λ. En este contexto, λ representa la tasa promedio de llegada de clientes por hora.

### Selección de Caja:

- Cuando un cliente llega a la sucursal, elige una de las cajas disponibles. La elección se basa en el principio de que el cliente seleccionará la caja con la menor cantidad de personas en espera.
- Si hay varias cajas con la misma cantidad mínima de personas en espera, el cliente elige una de ellas al azar.

### Atención al Cliente:

- Cada caja se modela como un recurso de SimPy que representa a un cajero.
- El tiempo que un cliente pasa siendo atendido en una caja sigue una distribución exponencial con una tasa λ1 (clientes atendidos por hora). En matemáticas, esto modela el tiempo que se necesita para servir a un cliente en una caja.

### Recopilación de Estadísticas:

- Durante la simulación, el programa recopila información importante:
- Tiempo que cada cliente pasa en la cola antes de ser atendido.
- Número de clientes en la cola en cada intervalo de tiempo.
- Tiempo total de servicio por caja.

### Resultados:

- Al final de la simulación, el programa calcula y muestra estadísticas clave:
- El tiempo promedio que un cliente pasa en la cola.
- El número promedio de clientes en la cola.
- El grado o factor de utilización de cada cajero, que representa la fracción de tiempo que cada cajero está ocupado atendiendo clientes en relación con el tiempo total de simulación.
'''
