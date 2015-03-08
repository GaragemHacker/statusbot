#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
By: isca
Curitiba/PR - 08/03/2015

                IRC STATUSBOT (lablabot)

This is the GaragemHacker Curitiba HackerSpace - StatusBot

    This bot must do this things:

        * Say to IRC Channel the HackerSpace status. (if it's open or closed)
        * Respond PING's to the irc serv to stay a live
        * Get OP Mode
        * Give voice to all connects and new arrives nicks on channel
        * Talk a litte bit with user's in the channel (in joke way mode)
        
    if a little more thinks come's in head we insert in the bot update

more docs:
        https://tools.ietf.org/html/rfc1459 --> IRC RFC, muito util, especialmente pelos IRC SIGNAL'S (NICK,JOIN etc...)
        http://garagemhacker.org/wiki/doku.php/projetos/todos/statusbot.txt
"""

import socket

#Global Vars
NICK = 'r0bot' #define nick
PASS = '?????' #the password
DEBUG = True # For debug Mode
NETWORK = "irc.freenode.net" #Define IRC Network
PORT = 6667 #Define IRC Server Port
CHAN = '#garagemhacker' #The IRC Channel

########
#Begin of server signals
#######
#irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #em testes AF_INET ipv4, STREAM
irc = socket.socket()
irc.connect((NETWORK,PORT)) #Connect to Server
irc.recv (4096) #Setting up the Buffer
irc.send('NICK ' + NICK + '\r\n') #Send our Nick(Notice the Concatenation)
irc.send('USER '+ NICK + ' ' + NICK + ' Bot: '+ NICK + '\r\n') #send user info to the server
irc.send('NICKSERV IDENTIFY ' + PASS + '\r\n') #msg nickserv identify
irc.send('JOIN ' + CHAN + '\r\n') #Join the channel
irc.send('NOTICE ' + CHAN + ' :Oi eu sou o StatusBot da Garagem. Ainda estou em testes...\r\n') #send notice to the channel
#irc.send('QUIT ' + CHAN + ': Ill be back') #my quit message


########
#Begin of bot body
#######
while True: #While Connection is Active
    data = irc.recv (4096) #Make Data the Receive Buffer
    print data #Print the Data to the console(For debug purposes)
    
    #Antes de tudo, responda os pings dos servidores
    if data.find('PING') != -1: #If PING is Found in the Data
        print data.find
        irc.send('PONG ' + data.split()[1] + '\r\n') #Send back a PONG
    
    #Inicio das piadas
    if data.find(':'+NICK+':') != -1:
        irc.send('PRIVMSG ' + CHAN + ''' :Oi, alguem falou comigo. 
        Eu ainda nao sei conversar... talvez outro dia eu lhe responda algo mais humano...\r\n''')
        
