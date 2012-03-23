<?php
include('./php/interface.php');
include('./php/libs/Postgrescom.class.php');
include('./php/libs/IXR_Library.inc.php');
include('./php/defines.php');

$con = new Postgrescom();

$con->open();
if($con->statusCon() == -1) {
    echo "conexao falhou!";
    exit;
}

$users = $con->query("SELECT firstname,lastname,phone2 FROM mdl_user WHERE id IN (SELECT userid FROM mdl_groups_members)");

if ($users == -1) {
    echo "Error while communicating with the moodle database!";
    exit;
}

$user_id = $_GET['user_id'];

if ($user_id != null) {
    $origin = $con->query("SELECT lastname FROM mdl_user WHERE id=$user_id");

    if ($origin == -1) {
        echo "Error while communicating with the moodle database!";
        exit;
    } else {
        $origin = pg_fetch_row($origin);
        $origin = $origin[0];
    }
} 

$header = build_header();
$contacts_table = build_contacts_table($users);
$table_buttons = build_table_buttons();
$selected_table = build_empty_table();
$input_form = build_input_form($origin);
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

    // retrieve contacts list //
    $contacts_raw = $_GET['destination_users_select'];
    $contacts_list = '';
    $index = 0;
    $contacts_len = count($contacts_raw);
    
    for ($index = 0; $index <= $contacts_len; $index++) {
        $contacts_list .= $contacts_raw[$index];

        if ($index < $contacts_len-1) {
            $contacts_list .= ',';
        }
    }

    // get origin //
    $origin_ts = $_GET['origin'];

    // retrieve message //
    $message = $_GET['message'];

    // retrieve  sms action "SEND" //
    $send = $_GET['sms_action'];

    // retrive date/time //
    if ($send == 1) {
        $datetime = $_GET['date'] . ' ' . $_GET['time'] . ':00';
        $send = False;

    } else {
        $datetime = "10/10/2012 20:30:30"; 
        $send = True;
    }

    // submit all //
    //echo $contacts_list . "<br/>" . $message . "<br/>" . $send . "<br/>" . $datetime . "<br/>" . $origin_ts;

    if (($origin_ts != null) and ($contacts_list != null) and ($message != null)) {
        try {
            $client = new IXR_Client($server_address);
            
            if (! $client->query('newRequisition', $origin_ts, $contacts_list, $message, $OPERATOR, $send, $datetime)) {
                print 'Procedure returned error message: ' . $client->getErrorMessage() . '.';
            }
            if ($client->getResponse() == $TRUE) {
                echo "<br />Requisition successful registered!";
    
            } else {
                echo "<br />Failed to communicate with the server!";
                
            }
        } catch (Exception $e) {
            echo "Failed to communicate with the server! $e";
        }
    }

}
?>

