<?php
include('./php/libs/Postgrescom.class.php');
include('./php/libs/IXR_Library.inc.php');
include('./php/defines.php');
include('./php/interface.php');
include("./lang/en/block_control_by_sms.php");

// Test if the user is allowed to use the feature //
$user_id = $_GET['user_id'];
if ($user_id != null) {

    $con = new Postgrescom();
    $con->open();
    if($con->statusCon() == -1) {

        echo $string['conection_failed'];
        exit(-1);
    }

    $answer = $con->query("select userid from mdl_role_assignments where roleid IN (select id from mdl_role where name='Manager')");

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

} else {
    echo $string['not_allowed'];
    exit(0);
}

$page.= "<html><head>";
$page.= "<title>Control By SMS" . $string['logs_title'] ." - Registros do Sistema</title>";
$page.= "<LINK REL=StyleSheet HREF=\"/moodle/theme/standard/style/core.css\" TYPE=\"text/css\" MEDIA=screen>";

$page.= "</head><body>";

$page.= "<h1 align=\"center\">";
$page.= $string['logs_title'];
$page.= "</h1>";

$page.= clean_log_button($string['clean_logs'], $user_id);

if($_GET['clean_logs'] == '1') {
    do_clean_logs();
}

$page.= "<div align=\"center\">";
$page .= "<textarea disabled=\"disabled\" rows=\"30\" cols=\"95\">" . get_system_log() . "</textarea>";
$page.= "</div>";
$page .= "</body></html>";

echo $page;

?>

