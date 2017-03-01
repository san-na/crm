//在layout中使用sweetalert2实现消息闪现
$(document).ready(function(){
  var swal_text = $('#swal_text').val();
  var swal_type = $('#swal_type').val();
  if(swal_text){
    swal({
      title: swal_text,
      text: '两秒后关闭提示框……',
      timer: 2000,
      type: swal_type
    }).then(
      // handling the promise rejection
      function (dismiss) {
        if (dismiss === 'timer') {
          console.log('I was closed by the timer');
        }
      });
  }
});
// end of sweetalert2 flash

//click applications
  $("#applications_nav").click(function(){
    window.location.href=Flask.url_for('Common.applications');
    // window.location.href=url;
  });
// end of click applications


//click users
  $("#users_nav").click(function(){
     window.location.href=Flask.url_for('Common.users',{'action': 'list' });
  });
// end of click users


//click two_fa_devices
  $("#two_fa_devices_nav").click(function(){
     window.location.href=Flask.url_for('Common.two_fa_devices');
  });
// end of click two_fa_devices

//click admins
  $("#admins_nav").click(function(){
     window.location.href=Flask.url_for('Common.admins');
  });
// end of click admins

//click logs
  $("#logs_nav").click(function(){
     window.location.href=Flask.url_for('Common.logs');
  });
// end of click logs
