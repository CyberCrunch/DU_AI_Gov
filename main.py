#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
AI Government for Dual Universe organizations.
 The purpose of this program is to assist DU-players by calculating
 governmental decisions based on the current situation in the game.
 To communicate with the organization members communication
 platforms (like Discord/TS3) are used.
Version: 0.03 (tech demo)
(based on Dumb-bot by sleibrock)

Setup Discord:
    create Discord ChatBot
    create Server.key file, with Discord Token
    install MongoDB (only for chatterbot usage)
    train chatterbot    
Setup Team Speak:
    (sometimes not supportet by soundcard) open audio settings
        setup virtual mic to take audio output as an input signal
    open dedicated TS3 client
    start TeamspeakBot
"""

from py_bots import DiscordBot
from py_bots import EnjinBot
from py_bots import TeamspeakBot

if __name__ == "__main__":
    #TeamspeakBot.setupTS()
    EnjinBot.setupEnjin()
    DiscordBot.setupDiscord()
