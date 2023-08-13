import disnake
import json
import os
from disnake.ext import commands

bot = commands.Bot(command_prefix="-", intents=disnake.Intents.all())

with open('config.json', 'r') as json_file:
    data = json.load(json_file)

for filename in os.listdir("./commands"):
  if filename.endswith('.py'):
    bot.load_extension(f'commands.{filename[:-3]}')

bot.run(data["token"])