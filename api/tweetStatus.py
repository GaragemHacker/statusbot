#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    Notificador via Twitter
        Garagem Hacker { http://garagemhacker.org }
            - StatusBot { https://github.com/Garagem-Hacker/statusbot }

    Requisitos:
        Python Twitter - { https://github.com/bear/python-twitter }

    Uso:
        - Criar uma app no Twitter { https://apps.twitter.com/app }
        - Gerar as chaves de acesso { https://dev.twitter.com/oauth/overview/application-owner-access-tokens }
            -- Consumer Key (API Key), Consumer Secret (API Secret), Access Token, Access Token Secret
            -- Access Level: Read and write
        - Substituir as chaves XXXXX em "api"
'''

import urllib2, twitter
from time import sleep

def get_status(req):
    page = urllib2.urlopen(req)
    status = page.read()
    page.close()
    return status

def twitter_print_status(now):
    if now == "aberto\n":
        tweet = api.PostUpdate( "A Garagem Hacker está aberta" )
        print tweet.text
        
    elif now == "fechado\n":
        tweet = api.PostUpdate( "A Garagem Hacker está fechada" )
        print tweet.text
    else:
        print "status não identificado ", now


api = twitter.Api(  consumer_key = "XXXXX",
                    consumer_secret = "XXXXX",
                    access_token_key = "XXXXX",
                    access_token_secret = "XXXXX")

# req = urllib2.Request('http://localhost:8080', headers={'accept': '*/*'})
req = urllib2.Request('http://garagemhacker.org/status.txt', headers={'accept': '*/*'})

status_prev = get_status(req)

twitter_print_status(status_prev) # notificação inicial

while True:

    status = get_status(req)

    if status != status_prev:
        twitter_print_status(status)
        status_prev = status

    sleep(60) # 1 min