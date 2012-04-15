/**
 * DHTML date validation script. Courtesy of SmartWebby.com (http://www.smartwebby.com/dhtml/datevalidation.asp)
 */
// Declaring valid date character, minimum year and maximum year
var dtCh= "/";
var minYear=2012;
var maxYear=minYear+1;

function isInteger(s){
    var i;
    for (i = 0; i < s.length; i++){   
        // Check that current character is number.
        var c = s.charAt(i);
        if (((c < "0") || (c > "9"))) return false;
    }
    // All characters are numbers.
    return true;
}

function stripCharsInBag(s, bag){
    var i;
    var returnString = "";
    // Search through string's characters one by one.
    // If character is not in bag, append to returnString.
    for (i = 0; i < s.length; i++){   
        var c = s.charAt(i);
        if (bag.indexOf(c) == -1) returnString += c;
    }
    return returnString;
}

function daysInFebruary (year){
    // February has 29 days in any year evenly divisible by four,
    // EXCEPT for centurial years which are not also divisible by 400.
    return (((year % 4 == 0) && ( (!(year % 100 == 0)) || (year % 400 == 0))) ? 29 : 28 );
}
function DaysArray(n) {
    for (var i = 1; i <= n; i++) {
        this[i] = 31
        if (i==4 || i==6 || i==9 || i==11) {this[i] = 30}
        if (i==2) {this[i] = 29}
   } 
   return this
}

function isDate(dtStr){

    var daysInMonth = DaysArray(12)
    var pos1 = dtStr.indexOf(dtCh)
    var pos2 = dtStr.indexOf(dtCh,pos1+1)
    var strDay = dtStr.substring(0,pos1)
    var strMonth = dtStr.substring(pos1+1,pos2)
    var strYear = dtStr.substring(pos2+1)
    strYr = strYear

    if (strDay.charAt(0)=="0" && strDay.length>1) strDay=strDay.substring(1)
    if (strMonth.charAt(0)=="0" && strMonth.length>1) strMonth=strMonth.substring(1)
    for (var i = 1; i <= 3; i++) {
        if (strYr.charAt(0)=="0" && strYr.length>1) strYr=strYr.substring(1)
    }
    month=parseInt(strMonth)
    day=parseInt(strDay)
    year=parseInt(strYr)
    if (pos1==-1 || pos2==-1){
        alert("O formato da data deve ser: dia/mes/ano")
        return false
    }
    if (strDay.length<1 || day<1 || day>31 || (month==2 && day>daysInFebruary(year)) || day > daysInMonth[month]){
        alert("Entre com um dia válido.")
        return false
    }
    if (strMonth.length<1 || month<1 || month>12){
        alert("Entre com um mês válido.")
        return false
    }
    if (strYear.length != 4 || year==0 || year<minYear || year>maxYear){
        alert("Entre com um ano válido de quatro dígitos. Ano máximo: " + maxYear)
        return false
    }
    if (dtStr.indexOf(dtCh,pos2+1)!=-1 || isInteger(stripCharsInBag(dtStr, dtCh))==false){
        alert("Entre com uma data válida.")
        return false
    }
return true
}

// Radio Button Validation
// copyright Stephen Chapman, 15th Nov 2004,14th Sep 2005
// you may copy this function but please keep the copyright notice with it
function valButton(btn) {
    var cnt = -1;
    for (var i=btn.length-1; i > -1; i--) {
        if (btn[i].checked) {cnt = i; i = -1;}
    }
    if (cnt > -1) return btn[cnt].value;
    else return null;
}


/*
<!-- Original:  Sandeep Tamhankar (stamhankar@hotmail.com) -->
<!-- Web Site:  http://207.20.242.93 -->

<!-- This script and many more are available free online at -->
<!-- The JavaScript Source!! http://javascript.internet.com -->

<!-- Begin -->
*/
function isValidTime(timeStr)
{
    var timePat = /^(\d{1,2}):(\d{2})?$/;
    
    var matchArray = timeStr.match(timePat);

    if (matchArray == null) {
        alert("A hora está em um formato inválido.");
        return false;
    }
    hour = matchArray[1];
    minute = matchArray[2];
    second = "00";
    ampm = null;
    
    if (second=="") { second = null; }
    if (ampm=="") { ampm = null }
    
    if (hour < 0  || hour > 23) {
        alert("Entre com uma hora entre 00 e 23.");
        return false;
    }

    if (minute<0 || minute > 59) {
        alert ("Entre com minutos entre 0 e 59.");
        return false;
    }

    return true;
}
//  End -->
