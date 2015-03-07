#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import socket

#Global Vars
nick = 'StatusBotGH' #define nick
debug = True # For debug Mode
network = "irc.freenode.net" #Define IRC Network
port = 6667 #Define IRC Server Port
chan = '#garagemhacker' #The IRC Channel

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define  IRC Socket
irc.connect((network,port)) #Connect to Server
irc.recv (4096) #Setting up the Buffer
irc.send('NICK ' + nick + '\r\n') #Send our Nick(Notice the Concatenation)
irc.send('USER StatusBot StatusBot StatusBot :StatusBot\r\n') #Send User Info to the server
irc.send('JOIN ' + chan + '\r\n') # Join the pre defined channel
irc.send('PRIVMSG ' + chan + ' :Oi eu sou o StatusBot da Garagem. Ainda estou em testes...\r\n') #Send a Message to the  channel


while True: #While Connection is Active
    data = irc.recv (4096) #Make Data the Receive Buffer
    print data #Print the Data to the console(For debug purposes)
    
    if data.find(':'+nick+':') != -1:
        irc.send('PRIVMSG ' + chan + ' :Oi, alguem falou comigo. Eu ainda nao sei conversar... talvez outro dia eu lhe responda algo mais humano...\r\n')
    
    if data.find('PING') != -1: #If PING is Found in the Data
        print data.find
        irc.send('PONG ' + data.split()[1] + '\r\n') #Send back a PONG
