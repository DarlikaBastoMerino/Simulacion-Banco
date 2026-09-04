import simpy
import random

# ============================================
# SIMULACIÓN DE ATENCIÓN DE CLIENTES EN UN BANCO
# ============================================

def cliente(env, nombre, cajeros, tiempo_atencion_min,
            tiempo_atencion_max, tiempos_espera, datos_sistema):

    # Momento en que llega el cliente
    llegada = env.now

    print(f"\n{nombre} llegó al banco en el minuto {llegada:.2f}")

    # El cliente solicita un cajero
    with cajeros.request() as solicitud:

        # Registrar la cantidad de personas en espera
        if cajeros.count >= cajeros.capacity:
            longitud_fila = len(cajeros.queue) + 1

            if longitud_fila > datos_sistema["max_fila"]:
                datos_sistema["max_fila"] = longitud_fila

        # Esperar hasta que haya un cajero disponible
        yield solicitud

        # Momento en que comienza la atención
        inicio_atencion = env.now

        # Calcular tiempo de espera
        tiempo_espera = inicio_atencion - llegada
        tiempos_espera.append(tiempo_espera)

        print(
            f"{nombre} comenzó a ser atendido "
            f"en el minuto {inicio_atencion:.2f}"
        )

        print(
            f"Tiempo de espera: "
            f"{tiempo_espera:.2f} minutos"
        )

        # Tiempo de atención aleatorio entre 2 y 8 minutos
        tiempo_atencion = random.uniform(
            tiempo_atencion_min,
            tiempo_atencion_max
        )

        # Simular el tiempo de atención
        yield env.timeout(tiempo_atencion)

        print(
            f"{nombre} terminó su atención "
            f"en el minuto {env.now:.2f}"
        )

        print(
            f"Duración de la atención: "
            f"{tiempo_atencion:.2f} minutos"
        )


def generar_clientes(
    env,
    numero_clientes,
    cajeros,
    llegada_min,
    llegada_max,
    atencion_min,
    atencion_max,
    tiempos_espera,
    datos_sistema
):

    for i in range(numero_clientes):

        # El primer cliente llega al inicio
        if i > 0:

            # Tiempo aleatorio entre llegadas:
            # entre 2 y 5 minutos
            tiempo_entre_llegadas = random.uniform(
                llegada_min,
                llegada_max
            )

            yield env.timeout(tiempo_entre_llegadas)

        # Crear el proceso del cliente
        env.process(
            cliente(
                env,
                f"Cliente {i + 1}",
                cajeros,
                atencion_min,
                atencion_max,
                tiempos_espera,
                datos_sistema
            )
        )


# ============================================
# PROGRAMA PRINCIPAL
# ============================================

print("=" * 60)
print("   SIMULACIÓN DE ATENCIÓN DE CLIENTES EN UN BANCO")
print("=" * 60)

print("\nDatos obtenidos mediante la observación de campo.")
print("Presione ENTER para utilizar los datos observados.\n")


# ============================================
# DATOS DE LA OBSERVACIÓN
# ============================================

numero_clientes = input(
    "Número de clientes observados [26]: "
)

if numero_clientes == "":
    numero_clientes = 26
else:
    numero_clientes = int(numero_clientes)


llegada_min = input(
    "Tiempo mínimo entre llegadas en minutos [2]: "
)

if llegada_min == "":
    llegada_min = 2
else:
    llegada_min = float(llegada_min)


llegada_max = input(
    "Tiempo máximo entre llegadas en minutos [5]: "
)

if llegada_max == "":
    llegada_max = 5
else:
    llegada_max = float(llegada_max)


numero_cajeros = input(
    "Número de cajeros disponibles [8]: "
)

if numero_cajeros == "":
    numero_cajeros = 8
else:
    numero_cajeros = int(numero_cajeros)


atencion_min = input(
    "Tiempo mínimo de atención en minutos [2]: "
)

if atencion_min == "":
    atencion_min = 2
else:
    atencion_min = float(atencion_min)


atencion_max = input(
    "Tiempo máximo de atención en minutos [8]: "
)

if atencion_max == "":
    atencion_max = 8
else:
    atencion_max = float(atencion_max)


# ============================================
# CREAR ENTORNO DE SIMPY
# ============================================

env = simpy.Environment()


# Los cajeros representan el recurso limitado
cajeros = simpy.Resource(
    env,
    capacity=numero_cajeros
)


# ============================================
# VARIABLES PARA GUARDAR RESULTADOS
# ============================================

tiempos_espera = []

datos_sistema = {
    "max_fila": 0
}


# ============================================
# INICIAR SIMULACIÓN
# ============================================

env.process(
    generar_clientes(
        env,
        numero_clientes,
        cajeros,
        llegada_min,
        llegada_max,
        atencion_min,
        atencion_max,
        tiempos_espera,
        datos_sistema
    )
)


# Ejecutar la simulación
env.run()


# ============================================
# CALCULAR RESULTADOS
# ============================================

promedio_espera = (
    sum(tiempos_espera)
    / len(tiempos_espera)
)

maximo_espera = max(tiempos_espera)


# ============================================
# MOSTRAR RESULTADOS
# ============================================

print("\n")
print("=" * 60)
print("                    RESULTADOS")
print("=" * 60)

print(
    f"Clientes simulados: "
    f"{numero_clientes}"
)

print(
    f"Cajeros disponibles: "
    f"{numero_cajeros}"
)

print(
    f"Tiempo entre llegadas: "
    f"{llegada_min:.2f} - {llegada_max:.2f} minutos"
)

print(
    f"Tiempo de atención: "
    f"{atencion_min:.2f} - {atencion_max:.2f} minutos"
)

print(
    f"Tiempo promedio de espera: "
    f"{promedio_espera:.2f} minutos"
)

print(
    f"Tiempo máximo de espera: "
    f"{maximo_espera:.2f} minutos"
)

print(
    f"Mayor longitud de fila registrada: "
    f"{datos_sistema['max_fila']} personas"
)

print(
    f"Tiempo total de simulación: "
    f"{env.now:.2f} minutos"
)

print("=" * 60)
print("Simulación terminada.")