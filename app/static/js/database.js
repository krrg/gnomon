function Database() {

}
Database.listOrganizations = function() {
  return $.ajax({
    type: "GET",
    url: "/api/v1/organizations",
    dataType: "json"
  });
}
Database.listUsers = function() {
  return $.ajax({
    type: "GET",
    url: "/api/v1/users",
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
