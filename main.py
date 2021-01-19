import discord #Discord libraries
import os
import json #Support for json files
from keepalive import keep_alive # imports the web server that pings the bot continually
from discord.ext import commands

client = discord.Client() # Connects to the discord client
client = commands.Bot(command_prefix = '&')
discord.ext.commands.Bot(command_prefix = '&', case_insensitive = True)
#client.removecommand("help")

docs_link = { 
"Unity" : "https://docs.unity3d.com/Manual/index.html",
"Python" : "https://docs.python.org/3/", 
"Xojo" : "http://docs.xojo.com/", 
"Java" : "https://docs.oracle.com/javase/8/docs/api/index.html?overview-summary.html",
"UE4" :  "https://docs.unrealengine.com/en-US/index.html",
"Unrealengine" :  "https://docs.unrealengine.com/en-US/index.html",
"C++" : "https://docs.microsoft.com/en-us/cpp/",
"C#" : "https://docs.microsoft.com/en-us/dotnet/csharp/",
"Discord" : "https://discord.com/developers/docs/intro",
"Pascal" : "https://www.freepascal.org/docs-html/3.0.0/prog/prog.html",
"idk" : "Then why did you asked? :thinking:",
"Cake": "The cake is not a lie.", # little secret hehehe
 } 


def load_json(): # Returns the dictionary in the specified json file
  with open('docs_links.json', 'r') as f:
    dictionary = json.load(f)

  return dictionary

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
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('A required argument is needed. Try &help to see required arguments.')
  
  await ctx.send('Error')

@client.command()
async def rtfm(ctx): # Brief intro to the bot
  await ctx.send('I am there to save you, ask me someting with &Dev <language type>!\nSearching for a topic on StackOverflow? Type &Stack <Question>!\nWant more commands? Type &Dev help!\nWant to help the bot? Type &Git!\nAnd thanks to all the ones that made this idea possible! Type &Credits!')

"""@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Devsearch", dscription = f'Use {client.command_prefix}Dev <Programing language> to use the bot')
  em.addfield(name="Dev", value="'C++', 'C#', 'Java'")
  
  await ctx.send(embed = em)
"""

@client.command()
async def dev(ctx, *, question=None): # Checks the documentation of a certain app/language
  #docs_link = load_json

  if any(word in question.split(" ")[0] for word in docs_link): # Finds the documentation to check in
    word = question.split(" ")[0]

    #tries to catch syntax errors in Discord????
    #if (word for word in docs_link):
    await ctx.send('Here is some documentation: ' + docs_link[word])
      
  elif (question.split(" ")[0] == "help"):
    await ctx.send("welp... you asked for help but i can only give you the satisfaction that devs are as clueless as you") 
    #we need to write documentation here but Idk what
    #All the commands formatted in a box
      
  else:
    # Be polite :)
    await ctx.send("Request not understood.... try '&dev help' for commands")

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