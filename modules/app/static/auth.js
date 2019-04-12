$(document).ready(function() {
    // Handle register
    $("#signup").click(function(e){
      var jsonData = {};
      var formData = $("#signup_form").serializeArray();
      $.each(formData, function() {
          if (jsonData[this.name]) {
             if (!jsonData[this.name].push) {
                 jsonData[this.name] = [jsonData[this.name]];
             }
             jsonData[this.name].push(this.value || '');
         } else {
             jsonData[this.name] = this.value || '';
         }
      });
      $.ajax(
      {
          type: 'POST',
          contentType: "application/json; charset=utf-8",
          dataType : 'json',
          url: '/register',
          data : JSON.stringify(jsonData),
          success : function(result) {
            if(result['ok'] == true){
              window.location.href = "/";
            }
          },
          error : function(errormsg){
            console.log(errormsg);
          }
      });
      e.preventDefault();
      });

      // Handle login

      $("#login").click(function(e){
      var jsonData = {};
      var formData = $("#login_form").serializeArray();
      $.each(formData, function() {
          if (jsonData[this.name]) {
             if (!jsonData[this.name].push) {
                 jsonData[this.name] = [jsonData[this.name]];
             }
             jsonData[this.name].push(this.value || '');
         } else {
             jsonData[this.name] = this.value || '';
         }
      });
      $.ajax(
      {
          type: 'POST',
          contentType: "application/json; charset=utf-8",
          dataType : 'json',
          url: '/login',
          data : JSON.stringify(jsonData),
          success : function(result) {
            if(result['ok'] == true){
              window.location.href = "/";
            }
          },
          error : function(errormsg){
            alert(errormsg.responseJSON['message']);
          }
      });
      e.preventDefault();
      });

  });

