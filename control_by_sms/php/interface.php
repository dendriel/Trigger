<?php
/********************************************************
 *
 * Author: Vitor Rozsa
 * email: vd5_@hotmail.com
 *
 * Brief: Functions that will build the schedule page.
 *******************************************************/

include_once('libs/IXR_Library.inc.php');
include_once('defines.php');
include_once('../lang/en/block_control_by_sms.php');


/* global */
$TBL_SIZE = 10;

/********************************************************
 * Brief: Build a table/list from the given parameter.
 */
function build_contacts_table($users)
{
    global $TBL_SIZE;
    global $string;

    $table.= "<div style=\"text-align:center;\">";
    $table.= "<select multiple=\"multiple\" id=\"avaliable_users_select\" name=\"avaliable_users\" size=\"$TBL_SIZE\">";
    $table.= "<optgroup label=\"" . $string['avaliable'] . "\")\">";
    
    while($user = pg_fetch_row($users)) {
    	$table.= "<option name=\"$user[2]\" value=\"$user[2]\">$user[2] - $user[0] $user[1]</option>";
    }
    
    $table.= "</optgroup>";
    $table.= "</select>";
    $table.= "</div>";
    
    return $table;
}
/********************************************************
 * Brief: Build a clear table to receive selected users.
 */
function build_empty_table()
{
    global $TBL_SIZE;
    global $string;
    $table.= "<select name=\"destination_users_select[]\" id=\"destination_users_select\" multiple=\"multiple\" size=\"$TBL_SIZE\">";
    $table.= "<optgroup label=\"" . $string['selected'] . "\">";
    $table.= "</optgroup>";
    $table.= "</select>";
    
    return $table;
}
/********************************************************
 * Brief: Build the header.
 */
function build_header()
{
    global $string;
    $header.= "<html><head>";
    $header.= "<title>" . $string['pluginname'] . " - " . $string['schedule_title'] . "</title>";
    $header.= "<script src=\"./js/interface.js\"></script>";
    $header.= "<script src=\"./js/validate.js\"></script>"; 
    $header.= "<LINK REL=StyleSheet HREF=\"/moodle/theme/standard/style/core.css\" TYPE=\"text/css\" MEDIA=screen>";
    $header.= "<LINK REL=StyleSheet HREF=\"style/plugin_style.css\" TYPE=\"text/css\" MEDIA=screen>";
    $header.= "</head><body>";
    $header.= "<h1 align=\"center\">" . $string['schedule_title'] . "</h1>";

    return $header;
}

/********************************************************
 * Brief: Build the tail.
 */
function build_tail()
{
    return "</body></html>";
}

/********************************************************
 * Brief: Build table interact buttons.
 */
function build_table_buttons()
{
    global $string;

    $button.= "<div style=\"text-align:center;\">";
    $button.= "<input type=\"button\" value=\"" . $string['rm_buttom']  . "\" onclick=\"removeSelected();\" />";
    $button.= "<input type=\"button\" value=\"" . $string['add_buttom'] . "\" onclick=\"addSelected();\" />";
    $button.= "</div>";
    
    return $button;
}
/********************************************************
 * Brief: Build form that will receive message and 
 *      options.
 */
function build_input_form($origin)
{
    global $string;
    $form.= "<table>";

    $form.= "<tr><td>";
    $form.= $string['input_origin'] . ":<br /><input name=\"origin\" type=\"text\" value=\"$origin\" maxlength=7 size=22>";
    $form.= "</td></tr>";

    $form.= "<tr><td>";
    $form.= "<textarea rows=\"8\" cols=\"19\" name=\"message\" maxlength=149></textarea><br />" . $string['max_text_length'];
    $form.= "</td></tr>";

    $form.= "<tr><td>";
    $form.= "<input type=\"radio\" name=\"sms_action\" id=\"sms_action0\" checked=\"yes\" value=\"0\" />" . $string['instant_sms'];
    $form.= "</td></tr>";

    $form.= "<table style=\"border:2px inset;\">";
        $form.= "<tr><td>";
            $form.= "<input type=\"radio\" name=\"sms_action\" id=\"sms_action1\" value=\"1\" />" . $string['schedule_sms'];
        $form.= "</td></tr>";

        $form.= "<tr><td>";
            $form.= $string['input_date'] . ":<br /><input name=\"date\" type=\"text\">";
        $form.= "</td></tr>";

        $form.= "<tr><td>";
            $form.= $string['input_time'] . ":<br /><input name=\"time\" type=\"text\" maxlength=5>";
        $form.= "</td></tr>";
    $form.= "</table>";

    $form.= "<tr><td style=\"border-style:none;text-align:center;\">";
    $form.= "<input type=\"submit\" value=\"".$string['register'] . "\">";
    $form.= "</td></tr>";

    $form.= "</table>";

    return $form;
}

/********************************************************
 * Brief: Build input field that will recover groups list.
 */
function build_select_group_input() 
{
    global $string;
    $form.= "<div style=\"text-align:center;\">";
    $form.= "<form method=\"get\" action=\"schedule_sms.php\">";
    $form.= $string['retrieve_dest_title'] . ":<br />";
    $form.= "<input name=\"course_group\" type=\"text\" maxlength=10>";
    $form.= "<input type=\"submit\" value=\"" . $string['retrieve_dest_buttom'] . "\">";
    $form.= "</form>";
    $form.= "</div>";

    return $form;
}

/********************************************************
 * Brief: Format that input.
 */
function mount_date($date_obj)
{
    $date.= $date_obj->hour . ":" . $date_obj->minute;
    $date.= " - ";
    $date.= $date_obj->day . "/" . $date_obj->month . "/" . $date_obj->year;

    return $date;
}

/********************************************************
 * Brief: Format the given string to be displayed.
 */
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

/********************************************************
 * Brief: Recover the specified type of requisitions from 
 *      server.
 */

function get_requisitions($req_type) 
{
    global $server_address;
    try {
        $client = new IXR_Client($server_address);
        
        if (! $client->query('getRequisitions', $req_type)) {
            echo get_string('daemon_error', 'block_control_by_sms');
            return null;
        }
        $req_list = $client->getResponse();
    
        return $req_list;
    
    } catch (Exception $e) {
        echo get_string('daemon_error', 'block_control_by_sms'); // $e;
        return null;
    }
}
?>
