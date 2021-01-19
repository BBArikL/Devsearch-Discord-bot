import discord #Discord libraries
import os
import requests # Allows HTTP requests
import json
from keepalive import keep_alive # imports the web server that pings the bot continually
#from discord.ext import commands

client = discord.Client() # Connects to the discord client
#client = commands.Bot(command_prefix = "&")

# Lists of Docs and docs link
#documentations = ["Unity", "Python", "Xojo", "Java", "UE4", "C++","C#","Discord","...."] Not used anymore lol

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
"Quiskit" : "https://qiskit.org/documentation/",
"idk" : "Then why did you asked? :thinking:",
"Cake": "The cake is not a lie.", # little secret hehehe
}

#in a perfect world, add a keyword search function in each page...
def get_quote():
  response = requests.get("https://zenquotes.io/api/random") # Get the page
  json_data = json.loads(response.text) # Converts it to json data
  quote = json_data[0]['q'] + " -" + json_data[0]['a'] # Search in the json data and extracts the quote + authors name
  return quote

# The function down below fucked up a little bit so imma let it there for now
def format_txt(message):
  # Will take the text, format it, then transfer it to be interpreted, will then ask a connection to the documentation website we want to search in, search the documentation and then reprints the links found formatted
  print('Blob')
  return '<Formatted text>'

@client.event #Callback to a unsychronous library of events
async def on_ready():
  # When the bot is ready to be used
  await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='rtfm'))

  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
# Each time a message is sent
  if message.author == client.user:
    return # Does Nothing if the message is sent by itself
  
  msg = message.content.lower() # The content of the message sent previously, in lower case

  if msg.startswith('&dev'):
    # Command : '&Devsearch ....'
    
    # Funneh quote hehehe
    # quote = get_quote()
    # await message.channel.send(quote) # Returns a message to be sent by the bot

    if any(word in msg for word in docs_link):
      word = msg.split(" ")
      await message.channel.send('Here is some documentation: ' + docs_link[word[1]])
  #check every message 

  elif msg.find("rtfm") != -1: 
    await message.channel.send('I am there to save you, ask me someting with &Dev <language type>!\nSearching for a topic on StackOverflow? Type &Stack <Question>!\nWant to help the bot? Type &Git!\nAnd thanks to all the ones that made this idea possible! Type &Credits!')

  elif msg.startswith("&git"):
    await message.channel.send("Want to help the bot? Go here: https://github.com/Noobyprogrammer/Devsearch-Discord-bot")
  elif msg.startswith("&stack"):

    if len(msg) != 6:
      await message.channel.send("WIP done here")
    else:
      await message.channel.send("The request should be formulated like this: &stack 'question'")
    
keep_alive()

client.run(os.getenv('TOKEN')) # Runs the bot with the private bot token