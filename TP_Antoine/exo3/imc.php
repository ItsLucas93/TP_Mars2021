<?php

if(isset($_POST["submit"])) {
	$height = $_POST["height"];
	$weight = $_POST["weight"];
	$imc = $_POST["display_IMC"];
	$myfile = fopen("./txt/imc.txt", "w") or die("Unable to open file!");
	$txt = "Masse (kg) : " . $height . ", Taille (m) : " . $weight . ", IMC calculé : " . $imc . ".";
	fwrite($myfile, $txt);
	fclose($myfile);
}

?> 

<?php header("Location: http://localhost/TP_Antoine/exo3/"); ?>