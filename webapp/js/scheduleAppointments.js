var count = [1,1,1,1,1];
function dayCounter(day) {
  if(day=="mon"){
    tmp = count[0];
    count[0]++;
    return tmp;
  }
  if (day == "tue") {
    tmp = count[1];
    count[1]++;
    return tmp;
  }
  if (day == "wed") {
    tmp = count[2];
    count[2]++;
    return tmp;
  }
  if (day == "thu") {
    tmp = count[3];
    count[3]++;
    return tmp;
  }
  if (day == "fri") {
    tmp = count[4];
    count[4]++;
    return tmp;
  }
}

$(document).ready(function () {
  $.ajax({
    type: 'POST',
    url: '/scheduleAppointments',
    // data: { get_param: 'value' },
    dataType: 'json',
    success: function (data) {

      $.each(data, function(index, appointment) {
        console.log(appointment);
        // console.log(appointment.Name);
        // console.log(appointment.Surname);
        // console.log(appointment.House);
        // console.log(appointment.Day);
        // console.log(appointment.Hour);
        createAppointment(index, appointment);
      })
      scheduleEverything();
    }
  });

});

function createAppointment(index, appointment) {
  var dayContainer = $('#' + appointment.Day + '> ul');
  
  dayContainer.append($('<li/>', {
    id: index,
    class: 'single-event'
  }))

  $('#' + index).attr("data-event", index);
  $('#' + index).attr("data-start", appointment.HourStart);
  $('#' + index).attr("data-end", appointment.HourEnd);
  $('#' + index).attr("data-event", "event-"+dayCounter(appointment.Day));
  let event = "<span class=\"event-name\">" + appointment.Name + " " + appointment.Surname + "<br/>" + appointment.HourStart + " - " + appointment.HourEnd + "<br/>" + "<em> House: " + appointment.House + "</em>" + "</span>"
  $('#' + index).append("<a>" + event + "</a>")


  // dayContainer.append($('<li/>', {
  //   text: "HEllo!"
  // }))

  // dayContainer.append("<li class=\"single-event\">"+ appointment.Name +"</li>")
  

  // <li class="single-event" data-start="12:00" data-end="13:45" data-content="event-restorative-yoga"
  //   data-event="event-4">
  //   <a href="#0">
  //     <span class="event-name">Restorative Yoga</span>
  //   </a>
  // </li>
}



// obj = JSON.parse(json);

// console.log(obj.count);
// // expected output: 42

// console.log(obj.result);
// // expected output: true