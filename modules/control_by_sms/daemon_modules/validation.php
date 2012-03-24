<?php
/********************************************************
 *
 * Author: Vitor Rozsa
 * email: vd5_@hotmail.com
 *
 * Brief: This module will evaluate the require number
 *       returning 0 if the number exist in the database
 *       or "return > 0" if the number does not exist.
 *******************************************************/

include('../php/libs/Postgrescom.class.php');

// args: number
if (count($argv) < 2) {
    exit(2);

} else {
    $number = $argv[1];
}

$con = new Postgrescom();

$con->open();

if($con->statusCon() == -1) {
    exit(2);
}

// mdl_role -> moodle access level for members
// mdl_role_assignments -> table that assigns users to levels
// mdl_users -> table of users
$query = "select username from mdl_user where phone2='$number' and id in (select userid from mdl_role_assignments where roleid IN (select id from mdl_role where name='Teacher'))";

$val = $con->query($query);

if ($val == -1) {
    // failed to query to the database.
    exit(2);

} else if (pg_fetch_row($val) == null) {
    // there are no ocurrences.
    exit(1);

} else {
    // there are ocurrences.
    exit(0);
}
?>
