function TimeTools () {

}
TimeTools.monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
TimeTools.dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
TimeTools.testTimesheet = {
  "dateCreated":1417000000000,
  "clockedIn":[1417000000000, 1417490641667, 1417490790000, 1417691990000, 1417791990000],
  "clockedOut":[1417001010000, 1417490699999, 1417490890000,1417701990000, 1417792990000]
};
TimeTools.getLastSunday = function(timestamp) {
  var dateCreated = new Date(timestamp);
  dateCreated.setDate(dateCreated.getDate() - dateCreated.getDay());
  var sunday = new Date(dateCreated.toLocaleDateString());
  return sunday;
}
TimeTools.getWeeks = function(clockInArray, clockOutArray) {
  var weeks = [];
  var startIndex = 0;
  var lastSunday = null;
  for(var i=0; i<clockInArray.length; i++) {
    var thisSunday = TimeTools.getLastSunday(new Date(clockInArray[i]));
    if(lastSunday == null) {
      lastSunday = thisSunday;
    }
    if(thisSunday > lastSunday) {
      var weekInArray = clockInArray.slice(startIndex, i);
      var weekOutArray = clockOutArray.slice(startIndex, Math.min(i, clockOutArray.length));
      weeks.push({"in":weekInArray, "out":weekOutArray});
      startIndex = i;
      lastSunday = thisSunday;
    }
  }
  if(clockInArray.length !== 0){
    var weekInArray = clockInArray.slice(startIndex, clockInArray.length);
    var weekOutArray = clockOutArray.slice(startIndex, clockOutArray.length);
    weeks.push({"in":weekInArray, "out":weekOutArray});
  }
  return weeks;
}
TimeTools.getFlatDay = function(timestamp) {
  var dateCreated = new Date(timestamp);
  var day = new Date(dateCreated.toLocaleDateString());
  return day;
}
TimeTools.getDays = function(clockInArray, clockOutArray) {
  var weeks = [];
  var startIndex = 0;
  var lastSunday = null;
  for(var i=0; i<clockInArray.length; i++) {
    var thisSunday = TimeTools.getFlatDay(new Date(clockInArray[i]));
    if(lastSunday == null) {
      lastSunday = thisSunday;
    }
    if(thisSunday > lastSunday) {
      var weekInArray = clockInArray.slice(startIndex, i);
      var weekOutArray = clockOutArray.slice(startIndex, Math.min(i, clockOutArray.length));
      weeks.push({"in":weekInArray, "out":weekOutArray});
      startIndex = i;
      lastSunday = thisSunday;
    }
  }
  if(clockInArray.length !== 0){
    var weekInArray = clockInArray.slice(startIndex, clockInArray.length);
    var weekOutArray = clockOutArray.slice(startIndex, clockOutArray.length);
    weeks.push({"in":weekInArray, "out":weekOutArray});
  }
  return weeks;
}
TimeTools.getTimeTotal = function(clockInArray, clockOutArray) {
  var sumTotal = 0;
  for(var i=0; i<clockInArray.length; i++) {
    var inTime = clockInArray[i];
    var outTime = null;
    if(i >= clockOutArray.length) {
      outTime = new Date().getTime();
    }
    else {
      outTime = clockOutArray[i];
    }
    sumTotal += (outTime-inTime);
  }
  return sumTotal
}
TimeTools.msToReadable = function(ms) {
  var seconds=(~~(ms/1000))%60
  var minutes=(~~(ms/(1000*60)))%60
  var hours=(~~(ms/(1000*60*60)))

  var hourStr = hours.toString();
  var minuteStr = minutes >= 10 ? minutes.toString() : "0"+minutes.toString();
  var secondsStr = seconds >= 10 ? seconds.toString() : "0"+seconds.toString();

  return ""+hourStr+":"+minuteStr+":"+secondsStr;
}
TimeTools.getBasicTime = function(date) {
  var hours = date.getHours();
  var mid = "AM";
  if(hours == 0) {
    hours = 12;
  }
  else if( hours > 12) {
    hours = hours % 12;
    mid = "PM";
  }
  return hours + ":"+TimeTools.getTwoDigitStr(date.getMinutes())+":"+TimeTools.getTwoDigitStr(date.getSeconds())+" "+mid;
}
TimeTools.getTwoDigitStr = function(val) {
  if(val < 10)
    return "0" + val;
  return val;
}
TimeTools.getTimeToMs = function() {

}
TimeTools.parseTextHourMinute = function(text) {
  text = text.trim();

  if(text === "") {
    return text;
  }
  var hour = 0;
  var minute = 0;
  var morning = true;
  if(text.toLowerCase().indexOf("pm", text.length - 2) !== -1) {
    morning = false;
    text = text.substring(0, text.length - 2);
  }
  if(text.toLowerCase().indexOf("am", text.length - 2) !== -1) {
    text = text.substring(0, text.length - 2);
  }

  var splitText = text.trim().split(":");
  var firstNumber = parseInt(splitText[0]);

  if(isNaN(firstNumber) || firstNumber < 1 || firstNumber > 12) {
    return null;
  }
  hour = firstNumber;
  if(!morning && hour != 12) {
    hour += 12;
  }
  if(morning && hour == 12) {
    hour = 0;
  }

  if(splitText.length == 1) {
    return {"hour":hour, "minute":minute};
  }

  var secondNumber = parseInt(splitText[1]);

  if(isNaN(secondNumber) || secondNumber < 0 || secondNumber > 59) {
    return null;
  }
  minute = secondNumber;
  return {"hour":hour, "minute":minute};
}
TimeTools.objectToMS = function(obj) {
  var time = 0;
  if(obj['hour']) {
    time += obj['hour']*3600000;
  }
  if(obj['minute']) {
    time += obj['minute']*60000;
  }
  return time;
}
