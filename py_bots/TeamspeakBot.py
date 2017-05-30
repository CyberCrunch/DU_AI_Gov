# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:13:02 2017

@author: robin
"""

import telnetlib
import time
import re
from gtts import gTTS
import os

import webbrowser
from py_controls import RSS_reader


def waitForMsg(tn):
    toStr =r"b''"
    while (r"b''"==toStr):
        toStr = str(tn.read_eager())
        time.sleep(1)
    
    toStr = toStr + str(tn.read_eager()) +  str(tn.read_eager()) +  str(tn.read_eager())
    toStr = toStr.replace("'b'", "")
    toStr = toStr.replace("\\\s", " ")

    searchObj = re.search( r'(.*)msg=(.*) target=(.*) invokerid=(.*) invokername=(.*?) .*', toStr, re.M|re.I)
    
    if searchObj:
        print ("searchObj.group() : ", searchObj.group())
        print ("searchObj.group(1) : ", searchObj.group(1))
        print ("searchObj.group(2) : ", searchObj.group(2))
        print ("searchObj.group(3) : ", searchObj.group(3))
        print ("searchObj.group(4) : ", searchObj.group(4))
        print ("searchObj.group(5) : ", searchObj.group(5))
    
        answerMsg= searchObj.group(2)
        answerId= searchObj.group(4)
        answerName= searchObj.group(5)
    else:
        print ("Nothing found!!")
    return {'answerMsg':answerMsg, 'answerId':answerId ,'answerName':answerName }

def processCommands(tn):
    while True:
        MsgDict=waitForMsg(tn)   
        print(tn.read_eager())

        if(MsgDict['answerMsg'] == r"shutdown"): #end loop
            break;
        if(MsgDict['answerMsg'] == r"Sing a Song"):
            webbrowser.open("db_tts\\DaisyBell.mp3")
        if(MsgDict['answerMsg'] == r"Tell me about Dual Universe"):
            readDualLore()
        if(MsgDict['answerMsg'] == r"rss"):
            print(RSS_reader.getRSSupdates('vulture announcements', 'http://www.vulturecorporation.com/forum/m/20530240/op/rss/forum_id/3849083'))
        else:
            readGivenText((' '+ str(MsgDict['answerMsg'])), lang='en')
            

            
def readGivenText(text):
    tts = gTTS(text, lang='en')
    tts.save("db_tts\\ttsSynthesis.mp3")
    webbrowser.open("db_tts\\ttsSynthesis.mp3")    #tts.save(os.path.join('.\AI_Gov', "ttsSynthesis.mp3"))
def readDualLore():
    webbrowser.open("db_tts\\DUlore.mp3")
    
def setupTS():

    readMsg= "clientnotifyregister schandlerid=0 event=notifytextmessage"

#Possible telnet commands:
#    cmd1 = "sendtextmessage targetmode=2 msg=SPAM"
#    cmd2 = "clientpoke msg=Wake\sup! clid=zmc89MzqjbZFv8GPCBpq3aWK1iQ="
#    cmd3 = "messageadd cluid=5 subject=Hi! message=Hello?!?"
  
    tn = telnetlib.Telnet("localhost",25639)
    time.sleep(1)
    print(tn.read_eager())
    print(tn.read_eager())
    print(tn.read_eager())
    print(tn.read_eager())
    tn.write(readMsg.encode('ascii') + b"\n")
    print(tn.read_eager())
    print(tn.read_eager())
    print(tn.read_eager())
    MsgDict=waitForMsg(tn)   

    print(tn.read_eager())
    
    readGivenText(('Welcome '+ str(MsgDict['answerName']) + '! I am your personal AI assistant. How can I help you?'), lang='en')
    time.sleep(2) #Wait for saying Hi.
    
    welcomeMsg = ("sendtextmessage targetmode=2 msg=New\sUser\sdetected:\sWelcome\s"+MsgDict['answerName'])
    tn.write(welcomeMsg.encode('ascii') + b"\n")
    print(tn.read_eager())
    time.sleep(2)
    print(tn.read_eager())
    print(tn.read_eager())
    print(tn.read_eager())
    print(tn.read_eager())
        
    processCommands(tn) #wait for shutdown

    tn.close()
    readGivenText('I am going offline, have a nice day!')
    
if __name__ == "__main__":
    #testing Text to Speech
    fileInput = open("db_tts\\tts.txt").readlines()
    text=(' '.join(fileInput))
    readGivenText(text)
    #readGivenText('I am going offline, have a nice day!')
