# import asyncio

# async def contador(nombre, segundos):
#     for i in range(1, segundos + 1):
#         print(f"{nombre}: {i}")
#         await asyncio.sleep(1)  # acá se "pausa" y da lugar a otras corutinas
#     print(f"{nombre} terminado.")

# async def main():
#     # Lanzamos dos contadores al mismo tiempo
#     tarea1 = asyncio.create_task(contador("Contador A", 5))
#     tarea2 = asyncio.create_task(contador("Contador B", 5))

#     await tarea1
#     await tarea2

# asyncio.run(main())

import asyncio
import time

async def contador(nombre, segundos, stats):
    inicio = time.perf_counter()
    interrupciones = 0

    for i in range(1, segundos + 1):
        print(f"{nombre}: {i}")
        await asyncio.sleep(1)  # se pausa y cede el control
        interrupciones += 1

    fin = time.perf_counter()
    stats[nombre] = {
        "tiempo_total": round(fin - inicio, 2),
        "interrupciones": interrupciones
    }
    print(f"{nombre} terminado.")

# async def: significa que se está definiendo una corutina, que la ejecuta el event loop
async def main():
    stats = {}
    # time.perf_counter(): para medir el tiempo con alta precisión 
    inicio_global = time.perf_counter()
    # asyncio.create_task: para la concurrencia en asyncio, ya que permite ejecutar múltiples corrutinas simultáneamente 
    # sin bloquear la ejecución del programa principal. 
    tarea1 = asyncio.create_task(contador("Contador A", 5, stats))
    tarea2 = asyncio.create_task(contador("Contador B", 5, stats))

    await tarea1
    await tarea2

    fin_global = time.perf_counter()
    tiempo_total = round(fin_global - inicio_global, 2)

    print("\n--- Resultados ---")
    print(f"Tiempo total de ejecución: {tiempo_total} segundos")
    for nombre, datos in stats.items():
        print(f"{nombre}: {datos['tiempo_total']}s, "
              f"Interrupciones: {datos['interrupciones']}")

# aquí se crea el event loop, el encagado de ejecutar las corutinas
asyncio.run(main())
