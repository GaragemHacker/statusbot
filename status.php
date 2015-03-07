<html>
<head>
<title>GaragemHacker Status</title>
</head>

<body>


<p>
<?php
if ($_GET["operacao"] === "abrir") {
	echo "aberto\n";
	// gravar "aceso" no status.txt
	$status = fopen("status.txt", "w") or die("OPS... nao gravou");	
	$txt = "aberto\n";
	fwrite($status, $txt);
	fclose($status);
	
} elseif ($_GET["operacao"] === "fechar") {
	echo "fechado";
	// gravar "apagado" no status.txt
	$status = fopen("status.txt", "w") or die("OPS... nao gravou");	
	$txt = "fechado\n";
	fwrite($status, $txt);
	fclose($status);
	
}

?>
<h3>Garagem Hacker - Curitiba HackerSpace</h3>
<!--</p>

<ul>
<li><a href="?operacao=abrir">Abrir</a></li>
<li><a href="?operacao=fechar">Fechar</a></li>
</ul>
-->


</body>
