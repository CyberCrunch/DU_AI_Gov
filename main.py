#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
(pre alpha tech demo) AI Government of for Dual Universe organizations.
 Using Discord to communicate with the organization members.
Version: 0.02
(based on Dumb-bot by sleibrock)

Setup:
    create Discord ChatBot
    create Server.key file, with Discord Token
    install MongoDB (only for chatterbot usage)
    train chatterbot
    
TIPP: to install missing modules, go to IPython and type: !pip install xy
"""

import DiscordBot
import EnjinBot


if __name__ == "__main__":
    EnjinBot.setupEnjin()
    DiscordBot.setupDiscord()
