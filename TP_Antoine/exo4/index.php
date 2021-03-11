<!DOCTYPE html>
<html>
<head>
	<title>Calcul Racine</title>
</head>
<body>

<fieldset>
	<legend>Racine (Page1)</legend>
		<button onclick="getInteger()"> Générer le nombre : </button>
		<form action="racine.php" method="post" enctype="multipart/form-data">
			Le nombre en question : <input type="number" min="-10" max="10" name="display" id="display"> </p>
			<input type="submit" value="Envoi du nombre" name="submit"><br><br>
		</form>
</fieldset>
</body>

<script type="text/javascript">
function getInteger(){
	var max = 10;
	var min = -10;
	var num = Math.floor(Math.random() * (max - min)) + min;
	document.getElementById('display').value = num;
}
</script>
</html>