import discord
from discord.ext import commands
import os

bot_prefix = 'd.'
# doki is the botname/clientname
doki = commands.Bot(command_prefix=commands.when_mentioned_or(bot_prefix),case_insensitive=True,help_command=None)
for fcogs in os.listdir("./cogs"):
  if fcogs.endswith(".py") and fcogs != "__init__.py":
    doki.load_extension(f'cogs.{fcogs[:-3]}')

doki.run(os.getenv("Token"))