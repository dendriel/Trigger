/********************************************************
 *
 * Author: Vitor Rozsa
 * email: vd5_@hotmail.com
 *
 * Brief: Functions that will give interation to the 
 *	schedule page.
 *******************************************************/

/********************************************************
 * Brief: Catch ands plit the given parameters in URL.
 */
function show_param()
{
	var x = 0
	var parameters = {};
	mySearch = location.search.substr(1).split("&")
	
	for (x=0;x<mySearch.length;x++) {

		var params = mySearch[x].split("=");
		parameters[params[0]] = params[1];
	}
	return parameters;
}
/********************************************************
 * Brief: Change the selected users from avaliable users
 *	list to the destinations list.
 */
function addSelected()
{
    var avaliable_list = document.getElementById('avaliable_users_select');
    var destination_list = document.getElementById('destination_users_select');
    var index;
  
    // Do for all the selected items.
    for (index = avaliable_list.length - 1; index>=0; index--) {
    
        if (avaliable_list.options[index].selected) {
            var copyItem = avaliable_list.options[index];
            avaliable_list.remove(index);
            destination_list.add(copyItem);
        }
    }
}
/********************************************************
 * Brief: Change the selected users from destinations
 *	list to avalible users list.
 */
function removeSelected()
{
    var destination_list = document.getElementById('destination_users_select');
    var avaliable_list = document.getElementById('avaliable_users_select');
    var index;
  
    // Do for all the selected items.
    for (index = destination_list.length - 1; index>=0; index--) {
  
        if (destination_list.options[index].selected) {
          var copyItem = destination_list.options[index];
          destination_list.remove(index);
          avaliable_list.add(copyItem);
        }
    }
}
/********************************************************
 * Brief: Mark all destinations before sending to daemon.
 *  	ref.: www.mredkj.com
 */
function selectAllOptions(select_box)
{
    var selected_obj = document.getElementById(select_box);
  
    if (selected_obj.length == 0) {
        return false;
    }

    for (var i=0; i<selected_obj.length; i++) {
        selected_obj.options[i].selected = true;
    }
    
    return true;
}
/********************************************************
 * Brief: Validate the input options inserted by the 
 *      user.
 */
function validateForm()
{
    var date = document.sms_service.date;
    var time = document.sms_service.time;
    var sms_action = valButton(sms_service.sms_action);

    if (isDate(date.value) == false) {
        date.focus()
        return false;

    } else if (selectAllOptions('destination_users_select') == false) {
        alert('No destinations are selected!');
        return false;

    } else if (document.sms_service.message.value.length == 0) {
        alert('You need to add some text to the body message!');
        return false;

    } else if (sms_action == 1) {

        if (isValidTime(time.value) == false) {
            time.focus();
            return false;
        }
    
    } else {
        return true;
    }
}

