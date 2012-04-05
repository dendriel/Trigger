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

if($_GET['course_group'] != null) {

    $group = $_GET['course_group'];
    $users = $con->query("SELECT firstname,lastname,phone2 FROM mdl_user WHERE id IN (SELECT userid FROM mdl_groups_members WHERE groupid IN (SELECT id FROM mdl_groups WHERE name='$group'));");

    if ($users == -1) {
        echo "Error while communicating with the moodle database!";
        exit;
    }

} else {
    $users = "";
}

$user_id = $_GET['user_id'];

// Test if the user is allowed to use the feature //
if ($user_id != null) {

    $answer = $con->query("select userid from mdl_role_assignments where roleid IN (select id from mdl_role where name='Teacher' or name='Manager')");

    if ($answer == -1) {
        echo "Error while communicating with the moodle database!";
        exit;

    } else {
        $allowed = pg_fetch_all($answer);
        $allowed_len = count($allowed);
        $ok = false;   

        for($index = 0; $index < $allowed_len; $index++) {
            if((int)$user_id == (int)$allowed[$index]["userid"]) {
                $ok = true;
            }
        }
        if ($ok == false) {
            echo "You don't have permission to use this feature!";
            exit(0);
        }
    }
    
    // Select the lastname of the user to fill the origin field //
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
$select_group = build_select_group_input();
$contacts_table = build_contacts_table($users);
$table_buttons = build_table_buttons();
$selected_table = build_empty_table();
$input_form = build_input_form($origin);
$tail = build_tail();


$form.= $header;

$form.= "<table border=\"2\">";
$form.= "<tr>";

$form.= "<td>";
$form.= "<table border=\"1\">";


    $form.= "<tr>";
        $form.= "<td>";
            $form.= $contacts_table;
        $form.= "</td>";
    $form.= "</tr>";

    $form.= "<tr>";
        $form.= "<td>";
            $form.= $select_group;
        $form.= "</td>";
    $form.= "</tr>";

$form.= "<td border-style:solid;\">";
$form.= $table_buttons;
$form.= "</td>";

$form.= "</table>";
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
    #echo $contacts_list . "<br/>" . $message . "<br/>" . $send . "<br/>" . $datetime . "<br/>" . $origin_ts;

    if (($origin_ts != null) and ($contacts_list != null) and ($message != null)) {
        try {
            $client = new IXR_Client($server_address);
            
            if (! $client->query('newRequisition', $origin_ts, $contacts_list, $message, $OPERATOR, $send, $datetime)) {
                print 'Procedure returned error message: ' . $client->getErrorMessage() . '.';
                exit(-1);
            }
            if ($client->getResponse() == $TRUE) {
                echo "<br />Requisition successful registered!";
    
            } else {
                echo "<br />Failed to communicate with the server!";
                exit(-1);
            }
        } catch (Exception $e) {
            echo "Failed to communicate with the server! $e";
                exit(-1);
        }
    }

}
?>

