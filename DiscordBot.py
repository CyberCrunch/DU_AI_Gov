# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 15:53:27 2016

@author: robin
"""

#!/usr/bin/env python
#-*- coding: utf-8 -*-

from botinfo import *
from bs4 import BeautifulSoup as BS
from requests import get as re_get
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import EconomyManager
import MilitaryManager
import MemoryManager

def setupDiscord():
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
    !setd cityname, resource, amount -> sets a demand for resources
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
            output = MemoryManager.regHuman(msg)                    
            return await client.send_message(mobj.channel, output)
    
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
            return await client.send_message(mobj.channel, "Please use Format: !geodata name planet type longitude latitude")
        try: 
            return await client.send_message(mobj.channel, MemoryManager.regLocation(msg))
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
            return await client.send_message(mobj.channel, (EconomyManager.getJob(msg)))
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
            return await client.send_message(mobj.channel, EconomyManager.reportJob(msg))
        except Exception as ex:
            logger("Error: {}".format(ex))
        return await client.send_message(mobj.channel, "Error: bad input args")
    @register_command
    async def setd(msg, mobj):
        """
        Report on executed job
        Example: !setd location needs price
        """
        if msg == "":
            return await client.send_message(mobj.channel, "You didn't say anything!")
        try:
            return await client.send_message(mobj.channel, EconomyManager.setDemand(msg))
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
            return await client.send_message(mobj.channel, MemoryManager.getDatabase())
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
    run_the_bot(client, bot_name, logger)



