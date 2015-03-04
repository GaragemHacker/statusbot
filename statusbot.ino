//GaragemHacker - StatusBot
/*
--> babysteps desse projeto
Objetivo: Requisiatar uma pagina web usando metodo get para
inidicar se o hackerspace esta aberto ou fechado.

- Arduino Ethercard ENC28J60 https://github.com/jcw/ethercard
- Este bot deve usar DHCP com MAC Amarrado ao nosso servidor local
- Caso conectemos via serial ele deve ecoar todos os parametros que ele possui
- Pode receber pings para mostar que esta vivo
- Se o status do botao ligado deve requisitar a pagina para abrir
- Se o status do botao for desligado deve requisitar a pagina para fechar

*/

//Incluindo a lib Ethercard --> https://github.com/jcw/ethercard/archive/master.zip
#include <EtherCard.h>

//Iniciando o ethernet shield com o mac abaixo
static byte mymac[] = { 0x74,0x69,0x69,0x2D,0x30,0x31 };
byte Ethernet::buffer[700];
static uint32_t timer;

//quem vou disparar o acesso
const char website[] PROGMEM = "garagemhacker.org";
static void look(){
  //condicional para fazer o dnslookup para trazer o callback da requisicao
  if (!ether.dnsLookup(website))
    Serial.println(F("DNS failed"));    
    ether.printIp(F("SRV: "), ether.hisip);
}

//funcao de callback - retorna a pagina que foi requisitada
static void get_callback(byte status, word off, word len) {
  Serial.println(F(">>>"));
  Ethernet::buffer[off+300] = 0;
  Serial.print((const char*) Ethernet::buffer + off);
  Serial.println(F("..."));
}


//funcao pra ecoar de quem esta me pingando
static void pingado (byte* ptr) {
  ether.printIp(">>>fui pingado por: ", ptr);
   timer = -9999999; // start timing out right away
  Serial.println();
}

//Esta funcao para iniciarmos o DHCP
static void dhcp() {
  if (ether.begin(sizeof Ethernet::buffer, mymac) == 0)
    Serial.println(F("Failed to access Ethernet controller"));
  if (!ether.dhcpSetup())
    Serial.println(F("DHCP failed"));

//Inicio dos ecos em serial de todos os dados que a placa tiver
//pequeno loop pra mostar o MAC ADRESS
  Serial.print("MAC: ");
  for (byte i=0;i<6;i++){
    Serial.print(mymac[i], HEX);
    if (i == 5){Serial.println();break;}
    Serial.print(":");
  }
  ether.printIp("IP:  ", ether.myip); //imprimindo o ip
  ether.printIp("Mask: ", ether.netmask); //mascara de subrede
  ether.printIp("GW:  ", ether.gwip); //gateway
  ether.printIp("DNS:  ", ether.dnsip); //dns
  ether.printIp("BROADCAST:  ", ether.broadcastip); //broadcast
  ether.printIp("DHCP server: ", ether.dhcpip); //servidor de onde veio o DHCP
}
//Inicializacao dos recursos.  
void setup() {
  Serial.begin(57600);//usamos serial para ecos dos dados.
  Serial.println(F("Iniciando"));
  
  dhcp(); //chama a funcao pra iniciar o dhcp
  look();
  ether.registerPingCallback(pingado);//chama esse report para receber os pings
  //ether.parseIp(ether.hisip, "10.10.10.10");
  
}

void loop () {
  word len = ether.packetReceive(); //permite receber pacotes
  word pos = ether.packetLoop(len); //responde os pings que entrarem
  
 //faz uma requisicao para a cada 15 segundos
  if (millis() > timer) {
    timer = millis() + 15000;
    Serial.println();
    Serial.print("<<< REQ ");
    ether.browseUrl(PSTR("/status.php?"), "operacao=abrir", website, get_callback);
   }
   
}
  
  
