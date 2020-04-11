$('button#btn-fw').click(function(){
    $.ajax({
        url: "/FW/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#btn-bw').click(function(){
    $.ajax({
        url: "/BW/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#btn-lf').click(function(){
    $.ajax({
        url: "/left/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#btn-rg').click(function(){
    $.ajax({
        url: "/right/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#stop').click(function(){
    $.ajax({
        url: "/stop/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#btn-rt-lf').click(function(){
    $.ajax({
        url: "/rotateleft/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#btn-rt-rg').click(function(){
    $.ajax({
        url: "/rotateright/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#btn-rec').click(function(){
    $.ajax({
        data : {
            title : prompt("Journal Name: "),
                },
        url: "/startJ/",
        type: "POST",
        success: function(resp){
            $('div#log-msg').append(resp.data);
        }
    });
  });
  $('button#btn-rec-stp').click(function(){
    $.ajax({
        url: "/stopJ/",
        type: "POST",
        success: function(resp){
            $('svg#map').append(resp.svgdata);
        }
    });
  });
  $(document).ready(function() {
      $('form#distanceForm').on('submit', function(event) {
      $.ajax({
          data : {
              x : $('#distanceX').val(),
              y: $('#distanceY').val(),
                  },
              type : 'POST',
              url : '/distance'
              })
          .done(function(resp) {
          /*$('div#log-msg').append(resp.data);*/
          $('div#map').append(resp.svgdata);
      });
      event.preventDefault();
      });
      $('form#rotateForm').on('submit', function(event) {
      $.ajax({
          data : {
              deg : $('#fname').val(),
                  },
              type : 'POST',
              url : '/rotate'
              })
          .done(function(resp) {
          $('div#log-msg').append(resp.data);
      });
      event.preventDefault();
      });   
  });