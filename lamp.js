window.onload=function start() {

var xmlhttp, status; //my vars
//var xmlhttp;
xmlhttp = new XMLHttpRequest();
//xmlhttp.open('GET', 'http://www.garagemhacker.org/status.txt', true); //this request for outsider's require enable CORS
xmlhttp.open('GET', 'status.txt', true);
xmlhttp.send();

status = xmlhttp.responseText;//get the response on status var
console.log(xmlhttp.responseText);
xmlhttp.onreadystatechange=function(){
	
	status = xmlhttp.responseText;//get the response on status var
	
 	 if (xmlhttp.readyState==4 && xmlhttp.status==200){
  		if(xmlhttp.responseText.trim() == 'fechado'){
    		document.getElementById("lamp").innerHTML=xmlhttp.responseText;
    		console.log(xmlhttp); //Somente para Debug 
    		}
    	else if (xmlhttp.responseText.trim() == 'aberto') {
   			//document.getElementById("real").innerText=xmlhttp.responseText;//Use para requisicoes sincronas com xmlhttp false
    		document.getElementById("lamp").innerHTML=xmlhttp.responseText;
    		}
    	}
  	}//close the xmlhttp.onreadystatechange
}//close start