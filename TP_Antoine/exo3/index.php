<!DOCTYPE html>
<html>

<head>
	<title>Formulaire PHP</title>
</head>

<body>

<form action="imc.php" method="post" enctype="multipart/form-data" name="IMC">
	<fieldset>
		<legend>Envoie de votre IMC</legend>
			Taille (m) : <input type="number" name="height" id="height" onChange="calc_imc()"><br><br>
		 	Masse (kg) : <input type="number" name="weight" id="weight" onChange="calc_imc()"><br><br>
		 	IMC : (Calcul : masse (kg) / (taille (m) )² : <input type="number" name="display_IMC" disabled><br><br>
  			<input type="submit" value="Envoie de l'IMC" name="submit"><br><br>
  			Dernière IMC indiquée : 

  			<?php 

  			$myfile = fopen("./txt/imc.txt", "r") or die("Unable to open file!");
			echo fread($myfile, filesize("./txt/imc.txt"));
			fclose($myfile);

  			?>
	</fieldset>  
</form>

<script type="text/javascript">
	
function calc_imc(){
	var kg = document.getElementById("weight").value;
	var m = document.getElementById("height").value;
    var IMCresult = kg / (m * m);
    document.IMC.display_IMC.value = IMCresult;
}

</script>

<form action="upload_file.php" method="post" enctype="multipart/form-data">
	<fieldset>
		<legend>Envoie d'image vers le serveur</legend>
		 	<input type="file" name="fileToUpload" id="fileToUpload"><br>
  			<input type="submit" value="Upload Image" name="submit"><br>

  			<?php 

			function random_pic($dir = './uploads')
			{
			    $files = glob($dir . '/*.*');
			    $file = array_rand($files);
			    return $files[$file];
			}

			echo "<img src=" . random_pic() . ">";

  			?>
  			<img src="" style="position: center;">
	</fieldset>  
</form>

</body>
</html>