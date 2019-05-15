$(document).ready(function () {
  $.ajax({
    type: 'POST',
    url: '/scheduleAppointments',
    // data: data,
    // data: { get_param: 'value' },
    success: function (data) {
      var names = data
      console.log(names)
      // $('#cand').html(data);
    }
  });
});

// obj = JSON.parse(json);

// console.log(obj.count);
// // expected output: 42

// console.log(obj.result);
// // expected output: true