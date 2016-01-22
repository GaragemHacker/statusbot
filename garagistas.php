<html>
<head>
<title>Garagistas</title>
</head>

<body>


<p>
<?php

if (strpos($_GET["name"], 'xxx.') !== false ) { //se nao comecar com xXx entao
	$str = ltrim($_GET["name"], "x.");
	echo $str;
	
} else {
	//print_r($_GET);
	echo 'Hummmm sorry!';
}

?>

</body>
