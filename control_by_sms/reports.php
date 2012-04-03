<?php
include('./php/libs/Postgrescom.class.php');
include('./php/libs/IXR_Library.inc.php');
include('./php/defines.php');
include('./php/interface.php');

$active_b = "Active";
$canceled_b = "Canceled";
$failed_b = "Failed";
$sent_b = "Sent";


$user_id = $_GET['user_id'];

if ($user_id != null) {

    $con = new Postgrescom();
    
    $con->open();
    if($con->statusCon() == -1) {
        echo "conexao falhou!";
        exit;
    }

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
}


$req_type = (int)$_GET['req_type'];

if(($req_type) >= 0 or ($req_type <=3)) {

    $req_list = get_requisitions($req_type);
    switch($req_type) {

        case $ACTIVE: $header2 = $active_b; break;
        case $CANCELED: $header2 = $canceled_b; break;
        case $FAILED: $header2 = $failed_b; break;
        case $SENT: $header2 = $sent_b; break;
    }
}

$page.= "<html><head>";
$page.= "<title>Control By SMS - Reports</title>";
$page.= "</head><body>";

$page.= "<h1 align=\"center\">Reports</h1>";

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

$table.= "<tr>";
$table.= "<th>Origin</th>";
$table.= "<th>Message</th>";
$table.= "<th>Blow</th>";
$table.= "<th>Destination[s]</th>";
$table.= "</tr>";

// Mount table
if ($req_list != null) {

    for ($index=0; $index < count($req_list); $index++) {
        $table.= "<tr>";
        $table.= "<td>" . $req_list[$index][$ORIG] . "</td>";
        $table.= "<td>" . treat_str($req_list[$index][$MSG]) . "</td>";
        $table.= "<td>" . mount_date($req_list[$index][$BLOW]) . "</td>";
        $table.= "<td>" . treat_str($req_list[$index][$DESTN]) . "</td>";
        $table.= "</tr>";
    }
}

$table.= "</table></div>";
$page.= $table;
$page .= "</body></html>";
echo $page;

function get_requisitions($req_type) 
{
    global $server_address;
    try {
        $client = new IXR_Client($server_address);
        
        if (! $client->query('getRequisitions', $req_type)) {
            print 'Procedure returned error message: ' . $client->getErrorMessage() . '.';
            return null;
        }
        $req_list = $client->getResponse();
    
        return $req_list;
    
    } catch (Exception $e) {
        echo "Failed to communicate with the server! $e";
        return null;
    }
}

function treat_str($msg)
{
    if(strlen($msg) >= 60) {
        $msg_ret.= substr($msg, 0, 54) . "<br />";
        $msg_ret2.= substr($msg, 54);

        if(strlen($msg_ret2) >= 60) {
            $msg_ret.= substr($msg_ret2, 0, 54) . "<br />";
            $msg_ret.= substr($msg_ret2, 54);

        } else {
            $msg_ret.= $msg_ret2;
        }

        return $msg_ret;

    } else {
        return $msg;
    }
}

function mount_date($date_obj)
{
    $date.= $date_obj->hour . ":" . $date_obj->minute;
    $date.= " - ";
    $date.= $date_obj->day . "/" . $date_obj->month . "/" . $date_obj->year;

    return $date;
}

?>
