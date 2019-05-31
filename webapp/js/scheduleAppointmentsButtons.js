document.getElementById("empty-schedule").addEventListener("click", function (event) {

  if (confirm("Are you sure you want to delete scheduled appointments?\nThis action can't be reversed.")) {
    $.ajax({
      type: 'GET',
      url: '/emptySchedule',
      success: function () {

        // delete existing appointments from html
        var dayContainer = $(".events-group > ul");
        Array.from(dayContainer).forEach(day => {
          day.innerHTML = "";
        });

        // delete existing not scheduled appointments from html
        var notScheduledContainer = $('.not-scheduled-event');
        Array.from(notScheduledContainer).forEach(event => {
          event.outerHTML = "";
        });

        // delete not scheduled appointments title
        if ($('#not-scheduled > h2').get(0) != null) {
          $('#not-scheduled > h2').get(0).outerHTML = "";
        }

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

  if ($("#num-requests-form")[0].value != "") {

    if (confirm("Are you sure you want to generate random requested appointments?\nThis action will override the current requests and can't be reversed.")) {

      // stop the form from submitting since we’re handling that with AJAX
      event.preventDefault();

      const numReq = $("#randomRequests").serializeArray()[0];

      $.ajax({
        type: 'POST',
        url: '/randomRequests',
        data: numReq.value,
        success: function () {
          alert("Requests generated!");
        }
      });

      $("#num-requests-form")[0].value = ""
    }
  }


});