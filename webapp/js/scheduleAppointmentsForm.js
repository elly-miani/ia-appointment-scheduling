var notScheduledAppointments;

$(document).ready(function () {
  // on page load call the showAppointments webservice, which will return the current schedule in json
  
  notScheduledAppointments = false;

  $.ajax({
    type: 'GET',
    url: '/showAppointments',
    dataType: 'json',
    success: function (data) {

      // create appointments in html code
      $.each(data, function (index, appointment) {
        createAppointment(index, appointment);
      })

      // refresh appointments on calendar
      scheduleEverything();
    }
  });
});


document.getElementById("compute-schedule").addEventListener("click", function (event) {
  // on click of button "Compute Schedule"

  const formData = $("#timeout-form").serializeArray()[0];


  // stop the form from submitting since we’re handling that with AJAX
  if ($("#timeout-form")[0].value != "") {
    event.preventDefault();

    // delete existing appointments from html
    var dayContainer = $(".events-group > ul");
    Array.from(dayContainer).forEach(day => {
      day.innerHTML = "";
    });

    // delete existing not scheduled appointments from html
    var notScheduledEvents = $('.not-scheduled-event');
    Array.from(notScheduledEvents).forEach(event => {
      event.outerHTML = "";
    });

    // delete not scheduled appointments title
    if ($('#not-scheduled > h2').get(0) != null) {
      $('#not-scheduled > h2').get(0).outerHTML = "";
    }

    // initialize notScheduledAppointments variable
    notScheduledAppointments = false;

    // reset daily count to set correct colors to elements
    count = [1, 1, 1, 1, 1];

    // call scheduleAppointments webservice, which will run the solver and return the output file in json
    $.ajax({
      type: 'POST',
      url: '/scheduleAppointments',
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(formData),
      dataType: 'json',
      success: function (data) {

        // create appointments in html code
        $.each(data, function (index, appointment) {
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
  }
  else {}

  $("#timeout-form")[0].value = ""
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

// dictionary to quickly render right text based on the values passed by the server
daysDict = { "mon": "Monday", "tue": "Tuesday", "wed": "Wednesday", "thu": "Thursday", "fri": "Friday" }


function createAppointment(index, appointment) {
  // add each appointment with its data to the correct day list in the html code

  if (appointment.Status != null) {
    // if the appointment is not scheduled

    var notScheduledContainer = $('#not-scheduled');

    if (notScheduledAppointments === false) {
      notScheduledContainer.append("<h2>Not scheduled appointments:</h2>");
      notScheduledAppointments = true;
    }

    // create new `not-scheduled` appointment div
    notScheduledContainer.append($('<div/>', {
      id: index,
      class: 'not-scheduled-event'
    }));

    constraints = "<div><ul>";
    // for each appointment constraint add a list item with the day (using the daysDict) and the time of day
    appointment.Day.forEach(x => {
      constraints += "<li>" + daysDict[x[0]] + " " + x[1] + "</li>";
    });
    constraints += "</ul></div>";

    // create the event html
    let event = "<h3>" + appointment.Name + " " + appointment.Surname + "</h3>" + "<em> House: " + appointment.House + "</em>" + "<br/> <h5> Requested constraints: </h5>" + constraints;

    // append to the correct event div
    $('#' + index).append(event) + "</span>";

  }
  else {
    // if the appointment is scheduled

    var dayContainer = $('#' + appointment.Day + '> ul');

    // create new appointment <li>
    dayContainer.append($('<li/>', {
      id: index,
      class: 'single-event'
    }))

    $('#' + index).attr("data-event", index);
    $('#' + index).attr("data-start", appointment.HourStart);
    $('#' + index).attr("data-end", appointment.HourEnd);
    $('#' + index).attr("data-event", "event-" + dayCounter(appointment.Day));

    // create the event html
    let event = "<span class=\"event-name\">" + appointment.Name + " " + appointment.Surname + "<br/>" + "<em> House: " + appointment.House + "</em>" + "</span>";

    // append to the correct event div
    $('#' + index).append("<a href=\"#0\">" + event + "</a>");
  }

  // update loading status when adding appointments after they were already loaded once
  // needed to ensure correct functioning of placeEvents() function in scheduleStructure.js
  $(".cd-schedule").removeClass('js-full');
  $(".cd-schedule").addClass('loading');
  
}