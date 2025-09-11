# Código principal que arranca el bot y carga las extensiones (cogs)
import os                          # Interactua con el SO para obtener la información de las variables de entorno. 
import asyncio                     # Para ejecutar la función main() asíncrona
from dotenv import load_dotenv     # Para leer .env (donde se tendrán las variables de entorno configuradas)
import discord                     # Importa la librería principal de discord
from discord.ext import commands   # Extensiones para comandos

# Cargamos en esta aplicación las variables de entorno desde el .env (si existe)
load_dotenv()                      # Lee un archivo .env y carga sus pares de clave-valor como variables de entorno en la aplicación Python.
TOKEN = os.getenv("BOT_TOKEN")     # con esto se logra NO poner el token en el código ( esto es una práctica segura)

if not TOKEN:
    # Si no hay token no funciona la aplicación por eso se va a recibir un mensaje de error
    raise RuntimeError("Falta BOT_TOKEN en .env — se debe copiar .env.example a .env y poner el token")

# Intents: indica qué eventos queremos recibir.
# message_content es necesario si querés leer el contenido de cada mensaje (para comandos con prefijo y detección de texto).
intents = discord.Intents.default()
intents.message_content = True

# Prefijo: es lo que el usuario escribe para comandos 'tradicionales' (ej: !hola).
    # Se puede usar string, lista de strings, o funciones.
        # 1 - Lista de Strings :   
            # bot = commands.Bot(command_prefix=["!", ".", "?"], intents=intents) 
            # el bot responde a !comando, .comando, o ?comando. 
        # 2 -  Funciones
            # def obtener_prefijo(bot, message):
            #     if message.guild and message.guild.id == 123456789:
            #         return "?"
            #     return "!"
            # si el mensaje viene de un servidor específico, el prefijo será "?", si no, será "!".
            # bot = commands.Bot(command_prefix=obtener_prefijo, intents=intents) 
                # cómo python puede procesar una función sin pasarle explícitamente los parámetros? 
                    # las funciones son objetos de primera clase en python : 
                        # se las puede pasar como argumentos a otras funciones
                        # asignarlas a variables,
                        # se pueden retornar desde funciones,
                        # se pueden almacenar en estructura de datos (listas, diccionarios, etc)
                        # es decir, usarlas como cualquier otro dato.
                        # Esto es porque Python es multipradigma
                            #  soporta paradigma orientado a objetios, funcional y procedimental (imperativo) , 
                            # no es un leguaje lógico pero posee bibliotecas que intentan emularlo.
                            # Se puede tener código en Python que sea: 
                                # Muy estructurado y orientado a objetos
                                # Minimalista y funcional
                                # Procedimental y directo. 
                                # O incluso mezclar estilos. Por ejemplo, usar clases para modelar datos y funciones puras para procesarlos. 
                    # lo que ocurre internamente en la librería discord.py
                        # 1- prefix = command_prefix(bot, message) no se ve en el código fuente pero si esta en la librería:  
                            # if callable(self.command_prefix):
                            # prefix = await utils.maybe_coroutine(self.command_prefix, self, message). self.command_prefix 
                            # es lo que se le pasa al bot (en este caso, la función obtener_prefijo).
                            # callable(...) verifica si eso es una función. utils.maybe_coroutine(...) llama a esa función 
                            # con los argumentos self (el bot) y message.
            # 3 - String
bot = commands.Bot(command_prefix="!", intents=intents, help_command=commands.DefaultHelpCommand())

# Evento: cuando el bot está listo
@bot.event # decorador que se aplica a funciones que manejan eventos del bot, proviene de la librería discord.py
async def on_ready():
    # on_ready se llama cuando el bot está conectado y listo.
    print(f"Bot conectado como {bot.user} (id: {bot.user.id})")
    # esto no es una buena práctica aquí: sincronizar comandos slash/híbridos: 
        # try:
        #     synced = await bot.tree.sync()
        #     print(f"Sincronizados {len(synced)} comandos de aplicación (global).")
        # except Exception as e:
        #     print("No se pudieron sincronizar los comandos de aplicación:", e)
        # sincronizar globalmente puede tardar hasta 1 hora en propagarse en Discord.

        # Cómo funciona la sincronización de slash/híbridos? 
        # Cuando se define @commands.hybrid_command, ese comando tiene que registrarse en la API de Discord.
        # Esa "sincronización" (el famoso await bot.tree.sync()) puede hacerse:
            # Globalmente → tarda hasta 1 hora en aparecer en todos los servidores. 
                # Si se hace seguido, puede ocurrir límites de rate-limit.
                    # rate-limit se traduce como limitado por tasa o restricción de frecuencia
                    # mecanismo de los sistemas informáticos para controlar cuántas veces se puede hacer una acción 
                    # en un período de tiempo (con el objetivo de evitar spam y sobrecargas).
                    # mensaje “You are being rate limited” (discord) aparece cuando intentas hacer una acción demasiadas veces 
                    # en poco tiempo, como: enviar muchos mensajes seguidos, intentar verificar el número de teléfono repetidamente, 
                    # hacer clic en botones de verificación sin esperar. 
                    # Discord bloquea al usuraio temporalmente (desde unos segundos hasta varios minutos) para proteger el sistema. 
            # Por servidor (guild-specific) → aparece al instante, ideal para pruebas, casi sin riesgo de rate-limit.


# NO conviene sincronizar siempre en on_ready porque cada vez que reiniciás el bot, va a intentar registrar todo de nuevo. Lo correcto: sincronizar sólo cuando cambiaste comandos o manualmente con un comando oculto para vos. # Lo correcto sería sincronizar para un solo GUILD (1 servidor). 


# Cargar extensiones (cogs). Esto es asíncrono y por eso usamos await.
# asíncrono : forma de ejecutar código sin bloquear el flujo principal.
# Permite que el programa siga funcionando mientras espera que algo termine 
# (como leer un archivo, esperar una respuesta de red, etc.).
# Se usa mucho en bots, servidores web, y apps que manejan múltiples tareas al mismo tiempo.
# await: indica que hay que esperar a la tarea que se esta procesando, pero permite seguir con otras tareas
# se usa dentro de funciones asíncronas (async def) para esperar el resultado de otra función asíncrona.

# load_extensions(): función que viene por defecto en commands.Bot. Sirve para cargar un módulo externo (llamado cog) 
# que contiene comandos, eventos, etc. útil para organizar tu bot en archivos separados, manteniendo el código limpio y modular. 
# "cogs.ejemplo" no es una ruta de archivo tradicional con barras (/ o \). Es una ruta estilo módulo de Python.

# "cogs.ejemplo" significa: → Hay un archivo llamado ejemplo.py dentro de una carpeta llamada cogs.

# En Python, los módulos se importan así: from cogs import ejemplo Por eso se usa el punto (.) en vez de la barra.

# Elemento	¿Qué es?
# async def	Define una función asíncrona.
# await	Espera una tarea sin bloquear el programa.
# bot.load_extension()	Carga un módulo externo (cog) al bot.
# "cogs.ejemplo"	Ruta estilo módulo: archivo ejemplo.py dentro de carpeta cogs.

async def load_extensions():
    # "cogs.ejemplo" corresponde al archivo cogs/ejemplo.py (ruta estilo módulo Python)
    # Esto le dice al bot: “Cargá esta extensión, pero no bloquees todo el programa mientras lo hacés.”
    await bot.load_extension("cogs.ejemplo")

# Usamos un patrón 'async main' moderno para manejar bien el ciclo de vida del bot.
async def main():
    # 'async with bot' abre el bot como contexto asíncrono: hace inicializaciones y asegura limpieza al salir.
    async with bot:
        await load_extensions()      # cargamos los cogs antes de iniciar la conexión
        await bot.start(TOKEN)      # inicia la conexión con Discord (websocket, loop, eventos)

# Punto de entrada del script
if __name__ == "__main__":
    # asyncio.run crea un loop, ejecuta main() y cierra el loop al terminar.
    asyncio.run(main())
