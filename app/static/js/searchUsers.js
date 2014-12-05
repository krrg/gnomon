$(document).ready(function() {
  var selectedJob = null;
  var selectedOrg = null;


  createUserList();
  getOrganizations().done(function(data){
    var organizations = data['organizations'];
    for(var i=0; i<organizations.length; i++) {
      createOrganzationItem(organizations[i]);
    }
  });
  $("#search-bar").on('input', function() {

    var query = $.trim($(this).val()).toLowerCase();
    $('.person-active').each(function(){
      var $this = $(this);
      var username = $this.find(".person-username").first().text().toLowerCase();
      if(username.indexOf(query) === -1) {
        $this.fadeOut();
      }
      else {
        $this.fadeIn();
      }
    });
  });

  $(document).on('click','#job-selector .dropdown-menu li a', function(e)
  {
    var newHeading = $(this).text();
    $('#job-selector-text').html(newHeading);
  });
  function createOrganzationItem(organization) {
    var dropdown = $("#organization-selector .dropdown-menu").first();
    var id = organization['id'];
    var organizationItem = $('<li role="presentation"><a role="menuitem" tabindex="-1" href="#">' + organization['name'] + '</a></li>');
    dropdown.append(organizationItem);
    organizationItem.click(function() {
      var selectedOrg = id;
      var newHeading = $(this).text();
      $('#organization-selector-text').html(newHeading);
      $('#job-selector .dropdown-menu').html('');
      $('#job-selector-text').html("Select Job");
      $('#job-selector-button').removeAttr("disabled");
    });
  }
  function createPerson(person) {
    var cloned = $("#person-template").clone();
    cloned.removeAttr('id');
    cloned.removeAttr('style');
    cloned.addClass('person-active');
    $("#user-list-inner").append(cloned);

    cloned.find(".person-username").html("<p>"+person['username']+"</p>");
    cloned.find("button").click(function() {
      var modal = $('#person-modal');
      modal.find(".modal-title").html(person['username']);
      $('#organization-selector-text').html("Select Organization");
      $('#job-selector-text').html("Select Job");
      $('#job-selector-button').attr("disabled","disabled");
      $('#add-person-button').attr("disabled","disabled");
      modal.modal('show');
      selectedJob = null;
      selectedOrg = null;
    });
    cloned.find(".img-responsive").attr('src', 'http://www.gravatar.com/avatar/'+person['id']+'?f=y&d=identicon');
  }
  function createUserList() {
    $.ajax({
      type: "GET",
      url: "/api/v1/users",
      dataType: "json",
      success: function(result) {
        var users = result['users'];
        for(var i=0; i<users.length; i++) {
          createPerson(users[i]);
        }
      },
      error: function(xhr,status,error) {
        console.log(xhr);
      }
    });
  }
});


function getOrganizations() {
  return $.ajax({
    type: "GET",
    url: "/api/v1/organizations",
    dataType: "json"
  });
}
