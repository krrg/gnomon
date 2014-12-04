$(document).ready(function(event) {
  $("#sign-in-button").click(function(event) {
    event.preventDefault();
    var data = {
      "username": $("#sign-in-username").val(),
      "password": $("#sign-in-password").val()
    }
    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: "/api/v1/auth",
      data: JSON.stringify(data),
      dataType: "json",
      success: function(result) {
        console.log("success");
        window.location = "/clockin";
      },
      error: function(xhr,status,error) {
        $("#sign-in-warning").show();
        if(xhr.status == 401) {
          $("#sign-in-warning").html("Incorrect username or password");
        }
        else {
          $("#sign-in-warning").html("There was an unknown error, please try a again later.");
        }
      }
    });
  });
});
