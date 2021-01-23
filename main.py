import discord #Discord libraries
import os
import json #Support for json files
from keepalive import keep_alive # imports the web server that pings the bot continually
from discord.ext import commands

def getprefix(client, message): # get the prefix of the current discord server that the bot is in
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = discord.Client() # Connects to the discord client
client = commands.Bot(command_prefix = getprefix)
#discord.ext.commands.Bot(command_prefix = get_prefix, case_insensitive = True)
client.remove_command("help") # Removes the default "help" function to replace it pby our own

@client.event #Callback to a unsychronous library of events
async def on_ready():
  # When the bot is ready to be used
  await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f'rtfm'))

  print('Logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild): # When the bot joins a new server
  # Loads the prefixes file
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = '&' # Default command prefix '&'

  # Saves the file
  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)
  
  await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f'{client.get_prefix}rtfm')) # Updates the activity of the bot

@client.event
async def on_guild_remove(guild): # When the bot leaves a server
    # Loads the prefixes file
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  prefixes.pop(str(guild.id)) # Deletes the server from the json list

  # Saves the file
  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)

@client.event
async def on_command_error(ctx, error):
  #Handles errors
  if isinstance(error, commands.CommandNotFound): # Command not found
    await ctx.send(f'Invalid command. Try {client.command_prefix}help to search for usable commands.')
  elif isinstance(error, commands.MissingRequiredArgument): # Manque d'arguments
    await ctx.send(f'A required argument is needed. Try {client.command_prefix}help to see required arguments.')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have the permission to do that.')
  else: # Erreurs non supporté pour le moment
    await ctx.send('Error not defined. Please report this issue at https://github.com/BBArikL/Devsearch-Discord-bot')

@client.command()
async def rtfm(ctx): # Brief intro to the bot
  await ctx.send(f'I am there to save you, ask me someting with {client.command_prefix}Dev <language type>!\nSearching for a topic on StackOverflow? Type {client.command_prefix}Stack <Question>!\nWant more commands? Type {client.command_prefix}Dev help!\nWant to help the bot? Type {client.command_prefix}Git!\nAnd thanks to all the ones that made this idea possible! Type {client.command_prefix}Credits!')

@client.group(invoke_without_command=True, case_insensitive = True)
async def help(ctx): # Custo Help command
  embed=discord.Embed(title="Devsearch", url="https://github.com/BBArikL/Devsearch-Discord-bot", description="Search into Application/Languages documentation and provides fast help to devs searching for solutions in their ideas.")
  embed.add_field(name="Dev", value=f"Use {client.command_prefix}Dev <language> to get information on links to the documentation. You can also add a keyword to precise your search! For supported documentations, use {client.command_prefix}help Dev.", inline=False)
  embed.add_field(name="Stack", value=f"Search for a question in stackoverflow with {client.command_prefix}Stack <Question>!", inline=True)
  embed.add_field(name="Git", value=f"Come help the bot! {client.command_prefix}Git", inline=True)
  embed.add_field(name="Changeprefix", value=f"Change the bot's prefix. Only persons with Manage Messages role can use this command. {client.command_prefix}ChangePrefix", inline=True)
  embed.set_footer(text="Support the bot here: https://github.com/BBArikL/Devsearch-Discord-bot")
  await ctx.send(embed=embed)

@help.command()
async def devcommand(ctx):
  # Lis le fichier json
  with open('docs_links.json', 'r') as f:
    docs_link = json.load(f)
  
  embed=discord.Embed(title="Dev", description="Search the documentation of various languages and applications.")

  for docname in docs_link: # Montre tout les documentations possibles
    embed.add_field(name=docname, value=docname+" documentation", inline=True)

  embed.add_field(name="**Syntax**", value=f"{client.command_prefix}Dev <Programming language> [Keywords]", inline=False)
  embed.set_footer(text="Support the bot here: https://github.com/BBArikL/Devsearch-Discord-bot")
  await ctx.send(embed=embed)

@client.command()
async def dev(ctx, *, question=None): # Checks the documentation of a certain app/language
  # Lis le fichier json
  with open('docs_links.json', 'r') as f:
    docs_link = json.load(f)

  docname = question.split(" ")[0]

  try: # Now the on_command_error() function works too much better, then the Try/Except block doesnt nearly do anything
    docs_link[docname]
    await ctx.send('Here is some documentation: ' + docs_link[docname])
  except ValueError:
    await ctx.send(f'Request not understood.... try {client.command_prefix}help dev for commands')

@client.command()
async def stack(ctx, *, question=None): #StackOverflow questions
  if question == None or (question.split(" ")[0]) == "question": 
    await ctx.send(f"The request should be formulated like this: {client.command_prefix}stack 'question'")
  else:
    await ctx.send("WIP done here")

@client.command()
async def git(ctx): # Links back to the github page
  await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/Devsearch-Discord-bot")

@client.command()
@commands.has_permissions(manage_messages=True) # Only mods can change the bot's prefix
async def ChangePrefix(ctx, prefix): #Changes the preprefix of the server
  # Loads the prefixes file
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  prefixes[str(ctx.guild.id)] = prefix # Default command prefix '&'

  # Saves the file
  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)
  
  await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f'{client.command_prefix}rtfm')) #Update Bot's activity

  await ctx.send(f'Prefix changed to : {prefix}')

"""
@client.command()
async def credits(ctx):
  await message.channel.send("Thanks to "+ <Persons who contributed to the github> + " for making this bot possible!")
"""

keep_alive() # Keeps the bot alive

client.run(os.getenv('TOKEN')) # Runs the bot with the private bot token