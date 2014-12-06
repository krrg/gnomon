$(document).ready(function() {

  //createTimesheets([TimeTools.testTimesheet,TimeTools.testTimesheet,TimeTools.testTimesheet])
  Database.listTimesheetsByUserId(GnomonSession.userid).done(function(result) {
    var timesheets = result['timesheets'];
    createTimesheets(timesheets);
  });


  function createTimesheets(timesheets) {
    var rowDiv = null;
    for(var i=0; i<timesheets.length; i++){
      if(i%2 === 0) {
        rowDiv = createNewRow();
      }
      $(rowDiv).append(createNewClock(timesheets[i]));
    }
  }

  function createNewClock(timesheet) {

    var weeks = TimeTools.getWeeks(timesheet['clockIn'], timesheet['clockOut']);
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

    var clonedBtn = cloned.find(".clock-in-btn").first();
    if(timesheet['clockIn'].length > timesheet['clockOut'].length) {
      clonedBtn.addClass("btn-danger");
      clonedBtn.html("Clock Out");
      clonedBtn.click(function() {
        var currentTime = new Date().getTime();
        var data = {"clockOut":currentTime};
        Database.createClock(data, timesheet['id']).done(function(){
          alert("clock out success");
        })
      });
    }
    else {
      clonedBtn.addClass("btn-success");
      clonedBtn.html("Clock In");
      clonedBtn.click(function(){
        var currentTime = new Date().getTime();
        var data = {"clockIn":currentTime};
        Database.createClock(data, timesheet['id']).done(function(){
          alert("clock in success");
        })
      });
    }

    cloned.find(".clock-in-btn").click(function(){
      console.log('here');
    });

    cloned.find(".clock-in-title-text").html("loading...");

    Database.getJob(timesheet['jobId']).done(function(result) {
      cloned.find(".clock-in-title-text").html(result['job']['name']);
      cloned.find(".clock-in-image").attr("src", "http://www.gravatar.com/avatar/" + result['job']['id'] + "?f=y&d=identicon")
    });
    cloned.find(".timesheet-link").attr("href", "/timesheet/"+timesheet['id']);
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
