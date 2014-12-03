function TimeTools () {

}
TimeTools.monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
TimeTools.dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
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
  console.log(ms);
  var seconds=(~~(ms/1000))%60
  var minutes=(~~(ms/(1000*60)))%60
  var hours=(~~(ms/(1000*60*60)))

  var hourStr = hours.toString();
  var minuteStr = minutes >= 10 ? minutes.toString() : "0"+minutes.toString();
  var secondsStr = seconds >= 10 ? seconds.toString() : "0"+seconds.toString();

  return ""+hourStr+":"+minuteStr+":"+secondsStr;
}
