<!DOCTYPE html>
<!-- This is a sample of how to get garagemhacker status using php 
	* Get the status.txt state on $status exploded array
	* Show div from the status value
-->
<html>
<head>
	<title>Changing image from php</title>
	<style>
		.lampon{
			width: 100px;
			height: 100px;
			background: #ff0; //Yellow brick
				
		}
		.lampoff{
			width: 100px;
			height: 100px;
			background: #000; //Black brick
		}		
		
	</style>
</head>

<body>
<?php
$file = 'http://garagemhacker.org/status.txt';
$status = explode("\n", file_get_contents($file));

if ($status[0] == 'aberto'){
	//Mostrar imagem com lampada acesa
	echo '<div class="lampon"></div>';
		
	}
else {
	//Mostrar imagem com lampada apagada
	echo '<div class="lampoff"></div>';
	}
?>


</body>
</html>