# cogs/ejemplo.py
# Ejemplo de Cog con:
#  - comando clásico (prefijado) -> @commands.command()
#  - comando híbrido (prefijo + slash) -> @commands.hybrid_command()
#  - listener (manejador de evento) -> @commands.Cog.listener()
#
# Finalmente exportamos async def setup(bot) para que load_extension lo llame.

import discord
from discord.ext import commands

class EjemploCog(commands.Cog):
    """Un Cog que agrupa comandos y listeners relacionados."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot  # guardamos referencia al bot si la necesitamos

    # ------------------------
    # Comando clásico (prefijo)
    # ------------------------
    @commands.command(name="hola", help="Responde con un saludo (comando con prefijo).")
    async def hola(self, ctx: commands.Context):
        # ctx = contexto de la invocación: autor, canal, guild, message, etc.
        # ctx.send() envía un mensaje al canal donde se llamó el comando.
        await ctx.send(f"¡Hola, {ctx.author.mention}! 👋")

    # -------------------------
    # Comando híbrido (prefijo + slash)
    # -------------------------
    @commands.hybrid_command(name="saludo", description="Saluda — funciona como prefijo y como slash command")
    async def saludo(self, ctx: commands.Context, nombre: str = "amigx"):
        """
        Este comando es 'híbrido': puede ejecutarse como:
          - !saludo    (prefijo)
          - /saludo    (slash)
        Los hybrid commands permiten mantener una sola implementación para ambos estilos.
        """
        # Cuando se invoca desde slash, ctx.respond() está disponible internamente.
        await ctx.send(f"¡Hola {nombre}! (invocado por {ctx.author.display_name})")

    # ------------------------
    # Listener / manejador de evento
    # ------------------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Los listeners reciben todos los eventos. Aquí escuchamos on_message.
        # Evitamos que el bot responda a sí mismo:
        if message.author.bot:
            return

        # Respuesta simple si alguien escribe 'chau'
        if "chau" in message.content.lower():
            await message.channel.send("¡Hasta luego! 👋")

        # MUY IMPORTANTE: si definís un on_message y querés que los comandos con prefijo
        # sigan funcionando, tenés que procesarlos manualmente:
        await self.bot.process_commands(message)

# Esta función es la que load_extension busca y ejecuta.
# En discord.py moderno se recomienda que sea async y que haga await bot.add_cog(...)
async def setup(bot: commands.Bot):
    await bot.add_cog(EjemploCog(bot))
