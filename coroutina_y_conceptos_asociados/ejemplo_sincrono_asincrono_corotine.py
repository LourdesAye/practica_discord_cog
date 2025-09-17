# PASAJE ENTRE EL MUNDO SÍNCRONO Y EL MUNDO ASÍNCRONO
# flujo de mensajes que refleja claramente el paso entre ambos mundos.  
import asyncio

# Mundo síncrono
print("Inicio en el mundo síncrono")

# Puente al mundo asíncrono
async def tarea(): # se usa async def para definir una corutina 
    print("Conectando con el mundo asíncrono...")
    await asyncio.sleep(1) # await con asyn def (await dentro de una corutina para esperar otra corutina o tarea asincrónica como asyncio.sleep(1))
    print("Estamos en el mundo asíncrono")

# Conexión
asyncio.run(tarea()) # se usa asyncio.run() para crear el event loop y ejecutar corutina desde el contexto síncrono 

# Mundo síncrono
print("Volviendo al mundo síncrono... Fin")



