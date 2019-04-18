$(document).ready(function() {
    // Handle register
    $("#profile").click(function(e){
      $.ajax(
      {
          type: 'GET',
          contentType: "application/json; charset=utf-8",
          dataType : 'json',
          url: '/profile',
          success : function(result) {
            if(result['ok'] == true){
              var user = result['data'];
              if(user['type'] == 'A'){
                console.log("reditecte");
                window.location.href = "./profile/admin_profile.html";
              }else if(user['type'] == 'R'){

              }else{

              }
            }
          },
          error : function(errormsg){
            console.log(errormsg);
          }
      });
      e.preventDefault();
      });

  });

