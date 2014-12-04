$(document).ready(function() {
  var rowDiv = createNewRow();

  $(rowDiv).append(createNewClock(TimeTools.testTimesheet));
  $(rowDiv).append(createNewClock(TimeTools.testTimesheet));

  function createNewClock(timesheet) {

    var weeks = TimeTools.getWeeks(timesheet['clockedIn'], timesheet['clockedOut']);
    var weekTime = 0;
    var dayTime = 0;
    if(weeks.length > 0) {
      var week = weeks[weeks.length-1];
      weekTime = TimeTools.getTimeTotal(week['in'], week['out']);

      var days = TimeTools.getDays(week['in'], week['out']);
      if(days.length > 0) {
        var day = days[days.length-1];
        day = TimeTools.getTimeTotal(day['in'], week['out']);
      }
    }

    var cloned = $("#clock-in-template").clone();
    cloned.removeAttr('id');
    cloned.removeAttr('style');

    cloned.find(".clock-in-title-text").html("Name Of Job")
    cloned.find(".clock-in-week").html("<strong>Week:</strong> "+TimeTools.msToReadable(weekTime));
    cloned.find(".clock-in-day").html("<strong>Day:</strong> "+TimeTools.msToReadable(dayTime));

    return cloned;
  }
  function createNewRow() {
    var rowDiv = $(document.createElement("div"));
    $("#clock-in-list").append(rowDiv);
    rowDiv.attr("class", "row");

    var fillerColumn = $(document.createElement("div"));
    rowDiv.append(fillerColumn);
    fillerColumn.attr("class", "col-sm-1 col-md-2 col-lg-3");

    return rowDiv;
  }
});
