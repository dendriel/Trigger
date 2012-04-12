<?php
include('./php/libs/Postgrescom.class.php');
include('./php/libs/IXR_Library.inc.php');
include('./php/defines.php');
include('./php/interface.php');
include("./lang/en/block_control_by_sms.php");

$active_b = get_string('active', 'block_control_by_sms');
$canceled_b = get_string('canceled', 'block_control_by_sms');
$failed_b = get_string('failed', 'block_control_by_sms');
$sent_b = get_string('sent', 'block_control_by_sms');

$active_b = $string['active'];
$canceled_b = $string['canceled'];
$failed_b = $string['failed'];
$sent_b = $string['sent'];

// Test if the user is allowed to use the feature //
$user_id = $_GET['user_id'];
if ($user_id != null) {

    $con = new Postgrescom();
    $con->open();
    if($con->statusCon() == -1) {

        echo $string['conection_failed'];
        exit(-1);
    }

    $answer = $con->query("select userid from mdl_role_assignments where roleid IN (select id from mdl_role where name='Teacher' or name='Manager')");

    if ($answer == -1) {
        echo $string['conection_failed'];
        exit(-1);
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
            echo $string['not_allowed'];
            exit(0);
        }
    }
    $con->close();
}

$req_type = (int)$_GET['req_type'];

if(($req_type) >= 0 or ($req_type <=3)) {

    $req_list = get_requisitions($req_type);
    switch($req_type) {

        case $ACTIVE: 
            $header2 = $active_b; 
            $tr_color = $string['green_header'];
            $th_color = $string['green_body'];
        break;
        case $CANCELED: 
            $header2 = $canceled_b; 
            $tr_color = $string['yellow_header'];
            $th_color = $string['yellow_body'];
        break;
        case $FAILED: 
            $header2 = $failed_b; 
            $tr_color = $string['red_header'];
            $th_color = $string['red_body'];
        break;
        case $SENT: 
            $header2 = $sent_b; 
            $tr_color = $string['blue_header'];
            $th_color = $string['blue_body'];
        break;
    }
}

$page.= "<html><head>";
$page.= "<title>Control By SMS - Reports</title>";
$page.= "<LINK REL=StyleSheet HREF=\"/moodle/theme/standard/style/core.css\" TYPE=\"text/css\" MEDIA=screen>";
$page.= '<style type="text/css">
table {
    border-width: 1px;
    border-spacing: 0px;
    border-style: solid;
    border-color: gray;
    border-collapse: collapse;
}
th {
    border-width: 1px;
    padding: 1px;
    border-style: dotted;
    border-color: gray;
    -moz-border-radius: ;
}
td {
    border-width: 1px;
    padding: 22x;
    border-style: dotted;
    border-color: gray;
    -moz-border-radius: ;
}';
$page.="</style>";

$page.= "</head><body>";

$page.= "<h1 align=\"center\">";
$page.= $string['reports_title'];
$page.= "</h1>";

// Reports options table //
$page.= "<div align=\"center\">";
$page.= "<table border=\"2\">";
$page.= "<tr>";
$page.= "<td><a href=\"reports.php?req_type=$ACTIVE\">$active_b</a></td>";
$page.= "<td><a href=\"reports.php?req_type=$CANCELED\">$canceled_b</a></td>";
$page.= "<td><a href=\"reports.php?req_type=$FAILED\">$failed_b</a></td>";
$page.= "<td><a href=\"reports.php?req_type=$SENT\">$sent_b</a></td>";
$page.= "</tr>";
$page.= "</table></div>";

$page.= "<h2 align=\"center\"><u>$header2</u></h2>";

$table.= "<div align=\"center\">";
$table.= "<table border=\"1\">";

$table.= "<tr style=\"background-color:$tr_color;\">";
$table.= "<th>" . $string['origin_col'] . "</th>";
$table.= "<th>" . $string['message_col'] . "</th>";
$table.= "<th>" . $string['blow_col'] . "</th>";
$table.= "<th>" . $string['destination_col'] . "</th>";
$table.= "</tr>";

// Mount table
if ($req_list != null) {

    for ($index=0; $index < count($req_list); $index++) {
        $table.= "<tr style=\"background-color:$th_color\">";
        $table.= "<td>" . $req_list[$index][$ORIG] . "</td>";
        $table.= "<td>" . treat_str($req_list[$index][$MSG]) . "</td>";
        $table.= "<td>" . mount_date($req_list[$index][$BLOW]) . "</td>";
        $table.= "<td>" . treat_str($req_list[$index][$DESTN]) . "</td>";
        $table.= "</tr>";
    }
} else {
    echo $string['daemon_error'];
}

$table.= "</table></div>";
$page.= $table;
$page .= "</body></html>";
echo $page;

?>

