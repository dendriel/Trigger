<?php
/********************************************************
 *
 * Author: Vitor Rozsa
 * email: vd5_@hotmail.com
 *
 * Brief: Functions that will build the schedule page.
 *******************************************************/

/* global */
$TBL_SIZE = 10;

/********************************************************
 * Brief: Build a table/list from the given parameter.
 */
function build_contacts_table($users)
{
    global $TBL_SIZE;
    $table.= "<select multiple=\"multiple\" id=\"avaliable_users_select\" name=\"avaliable_users\" size=\"$TBL_SIZE\">";
    $table.= "<optgroup label=\"Avaliable\")\">";
    
    while($user = pg_fetch_row($users)) {
    	$table.= "<option name=\"$user[2]\" value=\"$user[2]\">$user[2] - $user[0] $user[1]</option>";
    }
    
    $table.= "</optgroup>";
    $table.= "</select>";
    
    return $table;
}
/********************************************************
 * Brief: Build a clear table to receive selected users.
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
/********************************************************
 * Brief: Build the header.
 */
function build_header()
{
    $header.= "<html><head>";
    $header.= "<title>Control by SMS</title>";
    $header.= "<script src=\"./js/interface.js\"></script>";
    $header.= "<script src=\"./js/validate.js\"></script>"; 
    $header.= "</head><body>";
    $header.= "<h1 align=\"center\">SMS Service</h1>";

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
    $button.= "<input type=\"button\" value=\"Add Item &rarr;\" onclick=\"addSelected();\" /><br />";
    $button.= "<input type=\"button\" value=\"&larr; Rem Item\" onclick=\"removeSelected();\" />";
    
    return $button;
}
/********************************************************
 * Brief: Build form that will receive message and 
 *      options.
 */
function build_input_form($origin)
{
    $form.= "<table border=1>";

    $form.= "<tr><td>";
    $form.= "Origin:<input name=\"origin\" type=\"text\" value=\"$origin\" maxlength=7>";
    $form.= "</td></tr>";

    $form.= "<tr><td>";
    $form.= "<textarea rows=\"8\" cols=\"19\" name=\"message\" maxlength=149></textarea><br />M&aacute;x.149 caracteres";
    $form.= "</td></tr>";

    $form.= "<tr><td>";
    $form.= "<input type=\"radio\" name=\"sms_action\" id=\"sms_action0\" checked=\"yes\" value=\"0\" />Instant SMS";
    $form.= "<input type=\"radio\" name=\"sms_action\" id=\"sms_action1\" value=\"1\" />Schedule SMS";
    $form.= "</td></tr>";

    $form.= "<tr><td>";
    $form.= "Date:<input name=\"date\" type=\"text\">";
    $form.= "</td></tr>";

    $form.= "<tr><td>";
    $form.= "Time (HH:MM format):<input name=\"time\" type=\"text\" maxlength=5>";
    $form.= "</td></tr>";

    $form.= "<tr><td>";
    $form.= "<input type=\"submit\">";
    $form.= "</td></tr>";

    $form.= "</table>";

    return $form;
}
?>

