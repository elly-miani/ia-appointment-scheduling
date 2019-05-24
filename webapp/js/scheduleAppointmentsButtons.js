document.getElementById("empty-schedule").addEventListener("click", function (event) {

  if (confirm("Are you sure you want to delete scheduled appointments?\nThis action can't be reversed.")) {
    $.ajax({
      type: 'GET',
      url: '/emptySchedule',
      success: function () {

        // delete existing appointments from html
        var dayContainer = $(".events-group > ul");
        console.log(dayContainer);
        Array.from(dayContainer).forEach(day => {
          day.innerHTML = "";
        });

        // delete existing not scheduled appointments from html
        var notScheduledContainer = $('.not-scheduled-event');
        Array.from(notScheduledContainer).forEach(event => {
          event.outerHTML = "";
        });

        alert("Scheduled appointments deleted!")
      }
    });
  }
});


document.getElementById("empty-requests").addEventListener("click", function (event) {

  if (confirm("Are you sure you want to delete requested appointments?\nThis action can't be reversed.")) {
    $.ajax({
      type: 'GET',
      url: '/emptyRequests',
      success: function () {
        alert("Requests deleted!");
      }
    });
  }
});

document.getElementById("generate-random-requests").addEventListener("click", function (event) {

  if (confirm("Are you sure you want to generate random requested appointments?\nThis action will override the current requests and can't be reversed.")) {
    $.ajax({
      type: 'GET',
      url: '/randomRequests',
      success: function () {
        alert("Requests generated!");
      }
    });
  }
});