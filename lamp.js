/*This is the GaragemHacker Checkout Status JS

- It make an asyncronus check on a status.txt file, and change an image
class lampoff to lampon.

To use this you need to create an element on you page with  ID lamp.

*/

window.onload=function start() {

var xmlhttp, status, logger; //my vars
//var xmlhttp;
xmlhttp = new XMLHttpRequest();
//xmlhttp.open('GET', 'http://www.garagemhacker.org/status.txt', true); //this request for outsider's require enable CORS
xmlhttp.open('GET', 'status.txt', true);
xmlhttp.send();

//logger = xmlhttp.responseText;//get the response on status var
console.log(xmlhttp.responseText); //show the response on console.log (for debuger's
xmlhttp.onreadystatechange=function(){

status = xmlhttp.responseText;//get the response on status var

if (xmlhttp.readyState==4 && xmlhttp.status==200){
    if(status.trim() == 'fechado'){
        //Change element to lamp off
        document.getElementById("lamp").style.backgroundPosition=("-85px 85px");
        //document.getElementById("lamp").innerHTML=status;//show content of the status.txt file
        //console.log(xmlhttp); //Somente para Debug
        }
        else if (status.trim() == 'aberto') {
            //Change element to lamp on
            document.getElementById("lamp").style.backgroundPosition=("10px 85px");
            //document.getElementById("real").innerText=xmlhttp.responseText;//Use para requisicoes sincronas com xmlhttp false
            //document.getElementById("lamp").innerHTML=status;//show content of the status.txt file
            }
        //console.log(xmlhttp);//uncoment for a fully debug for if end else if condition
        }
    }//close the xmlhttp.onreadystatechange
}//close start