<html>
<head>
<script type="text/javascript">
function show_param()
{
	var x = 0
	var parameters = {};
	mySearch = location.search.substr(1).split("&")
	
	for (x=0;x<mySearch.length;x++) {

		var params = mySearch[x].split("=");
		parameters[params[0]] = params[1];
	}
	return parameters;
}
</script>
</head>

<body>




<?php
	include('Postgrescom.class.php');

	$con = new Postgrescom();

	$con->open();

	if($con->statusCon() == -1) {
		echo "conexao falhou!";
		exit;
	}
	$users = $con->query("SELECT username, phone1 FROM mdl_user");
	
	if ($users == -1) {
		echo "erro ao enviar query!";
		exit;
	}
        while($user = pg_fetch_row($users)) {
            echo "$user[0] - $user[1] <br />";
        }
	$con->close();

	$con->statusCon();

//	$js.= "<script type=\"text/javascript\">\n";
//	$js.= "var parameters = show_param()\n";
//	$js.= "alert('course_id = ' + parameters['course_id'])\n";
//	$js.= "</script>\n";
//	echo $js;

?>

</body>
</html>
