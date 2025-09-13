# coroutine 
# # función especial que puede pausar su ejecución y luego retomarla más tarde.  
# # A diferencia de una función común (que empieza y termina de corrido), 
# una coroutine puede “esperar” algo sin bloquear el resto del programa. 
# En Python se definen con async def y se usan con await. 

# Esto sirve para hacer varias tareas a la vez (concurrencia), como esperar respuestas de internet, 
# manejar mensajes de Discord, etc., sin congelar el programa.

import asyncio

async def saludar(): # async def → define una coroutine.
    print("Hola")
    # await → dice “esperá acá, mientras tanto seguí con otra cosa”.
    await asyncio.sleep(1)   # pausa 1 segundo sin trabar el programa 
    print("¿Cómo estás?")

asyncio.run(saludar())