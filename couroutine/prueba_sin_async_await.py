# 🔴 Versión bloqueante y secuencial (sin async/await)
# Tarda 6 segundos (bloqueante) en cambio el otro ejemplo: 2 segundos (asíncrono/concurrente).
import time # se usa para hacer pausas con sleep()
from datetime import datetime # se usa para obtener la hora actual y medir duración.

# Devuelve la hora actual como string, con formato HH:MM:SS.mmm. (mmm:milisegundos)
def now():
    # now() para obtener la fecha y hora actual local formato: 
    # year, month, day, hour, minute, second, and microsecond: 2025-09-12 15:36:00.123456
    # datetime.now().strftime("%H:%M:%S.%f") Podría devolver algo como: 15:42:07.123456
    # %f te da microsegundos (6 dígitos): donde .123456 son los microsegundos.
    return datetime.now().strftime("%H:%M:%S.%f")[:-3] 
    # strftime(...): convierte la hora a texto.
    # [:-3]: recorta los últimos 3 dígitos de los microsegundos para dejar solo milisegundos.
        # se muestran los milisegundos de forma visual, no se hacen cálculos precisos con ellos.

# Define una tarea que bloquea el programa durante delay segundos.
def blocking_task(name, delay):
    # Muestra la hora actual y que la tarea name está comenzando.
    print(f"{now()} - {name} start (blocking)")
    # Detiene la ejecución por delay segundos. Nada más se ejecuta en ese tiempo.
    time.sleep(delay)   # pausa REAL, bloquea todo el programa
    print(f"{now()} - {name} end (blocking)") # Muestra la hora actual y que la tarea terminó.

# función que ejecuta tres tareas una tras otra, sin solapamiento
def run_sequential():
    print("\nRUN SEQUENTIAL (blocking):") # Imprime un encabezado para indicar el tipo de ejecución.
    t0 = datetime.now()  # Guarda el tiempo de inicio para calcular duración total.
    # Ejecuta tres tareas, cada una con 2 segundos de pausa. 
    # Como son bloqueantes, se ejecutan en serie: primero A, luego B, luego C.
    blocking_task("Tarea A", 5)
    blocking_task("Tarea B", 5)
    blocking_task("Tarea C", 5)
    # Calcula y muestra el tiempo total transcurrido. Debería ser ~15 segundos.
    print(f"{now()} - Total elapsed: {datetime.now()-t0}\n") 

run_sequential() # Llama a la función para iniciar todo el proceso.

# Aca con delay :2
# RUN SEQUENTIAL (blocking):
# 17:52:21.962 - Tarea A start (blocking)
# 17:52:23.963 - Tarea A end (blocking)
# 17:52:23.963 - Tarea B start (blocking)
# 17:52:25.963 - Tarea B end (blocking)
# 17:52:25.963 - Tarea C start (blocking)
# 17:52:27.964 - Tarea C end (blocking)
# 17:52:27.964 - Total elapsed: 0:00:06.00

# Cada tarea espera 2 segundos completos antes de pasar a la siguiente. 
# El total fue 6 segundos.
# No hay concurrencia: cada tarea empiezó recién cuando terminó la anterior.

# Aca con delay:5
# RUN SEQUENTIAL (blocking):
# 19:17:56.340 - Tarea A start (blocking)
# 19:18:01.340 - Tarea A end (blocking)
# 19:18:01.341 - Tarea B start (blocking)
# 19:18:06.342 - Tarea B end (blocking)
# 19:18:06.342 - Tarea C start (blocking)
# 19:18:11.343 - Tarea C end (blocking)
# 19:18:11.344 - Total elapsed: 0:00:15.004420