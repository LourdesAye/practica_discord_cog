async def saludar():
    await print("Hola")  # ❌ Error

saludar()

# RuntimeWarning: coroutine 'saludar' was never awaited saludar()
# RuntimeWarning: Enable tracemalloc to get the object allocation traceback

# El mensaje indica que llamaste a saludar() directamente, sin usar await, lo que significa que la función nunca se ejecutó como se esperaba.
# tracemalloc es una herramienta que te permite rastrear dónde se asignan los objetos en memoria, útil para depurar problemas más complejos.

# Una corrutina en Python es una función que se define con async def 
# y se puede ejecutar de dos maneras
    # 1- Usar asyncio.run()
    # 2- Dentro de otra corrutina con await

# LO CORRECTO
# Usar asyncio.run() # Para ejecutar una corutina directamente
import asyncio

async def saludar(): # Define una función que devuelve una corrutina (no la ejecuta)
    print("Hola")

asyncio.run(saludar())  # ✅ Esto sí ejecuta la corrutina

 # ¿Qué hace asyncio.run(funcion_que_devuelve_corrutina())?
    # Ejecuta una corutina principal desde un entorno síncrono.
    # Crea un loop de eventos, corre la corutina, y lo cierra automáticamente.
    # Es ideal para scripts o programas que arrancan con una única corutina.

# Dentro de otra corrutina con await # Para encadenar corutinas, lógica más compleja
async def saludar(): # Define una función que devuelve una corrutina (no la ejecuta)
    print("Hola")

async def main(): # Define una función que devuelve una corrutina (no la ejecuta)
    await saludar() # se llama a una corrutina dentro de otra utilizando await

asyncio.run(main())   # ✅ Esto sí ejecuta la corrutina

# Acá estás definiendo una corutina (main()) que espera (await) otra corutina (saludar()).
# Luego usás asyncio.run() para ejecutar la corutina principal (main()).
# Útil cuando querés encadenar tareas asincrónicas o tener una lógica más compleja.

# No se puede usar await directamente en el nivel superior de un script (fuera de una función async). 
# Por eso existe asyncio.run() : para poder arrancar el mundo asincrónico desde el mundo síncrono.


# Un loop de eventos (o event loop)
    # Se crea automáticamente con asyncio.run() (que también ejecuta la corutina principal y luego la cierra)
    # Es el motor que ejecuta tareas asincrónicas. 
    # Es como un director de orquesta que:
        # Escucha eventos (como "esta tarea ya terminó").
        # Decide qué corutina ejecutar a continuación.
        # Coordina múltiples tareas sin bloquear el programa.
    # En Python, este loop lo maneja el módulo asyncio.


# Mundo     ->	¿Qué lo representa?	-> ¿Qué hace?
# Síncrono	->  Código normal	    -> Ejecuta paso a paso
# Asíncrono	->  async def, await	-> Permite tareas concurrentes
# El puente	->  asyncio.run()	    -> Inicia el loop y conecta ambos mundos



 
 

