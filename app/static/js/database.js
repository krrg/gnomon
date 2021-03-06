function Database() {

}
Database.validUsername = function(username) {
  var jsondata = JSON.stringify({"username":username});
  return $.ajax({
    type: "POST",
    url: "/api/v1/users/exists",
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.login = function(username, password) {
  return $.ajax({
    type: "POST",
    contentType: "application/json",
    url: "/api/v1/auth",
    data: JSON.stringify({"username":username, "password":password}),
    dataType: "json"
  });
}
Database.register = function(username, password) {
  var jsondata = JSON.stringify({"user":{"username":username, "password":password, "email":""}});
  return $.ajax({
    type: "POST",
    url: "/api/v1/users",
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.listOrganizations = function() {
  return $.ajax({
    type: "GET",
    url: "/api/v1/organizations",
    dataType: "json"
  });
}
Database.createOrganization = function(data) {
  var jsondata = JSON.stringify({"organization":data});
  return $.ajax({
    type: "POST",
    url: "/api/v1/organizations",
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.listUsers = function() {
  return $.ajax({
    type: "GET",
    url: "/api/v1/users",
    dataType: "json"
  });
}
Database.listUsersByJob = function(jobId) {
  return $.ajax({
    type: "GET",
    url: "/api/v1/users?jobId="+jobId,
    dataType: "json"
  });
}
Database.getUser = function(userId) {
  var url = "/api/v1/users/"+userId;

  return $.ajax({
    type: "GET",
    url: url,
    dataType: "json"
  });
}
Database.listJobs = function(orgId) {
  var url = "/api/v1/jobs?";

  if(orgId) {
    url += "organizationId=" + orgId;
  }

  return $.ajax({
    type: "GET",
    url: url,
    dataType: "json"
  });
}
Database.getJob = function(jobId) {
  var url = "/api/v1/jobs/"+jobId;

  return $.ajax({
    type: "GET",
    url: url,
    dataType: "json"
  });
}
Database.createJob = function(data) {
  var jsondata = JSON.stringify({"job":data});
  return $.ajax({
    type: "POST",
    url: "/api/v1/jobs",
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.updateJob = function(id,data) {
  var jsondata = JSON.stringify({"job":data});
  return $.ajax({
    type: "PUT",
    url: "/api/v1/jobs/"+id,
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.listTimesheetsByUserId = function(userId) {
  return $.ajax({
    type: "GET",
    url: "/api/v1/timesheets?userId="+userId,
    // url: "/api/v1/timesheets",
    dataType: "json"
  });
}
Database.listTimesheetsByUserIdAndJobId = function(userId, jobId) {
  return $.ajax({
    type: "GET",
    url: "/api/v1/timesheets?userId="+userId+"&"+jobId,
    // url: "/api/v1/timesheets",
    dataType: "json"
  });
}
Database.createTimesheet = function(data) {
  var jsondata = JSON.stringify({"timesheet":data});
  console.log(jsondata);
  return $.ajax({
    type: "POST",
    url: "/api/v1/timesheets",
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.createClock = function(data, id) {
  var jsondata= JSON.stringify(data);
  return $.ajax({
    type: "POST",
    url: "/api/v1/timesheets/"+id+"/clock",
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.deleteClock = function(timestamp, id){
  return $.ajax({
    type: "DELETE",
    url: "/api/v1/timesheets/"+id+"/clock/"+timestamp,
    dataType: "json",
    contentType:"application/json"
  });
}
Database.updateClock = function(data, id) {
  var jsondata= JSON.stringify(data);
  return $.ajax({
    type: "PUT",
    url: "/api/v1/timesheets/"+id+"/clock",
    dataType: "json",
    data:jsondata,
    contentType:"application/json"
  });
}
Database.getTimesheet = function(id) {
  return $.ajax({
    type: "GET",
    url: "/api/v1/timesheets/"+id,
    dataType: "json"
  });
}
Database.clockIn = function(id) {
  return $.ajax({
    type: "GET",
    url: "/api/v1/timesheets/"+id +"/clockin",
    dataType: "json"
  });
}
Database.clockOut = function(id) {
  return $.ajax({
    type: "GET",
    url: "/api/v1/timesheets/"+id +"/clockout",
    dataType: "json"
  });
}
