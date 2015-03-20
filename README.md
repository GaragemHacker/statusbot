# statusbot
Clever Joke Bot to make the Garage more acessible in the web

### Task's (to-do's)

 * Python Chatter Bot on IRC
 * HackerSpace Door status
 * Yowsup intergation
 * WebSite and Wiki hackerspace status

### status.php

Para passar o status do hackerspace como aberto, foi optado por usar o status.php que grava um arquivo status.txt com o estado do hackerspace. A requisicao e feito por um arduino com ethernet shield.

-------

### statusbot(turnkey/push).ino

Statusbot task's com Arduino
 - [x] Receber DHCP
 - [x] Imprimir tudo que estiver colhendo em Serial
 - [x] Aceitar requisicoes ping
 - [x] Fazer UrlRequest <i>(quando o estado se alterar)</i>
 - [ ] Twittar Status

Estou deixando para estudo de caso duas versões diferentes para arduino.
A versao <i>"turnkey"</i> usa a interrupcao como leitura e pode ser usado com botoes tradicionais tipo switch. O arquivo statusbot_push.ino tem um algoritimo que ira funcionar com botoes <i>"push"</i>. 

#### Exemplos de botoes
<img src="https://github.com/Garagem-Hacker/statusbot/blob/master/img/switch-button.jpg" />  | <img src="https://github.com/Garagem-Hacker/statusbot/blob/master/img/push-button.jpg" />
------------- | -------------
<i>Switch Gangorra</i>  | <i>Push button</i>

-------

### ircbot.py

Chatter bot, para notificao de status com WhatsApp e IRC
 * Notificao de presenca no HackerSpace pelo IRC
 * Aviso da abertura para WhatsApp com integracao ao yowsup
 * Vocabulario atrevido de respostas


-------

### lamp.js (<i>lamp_sample.html</i>)
Pequeno exemplo de como usar a API para colher o estado da garagem.
Este exemplo usa um javascript que colhe o estado do arquivo status.txt e quando aberto mostra uma lampada acesa no html. Quando apagado mostra uma lampada apagada.

<img src="https://github.com/Garagem-Hacker/statusbot/blob/master/img/lamp.png" /><br>
<i>Lampada usada no site da <a href="http://www.garagemhacker.org">garagemhacker</a></i>

