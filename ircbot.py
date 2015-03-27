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
import sys
import urllib
import socket

#Global Vars
NICK = 'botnick' #define nick
PASS = '????' #the password
DEBUG = True # For debug Mode
NETWORK = "irc.freenode.net" #Define IRC Network
PORT = 6667 #Define IRC Server Port
CHAN = '#debugthisr0bot' #The IRC Channel
GARAGESTATE= urllib.urlopen('http://garagemhacker.org/status.txt').read().rstrip()
STATEFILE = 'garagenow'
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
#irc.send('QUIT :Ill be back...') #my quit message

########
#Begin functions
#######
def status():
    try:
        print 'Arquivo ok'
        filenow = open(STATEFILE, 'r')
    except:
        print 'Essa eh minha primeira vez, vou criar um arquivo novo'
        filenow = open(STATEFILE, 'a')
        filenow.write(GARAGESTATE)
        filenow = open(STATEFILE, 'r')
    if filenow.read() == GARAGESTATE:
        print 'A garagem ainda esta', GARAGESTATE, 'nao mudarei nada', filenow.read()
        filenow.close()
    else:
        print 'A garagem agora esta', GARAGESTATE, 'vou salvar o novo status'
        filenow.close()
        filenow = open(STATEFILE, 'w')
        filenow.write(GARAGESTATE)
        filenow = open(STATEFILE, 'r')
        filenow.read()
        filenow.close()
        if GARAGESTATE == 'fechado':
            irc.send('PRIVMSG ' + CHAN + " :Heyyyy a garagem agora esta fechada!!!!!\r\n")
        else:
            irc.send('PRIVMSG ' + CHAN + " :Yuhuuuuu vamo la galera o HackerSpace esta ABERTO!!!! ;)\r\n")


def pongs():#Antes de tudo, responda os pings dos servidores
    if data[0] == 'PING': #opa recebi um PING do server
        irc.send('PONG '+ data[1]+ '\r\n') #manda o pong
        #print data #somente para debug do pong
        #status() #when recive the pong check for new state


def voce():
    prenick = data[0].find(':')
    posnick = data[0].find('!',prenick)
    youare = data[0][prenick+1:posnick]
    return youare;




########
#Begin of bot body
#######

while True: #While Connection is Active
    data = irc.recv (4096) #Make Data the Receive Buffer
    #print data #Print the Data to the console(For debug purposes)
    data=data.split() #split all data make more easy to process my request's unfortunately little bit more slow ;|    
    pongs()
    status()

    count = 0
    for linhas in data: #this for is only util during debug and development od this bot
        print "imprimindo o valor: ",count, "de ",linhas
        count= count + 1
    
   
     
    #Encontrar mensagens enviadas a mim
    if data[1] == 'PRIVMSG' and data[2] == NICK: #se recebi uma mensagem pvt
        print 'Opa achei uma mensagem PVT pra mim'
        print "Recebi mensagem de",voce()
        irc.send('PRIVMSG '+voce()+" :Ola "+voce()+" ainda nao sei conversar, me chame quando eu me tornar mais social!\r\n")
    elif data[1] == 'PRIVMSG' and NICK in data[3]: #se recebi uma mensagem pelo canal
        print "Falaram comigo pelo canal: ",data[2]
        irc.send('PRIVMSG ' + CHAN + " :Oi "+voce()+". Eu ainda nao sei conversar... talvez outro dia eu lhe responda algo mais humano...\r\n")
        
