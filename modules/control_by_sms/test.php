<?php
       include('Postgrescom.class.php');

$con = new Postgrescom();
$con->open();
if($con->statusCon() == -1)
        echo "conexao falhou!";
else {

	$res = $con->query('select username from mdl_user');
	echo $res;


}

?>
