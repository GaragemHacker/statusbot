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
from time import sleep

#Global Vars
nick = 'botnick' #define nick
passw = '????' #the password
debug = True # For debug Mode
ircsrv = "irc.freenode.net" #Define IRC Network
port = 6667 #Define IRC Server Port
chan = '#debugthisr0bot' #The IRC Channel
statefile = 'garagenow'

########
#Begin functions
#######

#======= connect ========
# * this function create connection socket and send signals to irc server like NICK,CHAN,JOIN, etc...
#irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #em testes AF_INET ipv4, STREAM
irc = socket.socket()
def connect():
    irc.connect((ircsrv,port)) #Connect to Server
    irc.recv (4096) #Setting up the Buffer
    irc.send('NICK ' + nick + '\r\n') #Send our Nick(Notice the Concatenation)
    irc.send('USER '+ nick + ' ' + nick + ' Bot: '+ nick + '\r\n') #send user info to the server
    irc.send('NICKSERV IDENTIFY ' + passw + '\r\n') #msg nickserv identify
    irc.send('JOIN ' + chan + '\r\n') #Join the channel
    irc.send('NOTICE ' + chan + ' :Oi eu sou o StatusBot da Garagem. Ainda estou em testes...\r\n') #send notice to the channel
    #irc.send('QUIT :Ill be back...') #my quit message


#======= status ========
# * this function make this bot say to the channel if the HackerSpace are open or closed
def status():
    
    garagestate = urllib.urlopen('http://garagemhacker.org/status.txt').read().rstrip()
    try:
        print 'Arquivo ok'
        filenow = open(statefile, 'r')
    except:
        print 'Essa eh minha primeira vez, vou criar um arquivo novo'
        filenow = open(statefile, 'a')
        filenow.write(garagestate)
        filenow = open(statefile, 'r')
    if filenow.read() == garagestate:
        print 'A garagem ainda esta', garagestate, 'nao mudarei nada', filenow.read()
        filenow.close()
    else:
        print 'A garagem agora esta', garagestate, 'vou salvar o novo status'
        filenow.close()
        filenow = open(statefile, 'w')
        filenow.write(garagestate)
        filenow = open(statefile, 'r')
        filenow.read()
        filenow.close()
        if garagestate == 'fechado':
            irc.send('PRIVMSG ' + chan + " :Heyyyy a garagem agora esta fechada!!!!!\r\n")
        else:
            irc.send('PRIVMSG ' + chan + " :Yuhuuuuu vamo la galera o HackerSpace esta ABERTO!!!! ;)\r\n")

#======= pongs ========
#* Antes de tudo, responda os pings dos servidores (funcao para mandar pongs)
def pongs():
    if data[0] == 'PING': #opa recebi um PING do server
        irc.send('PONG '+ data[1]+ '\r\n') #manda o pong
        #print data #somente para debug do pong
        status() #when recive the pong check for new state

#======= voce ========
# * this functions discover who you are
def voce():
    prenick = data[0].find(':')
    posnick = data[0].find('!',prenick)
    youare = data[0][prenick+1:posnick]
    return youare;

#======= voice ========
#    * this function auto voice new joiner's
def voice():
    if data[1] == 'JOIN':
        irc.send('MODE ' +chan+ ' +v: '+voce()+ '\r\n')#give voices to new joins

#======= mesgtome ========
#    * if someone talk to me i will do this code
def mesgtome():
    #Encontrar mensagens enviadas a mim
    if data[1] == 'PRIVMSG' and data[2] == nick: #se recebi uma mensagem pvt
        print "Recebi mensagem PVT de",voce()
        irc.send('PRIVMSG '+voce()+" :Ola "+voce()+" ainda nao sei conversar, me chame quando eu me tornar mais social!\r\n")
    elif data[1] == 'PRIVMSG' and nick in data[3]: #se recebi uma mensagem pelo canal
        print "Falaram comigo pelo canal: ",data[2]
        irc.send('PRIVMSG ' + chan + " :Oi "+voce()+". Eu ainda nao sei conversar... talvez outro dia eu lhe responda algo mais humano...\r\n")
        

#======= debug ========
#    * put all debug's you want on loop here ;)
def debug():
    #print data #Print the Data to the console(For debug purposes - HARD WAY TO READ)
    count = 0 #best way to read print data
    for linhas in data: #this is only util during debug and development of this bot
        print "imprimindo o valor: ",count, "de ",linhas
        count= count + 1
    print "###### FIM DA SESSAO ######", data[0]    

########
#Begin of bot body
#######
while True:

    connect()#inicia a conecao e autenticao

    while True: #While Connection is Active
        data = irc.recv (4096) #Make Data the Receive Buffer
        print "Socket data buffer em --> "+str(len(data))
        if len(data) == 0: #se o recv for zero quebre este loop e comece de novo
            print "Xiii caiu!!!"
            break   
    
        #======= data split ======#
        # - used by mesgtome function
        data=data.split() #split all data make more easy to process my request's unfortunately little bit more slow ;|    

        #======= Bot Functions ======== # 
        pongs()#first of all --> respond pings with this pong's
        voice()#Gives voice mode to all new joiner's
        mesgtome()#Detect and reply messages to this bot

        #======= Debug's ======== #   
        debug()

