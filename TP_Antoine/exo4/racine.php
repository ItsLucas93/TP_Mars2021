<!DOCTYPE html>
<html>
<head>
	<title>Calcul Racine</title>
</head>
<body>

<fieldset>
	<legend>Racine (Page2)</legend>
		<?php 

		if(isset($_POST["submit"])) {
			$number = $_POST["display"];
			echo "La racine carré du nombre " . $number . " est " . sqrt($number);
		}
		?>
		<a href="index.php">Revenir à la page 1</a>
</fieldset>
</body>
</html>