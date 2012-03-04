<html>
<head>
<script type="text/javascript">

/********************************************************
 * Brief: Catch ands plit the given parameters in URL.
 */
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
/********************************************************
 * Brief: Change the selected users from avaliable users
 *	 list to the destinations list.
 */
function addSelected()
{
  var avaliable_list = document.getElementById('avaliable_users_select');
  var destination_list = document.getElementById('destination_users_select');
  var index;

  // Do for all the selected items.
  for (index = avaliable_list.length - 1; index>=0; index--) {

    if (avaliable_list.options[index].selected) {

      var copyItem = avaliable_list.options[index];
      avaliable_list.remove(index);
      destination_list.add(copyItem);
    }
  }
}
/********************************************************
 * Brief: Change the selected users from destinations
 *	 list to avalible users list.
 */
function removeSelected()
{
  var destination_list = document.getElementById('destination_users_select');
  var avaliable_list = document.getElementById('avaliable_users_select');
  var index;

  // Do for all the selected items.
  for (index = destination_list.length - 1; index>=0; index--) {

    if (destination_list.options[index].selected) {

      var copyItem = destination_list.options[index];
      destination_list.remove(index);
      avaliable_list.add(copyItem);
    }
  }
}
/********************************************************
 * Brief: Mark all destinations before sending to daemon.
 *  ref.: www.mredkj.com
 */
function selectAllOptions(select_box)
{
  var selected_obj = document.getElementById(select_box);

  for (var i=0; i<selected_obj.options.length; i++) {
    selected_obj.options[i].selected = true;
  }
}

</script>
</head>

<body>

<?php

$TBL_SIZE = 10;

/*
 * Brief: Build a table/list from the given parameter.
 */
function build_contacts_table($users)
{
	global $TBL_SIZE;
	$table.= "<select multiple=\"multiple\" id=\"avaliable_users_select\" name=\"avaliable_users\" size=\"$TBL_SIZE\">";
	$table.= "<optgroup label=\"Avaliable\")\">";

	while($user = pg_fetch_row($users)) {
		$table.= "<option name=\"$user[1]\" value=\"$user[1]\">$user[1] - $user[0]</option>";
        }

	$table.= "</optgroup>";
	$table.= "</select>";

	return $table;
}

/*
 * Build a clear table to receive selected users;
 */
function build_empty_table()
{
	global $TBL_SIZE;
	$table.= "<select name=\"destination_users_select[]\" id=\"destination_users_select\" multiple=\"multiple\" size=\"$TBL_SIZE\">";
	$table.= "<optgroup label=\"Selected\">";
	$table.= "</optgroup>";
	$table.= "</select>";

	return $table;
}

?>


<?php

include('Postgrescom.class.php');

$con = new Postgrescom();

$con->open();
if($con->statusCon() == -1) {
	echo "conexao falhou!";
	exit;
}

$users = $con->query("SELECT firstname,phone2 FROM mdl_user WHERE id IN (SELECT userid FROM mdl_groups_members)");

if ($users == -1) {
	echo "erro ao enviar query!";
	exit;
}
$contacts_table = build_contacts_table($users);
$selected_table = build_empty_table();


$form.= $contacts_table;
$form.= "<form action=\"schedule_sms.php\" method=\"get\" onsubmit=\"selectAllOptions('destination_users_select');\">";
$form.= $selected_table;
$form.= "<input type=\"button\" value=\"Add Selected\" onclick=\"addSelected();\" /><br />";
$form.= "<input type=\"button\" value=\"Remove Selected\" onclick=\"removeSelected();\" />";
$form.= "<input type=\"submit\" value=\"Send\" />";
$form.= "</form>";



//echo $contacts_table;
//echo $selected_table;
echo $form;

$con->close();

?>

<?php

if ($_GET != null) {
  $contact_list = $_GET['destination_users_select'];
	$index = 0;
	for ($index = 0; $index<= count($contact_list); $index++) {
		echo "<br />".$contact_list[$index];
	}
}
?>



</body>
</html>
