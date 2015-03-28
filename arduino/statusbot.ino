//GaragemHacker - StatusBot
/*
--> babysteps desse projeto
Objetivo: Requisitar uma pagina web usando metodo get para
indicar se o hackerspace esta aberto ou fechado.

- Arduino Ethercard ENC28J60 https://github.com/jcw/ethercard
- Este bot deve usar DHCP com MAC Amarrado ao nosso servidor local
- Caso conectemos via serial ele deve ecoar todos os parametros que ele possui
- Pode receber pings para mostar que esta vivo
- Se o status do botao estiver ligado deve requisitar a pagina para abrir e acender o led verde
- Se o status do botao for desligado deve requisitar a pagina para fechar e acender o led vermelho

*/

//Incluindo a lib Ethercard --> https://github.com/jcw/ethercard/archive/master.zip
#include <EtherCard.h>

int ledgreen = 7; //iniciar led verde na porta 7
int ledred = 6; //iniciar led vermelho na porta 6
int botao = 2; //iniciar botao na porta 6
int buttonState;//the current reading from the input pin
int lastButtonState = LOW;//set lastbutton state to LOW


//Iniciando o ethernet shield com o mac abaixo
static byte mymac[] = { 0x74,0x69,0x69,0x2D,0x30,0x31 };
byte Ethernet::buffer[700];
static uint32_t timer;

//quem vou disparar o acesso
const char website[] PROGMEM = "garagemhacker.org";

//funcao para dnsLookup (traducao de ip)
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

//funcao para alternar os leds pelo estado do botao
static void ledchange(){
// set initial LED state  
  int reading = digitalRead(botao);
  if (reading == LOW){   
      digitalWrite(ledred, HIGH);
      digitalWrite(ledgreen,LOW);
  }
  else{
      digitalWrite(ledred,LOW );
      digitalWrite(ledgreen,HIGH);
  }
}


//My debouncing settings (solve button debouce)
long lastDebounceTime = 0; 
long debounceDelay = 50;

//Inicializacao dos recursos.  
void setup() {
  pinMode (ledgreen, OUTPUT);
  pinMode (ledred, OUTPUT);
  pinMode (botao, INPUT);
  Serial.begin(57600);//usamos serial para ecos dos dados.
  Serial.println(F("Iniciando"));
 
  dhcp(); //chama a funcao pra iniciar o dhcp
  look();
  ether.registerPingCallback(pingado);//chama esse report para receber os pings
  //ether.parseIp(ether.hisip, "10.10.10.10");//Seta um ip em hisip

  //iniciar com o led na mesma posicao do botao
  ledchange();
  
}

void loop () {
   
  //Receber pings e troca de dados
  word len = ether.packetReceive(); //permite receber pacotes
  word pos = ether.packetLoop(len); //responde os pings que entrarem

  int reading = digitalRead(botao);
   if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }
 
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer
    // than the debounce delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;
      ledchange();
      if (buttonState == HIGH){
        Serial.println("abriu!!! ;p");
        ether.browseUrl(PSTR("/status.php?"), "operacao=abrir", website, get_callback);
      }
      else{
        Serial.println("fechou!!! ;(");
        ether.browseUrl(PSTR("/status.php?"), "operacao=fechar", website, get_callback);
      }
    }
  }
 
  // set the LED:
  
  // save the reading.  Next time through the loop,
  // it'll be the lastButtonState:
  lastButtonState = reading;

}
