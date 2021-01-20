import discord #Discord libraries
import os
import json #Support for json files
from keepalive import keep_alive # imports the web server that pings the bot continually
from discord.ext import commands

client = discord.Client() # Connects to the discord client
client = commands.Bot(command_prefix = '&')
discord.ext.commands.Bot(command_prefix = '&', case_insensitive = True)
client.remove_command("help")

@client.event #Callback to a unsychronous library of events
async def on_ready():
  # When the bot is ready to be used
  await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='&rtfm'))

  print('Logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
  #Handles errors
  if isinstance(error, commands.CommandNotFound): # Command not found
    await ctx.send('Invalid command. Try &help to search for usable commands.')
  elif isinstance(error, commands.MissingRequiredArgument): # Manque d'arguments
    await ctx.send('A required argument is needed. Try &help to see required arguments.')
  else: # Erreur non supporté pour le moment
    await ctx.send('Error not defined. Please report this issue at https://github.com/Noobyprogrammer/Devsearch-Discord-bot')

@client.command()
async def rtfm(ctx): # Brief intro to the bot
  await ctx.send('I am there to save you, ask me someting with &Dev <language type>!\nSearching for a topic on StackOverflow? Type &Stack <Question>!\nWant more commands? Type &Dev help!\nWant to help the bot? Type &Git!\nAnd thanks to all the ones that made this idea possible! Type &Credits!')

@client.group(invoke_without_command=True, case_insensitive = True)
async def help(ctx):
  embed=discord.Embed(title="Devsearch", url="https://github.com/Noobyprogrammer/Devsearch-Discord-bot", description="Search into Application/Languages documentation and provides fast help to devs searching for solutions in their ideas.")
  embed.add_field(name="Dev", value="Use &Dev <language> to get information on links to the documentation. You can also add a keyword to precise your search! For supported documentations, use &help Dev.", inline=False)
  embed.add_field(name="Stack", value="Search for a question in stackoverflow with &Stack <Question>!", inline=True)
  embed.add_field(name="Git", value="Come help the bot! &Git", inline=True)
  embed.set_footer(text="Support the bot here: https://github.com/Noobyprogrammer/Devsearch-Discord-bot")
  await ctx.send(embed=embed)

@help.command()
async def devcommand(ctx):
  embed=discord.Embed(title="Dev", description="Search the documentation of various languages and applications.")
  embed.add_field(name="C++", value="C++ documentation", inline=True)
  embed.add_field(name="C#", value="C# documentation", inline=True)
  embed.add_field(name="Java", value="Java documentation", inline=True)
  embed.add_field(name="Python", value="Python documentation", inline=True)
  embed.add_field(name="Pascal", value="Pascal documentation", inline=True)
  embed.add_field(name="Xojo", value="Xojo documentation", inline=True)
  embed.add_field(name="Unity", value="Unity documentation", inline=True)
  embed.add_field(name="UE4", value="UE4 documentation", inline=True)
  embed.add_field(name="Discord", value="Discord documentation", inline=True)
  embed.add_field(name="Qiskit", value="Qiskit documentation", inline=True)
  embed.add_field(name="**Syntax**", value="&Dev <Programming language> [Keywords]", inline=False)
  embed.set_footer(text="Support the bot here: https://github.com/Noobyprogrammer/Devsearch-Discord-bot")
  await ctx.send(embed=embed)

@client.command()
async def dev(ctx, *, question=None): # Checks the documentation of a certain app/language
  # Lis le fichier json
  with open('docs_links.json', 'r') as f:
    docs_link = json.load(f)

  docname = question.split(" ")[0]

  try:
    docs_link[docname]
    await ctx.send('Here is some documentation: ' + docs_link[docname])
  except ValueError:
    await ctx.send(f'Request not understood.... try {client.command_prefix}help dev for commands')

@client.command()
async def stack(ctx, *, question=None): #StackOverflow questions
  if question == None or (question.split(" ")[0]) == "question": 
    await ctx.send("The request should be formulated like this: &stack 'question'")
  else:
    await ctx.send("WIP done here")

@client.command()
async def git(ctx): # Links back to the github page
  await ctx.send("Want to help the bot? Go here: https://github.com/Noobyprogrammer/Devsearch-Discord-bot")

"""
@client.command()
async def credits(ctx):
  await message.channel.send("Thanks to "+ <Persons who contributed to the github> + " for making this bot possible!")
"""

keep_alive() # Keeps the bot alive

client.run(os.getenv('TOKEN')) # Runs the bot with the private bot token