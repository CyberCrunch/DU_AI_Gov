#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
(pre alpha tech demo) AI Government of for Dual Universe organizations. Using Discord
to communicate with the organization members.
Version: 0.01
(based on Dumb-bot by sleibrock)

Setup:
    create Discort ChatBot
    create Server.key file, with Discort Token
    install MongoDB
    train chatterbot
    
TIPP: to install missing modules, go to IPython and type: !pip install xy
"""

from botinfo import *
from bs4 import BeautifulSoup as BS
from requests import get as re_get
import json
import machine_learning_test
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

###############################INITIALIZE_CHATTERBOT###########################
chatterbot = ChatBot('DiscordChatter', #please comment out if MongoDB not installed
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputFormatAdapter",
    output_format='text',
    database='chatterbot-database',
    #trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
###Train ChatBot before first usage!
#chatterbot.set_trainer(ChatterBotCorpusTrainer)
#chatterbot.train("chatterbot.corpus.english")
###############################################################################

help_msg = """
The Discord Bot Project
https://github.com/sleibrock/discord-bots

Command reference
https://github.com/sleibrock/discord-bots/blob/master/docs/bot-command-guide.md
"""

bot_name = "AI_Gov"
client = discord.Client()
logger = create_logger(bot_name)

@register_command
async def howto(msg, mobj):
    """
    Return a help message
    If you came here from !howto help; there's nothing else, sorry
    """
    return await client.send_message(mobj.channel, pre_text(help_msg))

@register_command
async def rtd(msg, mobj):
    """
    Roll a d<N> di[c]e <X> number of times
    Example: !rtd 2d10 - rolls two d10 dice
    """
    if msg == "":
        return await client.send_message(mobj.channel, "You didn't say anything!")
    try:
        times, sides = list(map(int, msg.lower().split("d")))
        res = [randint(1, sides) for x in range(times)]
        return await client.send_message(mobj.channel, ", ".join(map(str, res)))
    except Exception as ex:
        logger("Error: {}".format(ex))
    return await client.send_message(mobj.channel, "Error: bad input args")

@register_command
async def ddg(msg, mobj):
    """
    Search DuckDuckGo and post the first result
    Example: !ddg let me google that for you
    """
    try:
        if msg == "":
            return await client.send_message(mobj.channel, "You didn't search for anything!")
        msg.replace(" ", "%20") # replace spaces
        url = "https://duckduckgo.com/html/?q={0}".format(msg)
        bs = BS(re_get(url).text, "html.parser")
        results = bs.find_all("div", class_="web-result")
        if not results:
            return await client.send_message(mobj.channel, "Couldn't find anything")
        a = results[0].find("a", class_="result__a")
        title, link = a.text, a["href"]
        return await client.send_message(mobj.channel, "{} - {}".format(title, link))
    except Exception as ex:
        logger("Fail: {}".format(ex))
    return await client.send_message(mobj.channel, "Failed to get the search")

@register_command
async def yt(msg, mobj):
    """
    Do a youtube search and yield the first result
    Example: !yt how do I take a screenshot
    """
    try:
        if msg == "":
            return await client.send_message(mobj.channel, "You didn't search for anything!")
        msg.replace(" ", "+")
        url = "https://www.youtube.com/results?search_query={}".format(msg)
        bs = BS(re_get(url).text, "html.parser")
        items = bs.find("div", id="results").find_all("div", class_="yt-lockup-content")
        if not items:
            return await client.send_message(mobj.channel, "Couldn't find any results")

        # Search for a proper youtube url, has to start with /watch
        # TODO: rewrite this with a list comp/filter
        i, found = 0, False
        while not found and i < 20:
            href = items[i].find("a", class_="yt-uix-sessionlink")["href"]
            if href.startswith("/watch"):
                found = True
            i += 1
        if not found:
            return await client.send_message(mobj.channel, "Couldn't find a link")
        return await client.send_message(mobj.channel, "https://youtube.com{}".format(href))
    except Exception as ex:
        logger("Fail: {}".format(ex))
    return await client.send_message(mobj.channel, "Failed to request the search")


################################DEFINE_AI_Commands#############################
@register_command
async def help(msg, mobj):
    """
    displays possible commands
    Example: !regPOI name, planet, type, coordinateX, coordinateY, coordinateZ
    """
    return await client.send_message(mobj.channel, pre_text("""
Commands:
!help -> displays possible commands.
!reg name, preferedJob -> registers new user in the database.
!geodata name, planet, type, longitude, latitude -> registers new location in the database
!getj name -> find suitable Job to execute
!repj name success -> Report on executed job 
!chat Greetings! -> Do some smalltalk with a default python-chatterbot
"""))
  
@register_command
async def reg(msg, mobj):
    """
    registers new user in the database
    Example: !reg name, preferedJob
    """
    if msg == "":
        return await client.send_message(mobj.channel, "Please use Format: !reg 'name job'")
    try: 
        splitStr = msg.split()
        if(len(splitStr) != 2):
            return await client.send_message(mobj.channel, "Invalid Parameters, please use Format: !reg 'name job'")
        with open('memoryDB.json', 'r+') as json_file:
            json_data = json.load(json_file)
            json_data[splitStr[0]] = ['Human', splitStr[1],"idle", "unknownPos", 0]
            json_file.seek(0, 0)
            json_file.write(json.dumps(json_data, indent=4))
            json_file.truncate()
                
        return await client.send_message(mobj.channel, ("New human registered: " +msg))

    except Exception:
        raise IOError("Error: IO exeption")
    return await client.send_message(mobj.channel, "Error: bad input args")
    
@register_command
async def geodata(msg, mobj):
    """
    registers new location in the database
    Example: !geodata name planet type longitude latitude
    """
    if msg == "":
        return await client.send_message(mobj.channel, "Please use Format: !reg 'name job'")
    try: 
        splitStr = msg.split()
        if(len(splitStr) != 5):
            return await client.send_message(mobj.channel, "Invalid Parameters, please use Format: !reg 'name job'")
        with open('memoryDB.json', 'r+') as json_file:
            json_data = json.load(json_file)
            json_data[splitStr[0]] = ['Location', splitStr[1], splitStr[2], splitStr[3], splitStr[4]]
            json_file.seek(0, 0)
            json_file.write(json.dumps(json_data, indent=4))
            json_file.truncate()
        return await client.send_message(mobj.channel, ("New location registered: " +msg))
    except Exception:
        raise IOError("Error: IO exeption")
    return await client.send_message(mobj.channel, "Error: bad input args")
   
@register_command
async def getj(msg, mobj):
    """
    find suitable Job to execute
    Example: !getj name
    """
    if msg == "":
        return await client.send_message(mobj.channel, "You didn't say anything!")
    try:
        with open('memoryDB.json', 'r+') as json_file:
            json_data = json.load(json_file)
            job = json_data[msg][1]
            EvaluateResources = "[placeholder]" #placeholder... every job should be calculated in his own class...
            if(job == "Miner"):
                json_data[msg][2] = "working"
                json_data[msg][3] = "Sector A3"
                output = "You are now assigned to Sector A3 for mining" + EvaluateResources + " Minerals. You will receave "+EvaluateResources+" Credits if successfull."
            elif(job == "Builder"):
                json_data[msg][2] = "working"
                json_data[msg][3] = "Sector C8"
                output = "You are now assigned to Sector C8 for building an automatic defence turret. You will receave "+EvaluateResources+" Credits if successfull."
            else:
                output = "There are currently no jobs available for your profession, please enjoy the game now."
            json_file.seek(0, 0)
            json_file.write(json.dumps(json_data, indent=4))
            json_file.truncate()
        return await client.send_message(mobj.channel, (output))
    except Exception as ex:
        logger("Error: {}".format(ex))
    return await client.send_message(mobj.channel, "Error: bad input args")
    
@register_command
async def repj(msg, mobj):
    """
    Report on executed job
    Example: !repj yourName success
    """
    if msg == "":
        return await client.send_message(mobj.channel, "You didn't say anything!")
    try:
        splitStr = msg.split()
        if(len(splitStr) != 2):
            return await client.send_message(mobj.channel, "Invalid Parameters, please use Format: !repj 'name statusreport'")
        if(splitStr[1] == "success"):
            fakeMoney = machine_learning_test.tensorflow_test() #placeholder
            with open('memoryDB.json', 'r+') as json_file:
                json_data = json.load(json_file)
                json_data[splitStr[0]][2] = "idle"
                json_data[splitStr[0]][3] = "unknownPos"
                json_data[splitStr[0]][4] = json_data[splitStr[0]][4] + int(fakeMoney[0]*1000)   #str(int(json_data[msg][4]) + 9000)
                json_file.seek(0, 0)
                json_file.write(json.dumps(json_data, indent=4))
                json_file.truncate()
            return await client.send_message(mobj.channel, ("Thanks for your contribution. Your earned " + str(int(fakeMoney[0]*1000)) + " credits"))
        return await client.send_message(mobj.channel, ("Your report will be analyzed.")) #placeholder!

    except Exception as ex:
        logger("Error: {}".format(ex))
    return await client.send_message(mobj.channel, "Error: bad input args")

@register_command
async def secret_debug_command(msg, mobj):
    """
    secret function to view behind the curtain
    (prints complete json database for debug puropses)
    """
    try:
        with open('memoryDB.json', 'r') as json_file:
            json_data = json.load(json_file)
            formatted = json.dumps(json_data, indent=4, sort_keys=True)
        return await client.send_message(mobj.channel, formatted)
    except Exception as ex:
        logger("Error: {}".format(ex))
    return await client.send_message(mobj.channel, "Error: bad input args")
    
@register_command
async def chat(msg, mobj):
    """
    Do some smalltalk with a default python-chatterbot
    Example: !chat Greetings!
    """
    if msg == "":
        return await client.send_message(mobj.channel, "You didn't say anything!")

    bot_input = chatterbot.get_response(msg)
    return await client.send_message(mobj.channel, (bot_input))
###############################################################################

# Last step - register events then run
setup_all_events(client, bot_name, logger)
if __name__ == "__main__":
    
    run_the_bot(client, bot_name, logger)
# end


