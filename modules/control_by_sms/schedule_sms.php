<?php
include('./php/interface.php');
include('Postgrescom.class.php');

$con = new Postgrescom();

$con->open();
if($con->statusCon() == -1) {
    echo "conexao falhou!";
    exit;
}

$users = $con->query("SELECT firstname,lastname,phone2 FROM mdl_user WHERE id IN (SELECT userid FROM mdl_groups_members)");

if ($users == -1) {
    echo "erro ao enviar query!";
    exit;
}

$header = build_header();
$contacts_table = build_contacts_table($users);
$table_buttons = build_table_buttons();
$selected_table = build_empty_table();
$input_form = build_input_form();
$tail = build_tail();


$form.= $header;

$form.= "<table>";
$form.= "<tr>";

$form.= "<td>";
$form.= $contacts_table;
$form.= "</td>";

$form.= "<td>";
$form.= $table_buttons;
$form.= "</td>";

$form.= "<form name=\"sms_service\" action=\"schedule_sms.php\" method=\"get\" onsubmit=\"return validateForm();\">";
$form.= "<td>";
$form.= $selected_table;
$form.= "</td>";

$form.= "<td>";
$form.= $input_form;
$form.= "</td>";

$form.= "</tr>";
$form.= "</form>";
$form.= "</table>";

$form.= $tail;

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

