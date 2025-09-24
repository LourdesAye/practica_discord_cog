# Coroutine 
# función que puede pausar su ejecución y luego retomarla más tarde. En Python se definen con async def.
# Puede quedar a la espera de una operación asíncrona sin bloquear el resto del programa. 
# Esto sirve para lograr concurrencia, cuando se esperar respuestas de internet, se consulta una API, sin congelar el programa.

import asyncio
import time

# async def → define una coroutine.
async def contador_de_segundos(nombre_contador_de_segundos, segundos_a_contar, estadisticas): 
    # time.perf_counter(): para medir el tiempo con alta precisión 
    inicio_tiempo_ejecución = time.perf_counter() 
    interrupciones = 0

    # genera un rango desde 1 hasta segundos_a_contar (es decir, cantidad de veces que se ejecuta el for: segundos_a_contar)
    for i in range(1, segundos_a_contar + 1): 
        print(f"{nombre_contador_de_segundos}: ejecutando {i} segundos")
        # asyncio.sleep(1) : se pausa 1 segundo y cede el control, da lugar a otras corutinas
        await asyncio.sleep(1) 
        # se considera el asyncio.sleep(1) una interrupción de la ejecución 
        interrupciones += 1

    # time.perf_counter(): para medir el tiempo con alta precisión 
    fin_tiempo_ejecucion = time.perf_counter()
    # estadisticas : diccionario donde la clave es el nombre del contador de segundos y el valor otro diccionario
        # el diccionario incluido posee dos pares de clave- valor: 
            # tiempo total de ejecución (de esta operación)
            # cantidad total de interrupciones (de esta operación)
    estadisticas[nombre_contador_de_segundos] = { 
        "tiempo_total_ejecucion": round(fin_tiempo_ejecucion - inicio_tiempo_ejecución, 2),
        "cantidad_total_interrupciones": interrupciones
    }
    print(f"\n{nombre_contador_de_segundos} terminado.")

# async def → define una coroutine.
async def main():
    # se inicializa un diccionario vacío
    estadisticas = {}
    # time.perf_counter(): para medir el tiempo con alta precisión 
    inicio_global = time.perf_counter()
    # asyncio.create_task: crea un objeto Task para que varias corrutinas se ejecuten de forma concurrente , sin bloquear la ejecución del programa principal o hilo. 
    tarea1 = asyncio.create_task(contador_de_segundos("Contador A", 5, estadisticas))
    tarea2 = asyncio.create_task(contador_de_segundos("Contador B", 5, estadisticas))
    # await es necesario para obtener los resultados de las corutinas una vez que se ejecutan
    await tarea1
    await tarea2
    # time.perf_counter(): para medir el tiempo con alta precisión 
    fin_global = time.perf_counter()
    # tiempo total de ejecución del programa entero
    tiempo_total = round(fin_global - inicio_global, 2)

    print("\n--- Resultados ---\n") # Se van a mostrar estadísticas de ejecución global y por operación
    print(f"Tiempo total de ejecución del programa entero: {tiempo_total} segundos\n") # tiempo total de ejecución del programa
    for nombre_contador_de_segundos, estadisticas_de_ejecucion in estadisticas.items(): # se recorre el diccionario obtiendo cada par clave,valor
        print(f"{nombre_contador_de_segundos}:\nTiempo Total de su Ejecución: {estadisticas_de_ejecucion['tiempo_total_ejecucion']}s, \n"
              f"Cantidad de Interrupciones: {estadisticas_de_ejecucion['cantidad_total_interrupciones']}")

# aquí se crea el event loop, el encagado de ejecutar las corutinas
asyncio.run(main())
