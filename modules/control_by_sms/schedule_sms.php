<html>
<head></head>

<body>
<?php
include_once realpath(dirname( __FILE__ ).DIRECTORY_SEPARATOR).DIRECTORY_SEPARATOR."common.php";
include_once LIB_DIR.DIRECTORY_SEPARATOR."User.php";
include_once LIB_DIR.DIRECTORY_SEPARATOR."Course.php";
include_once LIB_DIR.DIRECTORY_SEPARATOR."eMail.php";

	global $USER;
	$userid = $USER->id;
	echo "user: $userid";

	$con = mysql_connect("localhost", "moodle", "moodle");
	if (!$con) {
		die('Could not connect: ' . mysql_error());
	}
	mysql_select_db("moodle", $con);
	$list_name = mysql_query("SELECT username FROM mdl_user");

	while($name = mysql_fetch_array($list_name)) {
		echo "$name <br />";
	}
	mysql_close($con);
?>



</body>
</html>
