<?php
/********************************************************
 *
 * Author: Vitor Rozsa
 * email: vd5_@hotmail.com
 *
 * Brief: Search by the given group number and return all
 *       the members of it.
 *******************************************************/

include('../php/libs/Postgrescom.class.php');
include('../php/defines.php');

// args: number
if (count($argv) < 2) {
    exit(2);

} else {
    $group = $argv[1];
}

$con = new Postgrescom();

$con->open();

if($con->statusCon() == -1) {
    exit(2);
}

// mdl_groups -> moodle course groups.
// mdl_groups_members -> table that assigns users to groups.
// mdl_users -> table of users
$query = "select phone2 from mdl_user where id in (select userid from mdl_groups_members where groupid in (select id from mdl_groups where name='$group'))";

$val = $con->query($query);

if ($val == -1) {
    // failed to query to the database.
    exit(2);

} else if (pg_fetch_row($val) == null) {
    // there are no ocurrences.
    exit(1);

} else {
    $list = pg_fetch_all($val);
    $list_len = count($list);
    $contacts = "";

    for($index = 0; $index < $list_len; $index++) {
        $contacts.= $list[$index][$PHONE2];

        if ($index < ($list_len-1)) {
            $contacts.= ',';
        }
    }
    exit($contacts);
}
?>
