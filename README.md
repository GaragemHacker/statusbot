# statusbot
Clever Joke Bot to make the Garage more acessible in the web

### Anseios (to-do's)

 * Python Chatter Bot on IRC
 * HackerSpace Door status
 * Yowsup intergation
 * WebSite and Wiki hackerspace status

### status.php

Para passar o status do hackerspace como aberto, foi optado por usar o status.php que grava um arquivo status.txt com o estado do hackerspace. A requisicao e feito por um arduino com ethernet shield.

### statusbot.ino

Statusbot agora funciona com Arduino
 * Recebe DHCP
 * Imprime tudo que estiver colhendo em Serial
 * Aceita requisicoes ping
 * Faz UrlRequest

### ircbot.py

Chatter bot, para notificao de status com WhatsApp e IRC
 * Notificao de presenca no HackerSpace pelo IRC
 * Aviso da abertura para WhatsApp com integracao ao yowsup
 * Vocabulario atrevido de respostas
