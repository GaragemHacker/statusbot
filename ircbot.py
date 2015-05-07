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
import select
import urllib
import socket
import time

#Global Vars
nick = 'rob0tn1ck' #define nick
passw = '????' #the password
ircsrv = "irc.freenode.net" #Define IRC Network
port = 6667 #Define IRC Server Port
chan = '#debugthisr0bot' #The IRC Channel
statefile = 'garagenow'
turnondebug = 'y' # y for show debug anithing else to no debug
leasetime = 7 * 60 # 7 minutos para espera de pings

########
#Begin functions
#######

#======= start ========
# * this function create connection socket and send signals to irc server like NICK,CHAN,JOIN, etc...
#irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #em testes AF_INET ipv4, STREAM
irc = socket.socket()
def connect():
    try:
        irc.connect((ircsrv,port)) #Connect to Server
        irc.recv (4096) #Setting up the Buffer
        irc.send('NICK ' + nick + '\r\n') #Send our Nick(Notice the Concatenation)
        irc.send('USER '+ nick + ' ' + nick + ' Bot: '+ nick + '\r\n') #send user info to the server
        irc.send('NICKSERV IDENTIFY ' + passw + '\r\n') #msg nickserv identify
        irc.send('JOIN ' + chan + '\r\n') #Join the channel
        irc.send('NOTICE ' + chan + ' :Oi eu sou o StatusBot da Garagem. Ainda estou em testes...\r\n') #send notice to the channel
        #irc.send('QUIT :Ill be back...') #my quit message
    except:
        print "Nao consegui conectar dessa vez ;( Vou tentar de novo"
        irc.send('QUIT :Ill be back...\r\n') #my quit message
        ok = irc.getsockname()
        print ok
        irc.socket.shutdown(ok)
        irc.socket.close(ok)
#======= status ========
# * this function make this bot say to the channel if the HackerSpace are open or closed
def status():
    try:
        garagestate = urllib.urlopen('http://garagemhacker.org/status.txt').read().rstrip()
        try:
            filenow = open(statefile, 'r')
            print 'Que bom!!! O arquivo',statefile,'ja existe, seguindo em frente...'
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
            filenow = open(statefile, 'w')
            filenow.write(garagestate)
            filenow = open(statefile, 'r')
            filenow.read()
            filenow.close()
            if garagestate == 'fechado':
                irc.send('PRIVMSG ' + chan + " :Heyyyy a garagem agora esta fechada!!!!!\r\n")
            else:
                irc.send('PRIVMSG ' + chan + " :Yuhuuuuu vamo la galera o HackerSpace esta ABERTO!!!! ;)\r\n")
    except:
            print "Ups... nao consegui resolver nesse, tento mais uma vez na proxima ;)"

#======= checkin ========
#*Verifica de tempo em tempo se recebeu um ping
def checkin():
#Este codigo deve ser melhorado com a funcao expira
    pingado = time.time()
    print 'Estou recebendo um ping em:',pingado
    if (time.time() - pingado) > leasetime:
        print 'Opa... nao recebi ping a mais de',leasetime,'entao vou recomecar o socket'
        irc.shutdown()
        irc.close()
        return True
    else:
        return False


#======= pongs ========
#* Antes de tudo, responda os pings dos servidores (funcao para mandar pongs)
def pongs():
    if data[0] == 'PING': #opa recebi um PING do server
        irc.send('PONG '+ data[1]+ '\r\n') #manda o pong
        #print data #somente para debug do pong

        checkin() #verify recived pings        
        status() #when recive the pong check for new state

#======= expira ========
#* se nao receber um ping em um periodo menor que o leastime definido, quebra o loop pra reconectar
#* Quebra e recomeca o socket se nao receber um ping do server no tempo do leasetime
#def expira():
#    if data[0] == 'PING':
        

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
        print "Recebi mensagem PVT de",voce(),"dizendo:",data[3:]
        irc.send('PRIVMSG '+voce()+" :Ola "+voce()+" ainda nao sei conversar, me chame quando eu me tornar mais social!\r\n")
    elif data[1] == 'PRIVMSG' and nick in data[3]: #se recebi uma mensagem pelo canal
        print voce(),"falou comigo pelo canal",chan,"e me disse:",data[3:]
        irc.send('PRIVMSG ' + chan + " :Oi "+voce()+". Eu ainda nao sei conversar... talvez outro dia eu lhe responda algo mais humano...\r\n")
        

#======= debug ========
#    * put all debug's you want on loop here ;)
def debug():

    #print data #Print the Data to the console(For debug purposes - HARD WAY TO READ)
    print "Socket data buffer em --> ",len(data)#enable to see Socket buffer size
    count = 0 #best way to read print data
    for linhas in data: #this is only util during debug and development of this bot
        print "imprimindo o valor: ",count, "de ",linhas
        count= count + 1
    print "###### FIM DA SESSAO ######", data[0]
    

#======= silent ========
#    * if debug is off silent function print silent messages to trace where bot stage are
def silent():
    
    if data[1] == 'JOIN' and voce() == nick:
        print "Beleza to dentro... entrei no canal",data[2]

    if data[1] == "001":
        print "Estou agora connectado em",data[0]
        print "Meu nick name é", nick

#======= killme ========
#    * kill this bot when you type KILL in bot prompt
def killme():
#im using this only for breaking the loop, just in case to exit this bot (3s to type KILL)
    print "Voce tem 3 segundos para responder!"
    i, o, e = select.select( [sys.stdin], [], [], 3 )
    if (i):
      if sys.stdin.readline().strip() == "KILL":
        print "Pra mim chega... fui..."
        return True
    else:
      print "Voce nao disse nada!"

########
#Begin of bot body
#######
while True:

    if killme(): #se killme retornar True saia do loop
        break

    try:
        connect()

        while True: #While Connection is Active
            data = irc.recv (4096) #Make Data the Receive Buffer
            if len(data) == 0: #se o recv for zero quebre este loop e comece de novo
                print "Xiii caiu!!!"
                irc.close()
                break

            #======= data split ======#
            # - used by mesgtome function and all function's using data as array
            data=data.split() #split all data make more easy to process my request's unfortunately little bit more slow ;|    

            #======= Bot Functions ======== # 
            #pongs()#first of all --> respond pings with this pong's
            if pongs():#respond pings and if leastime expires it sends a break to this loop
                break
            voice()#Gives voice mode to all new joiner's
            mesgtome()#Detect and reply messages to this bot
            if checkin():#checkin action and save time
                break
            #======= Debug's ======== #
            if turnondebug == 'y':
                debug()
            else:
                silent()
    except:
            print "Alguma coisa deu errado e falhei na conexao... vou reiniciar a conecao AGORA!"
            irc.send('PRIVMSG ' +chan+ ' :Ill be back...\r\n') #my quit message
            irc = socket.socket()
            continue
exit()


