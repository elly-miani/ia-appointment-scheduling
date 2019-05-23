$(document).ready(function () {
  // on page load call the showAppointments webservice, which will return the current schedule in json

  $.ajax({
    type: 'GET',
    url: '/showAppointments',
    dataType: 'json',
    success: function (data) {

      // create appointments in html code
      $.each(data, function (index, appointment) {
        console.log(appointment);
        createAppointment(index, appointment);
      })

      // refresh appointments on calendar
      scheduleEverything();
    }
  });
});



document.getElementById("compute-schedule").addEventListener("click", function () {
  // on click of button "Compute Schedule"

  // delete existing appointments from html
  var dayContainer = $(".events-group > ul");
  console.log(dayContainer);
  Array.from(dayContainer).forEach(day => {
    day.innerHTML = "";
  });

  // reset daily count to set correct colors to elements
  count = [1, 1, 1, 1, 1];

  // call scheduleAppointments webservice, which will run the solver and return the output file in json
  $.ajax({
    type: 'POST',
    url: '/scheduleAppointments',
    dataType: 'json',
    success: function (data) {

      // create appointments in html code
      $.each(data, function (index, appointment) {
        console.log(appointment);
        createAppointment(index, appointment);
      })

      // refresh appointments on calendar
      scheduleEverything();

      // scroll to calendar
      $('html, body').animate(
        {
          scrollTop: $("#schedule-calendar").offset().top,
        },
        500,
        'linear'
      )
    }
  });
});




// helper function to keep count of scheduled appointments for each day
// needed for scheduleStructure.js to add colors correctly
var count = [1, 1, 1, 1, 1];

function dayCounter(day) {
  if (day == "mon") {
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



function createAppointment(index, appointment) {
  // add each appointment with its data to the correct day list in the html code
  var dayContainer = $('#' + appointment.Day + '> ul');
  
  dayContainer.append($('<li/>', {
    id: index,
    class: 'single-event'
  }))

  // update loading status when adding appointments after they were already loaded once
  // needed to ensure correct functioning of placeEvents() function in scheduleStructure.js
  $(".cd-schedule").removeClass('js-full');
  $(".cd-schedule").addClass('loading');

  console.log("index:" + index);
  $('#' + index).attr("data-event", index);
  $('#' + index).attr("data-start", appointment.HourStart);
  $('#' + index).attr("data-end", appointment.HourEnd);
  $('#' + index).attr("data-event", "event-"+dayCounter(appointment.Day));
  // let event = "<span class=\"event-name\">" + appointment.Name + " " + appointment.Surname + "<br/>" + appointment.HourStart + " - " + appointment.HourEnd + "<br/>" + "<em> House: " + appointment.House + "</em>" + "</span>"
  let event = "<span class=\"event-name\">" + appointment.Name + " " + appointment.Surname + "<br/>" + "<em> House: " + appointment.House + "</em>" + "</span>"
  $('#' + index).append("<a href=\"#0\">" + event + "</a>")
}