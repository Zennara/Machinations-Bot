#general imports I almost always need for bots
import discord #pycord
import os #for token
import requests #for rate limit checker
import json
import keep_alive
from discord.commands import Option #slash commands, options, permissions
from datetime import datetime #time and ping command

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

guild_ids = [806706495466766366, 910935393497657374] #enter your guild ID's here for instant use instead of waiting for global slash registration

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

@bot.slash_command(description="Test the Machinations API, will take a few seconds.",guild_ids=guild_ids)
async def generate(ctx, prompt:Option(str, "The prompt for the AI to generate"), mode:Option(str, "The mode to use for generation", choices=["manual","auto"], required=False, default=None), version:Option(str, "The version to use", choices=["v1","v2","v3","v4"], required=False, default=None)):
  await ctx.defer()
  payload = {'prompt': prompt}
  v = ""
  m = ""
  if mode != None:
    payload["mode"] = mode
    m = f"**Mode**: `{mode}`\n"
  if version != None:
    payload["version"] = version
    v = f"**Version**: `{version}`\n"  

  r = requests.post('https://machinations-app-api-mainnet-p5utl2xkua-uc.a.run.app/snapshot/create-test', data=payload)
  dt = json.loads(r.text)
  p = dt["prompt"]
  embed = discord.Embed(color=0x000000, description=f"**Prompt**: `{p}`\n{v}{m}")
  embed.set_image(url=dt["full_image_url"])
  await ctx.respond(embed=embed)
  
#<-----------------------EVENTS----------------------->
@bot.event
async def on_ready():
  print(f"{bot.user.name} Online.")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Machinations NFT"))
  #set onlineTime for /ping commands 
  global onlineTime
  onlineTime = datetime.now()
  
#<-----------------------FUNCTIONS----------------------->

#simple error message, passes ctx from commands
async def error(ctx, code):
  embed = discord.Embed(color=0xFF0000, description= f"❌ {code}")
  await ctx.respond(embed=embed, ephemeral=True)

keep_alive.keep_alive()  #keep the bot alive
#bot
bot.run(os.environ.get("TOKEN"))  #secret variable named 'TOKEN'