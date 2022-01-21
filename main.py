#general imports I almost always need for bots
import discord #pycord
import os #for token
import requests #for rate limit checker
import asyncio #for asyncio functions
from discord.ext import commands #for commands
from discord.commands import Option, permissions #slash commands, options, permissions
from datetime import datetime #time and ping command

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

guild_ids = [] #enter your guild ID's here for instant use instead of waiting for global slash registration

#api limit checker | use 'kill 1' in the shell if you get limited
r = requests.head(url="https://discord.com/api/v1")
try:
  print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
  print("No rate limit")


#<-----------------------COMMANDS----------------------->
@bot.slash_command(description="Show the bot's uptime",guild_ids=guild_ids)
async def ping(ctx):
  embed = discord.Embed(color=0x00FF00, title="**Pong!**", description=f"{bot.user.name} has been online for {datetime.now()-onlineTime}!")
  await ctx.respond(embed=embed)

@bot.slash_command(description="Test the Machinations API",guild_ids=guild_ids)
async def generate(ctx, prompt:Option(str, "The prompt for the AI to generate"), ):
  embed = discord.Embed(color=0x00FF00, title="", description=f"")
  await ctx.respond(embed=embed)
  
#<-----------------------EVENTS----------------------->
@bot.event
async def on_ready():
  print(f"{bot.user.name} Online.")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Machinations NFT"))
  #set onlineTime for /ping commands 
  global onlineTime
  onlineTime = datetime.now()

  #persistance
  #bot.add_view(helpClass())
  
#<-----------------------FUNCTIONS----------------------->

#simple error message, passes ctx from commands
async def error(ctx, code):
  embed = discord.Embed(color=0xFF0000, description= f"❌ {code}")
  await ctx.respond(embed=embed, ephemeral=True)

#simple confirmation message, passes ctx from commands
async def confirm(ctx, code, eph): 
  embed = discord.Embed(color=0x00FF00, description= f"✅ {code}")
  await ctx.respond(embed=embed, ephemeral=eph)

#bot
bot.run(os.environ.get("TOKEN"))  #secret variable named 'TOKEN'