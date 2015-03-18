window.onload=function start() {

//var xmlhttp, text; //algumas variaveis de debug
var xmlhttp;
xmlhttp = new XMLHttpRequest();
xmlhttp.open('GET', 'http://www.garagemhacker.org/status.txt', true);
xmlhttp.send();

//text = xmlhttp.responseText; //get the response on text var

xmlhttp.onreadystatechange=function(){
  if (xmlhttp.readyState==4 && xmlhttp.status==200){
  	if(xmlhttp.responseText.trim() == 'fechado'){
    	document.getElementById("lamp").innerHTML=xmlhttp.responseText;
    	//console.log(xmlhttp); //Somente para Debug
    	
    	}
    else if (xmlhttp.responseText.trim() == 'aberto') {
   		//document.getElementById("real").innerText=xmlhttp.responseText;//Use para requisicoes sincronas com xmlhttp false
    	document.getElementById("lamp").innerHTML=xmlhttp.responseText;
    	}
    }
  }
}