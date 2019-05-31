// Function to handle forms and send content as JSON via ajax to the server


// validate form to ensure all fields have been filled in
function formValidation() {

  // stop the form from submitting since we’re handling that with AJAX
  event.preventDefault();


  checkedDays = $("#days-form:checked").length;
  checkedPref = $("#pref-form:checked").length;

  if (!checkedDays) {
    alert("You must select at least one day.");
  }
  else {
      // if everything is validated then process the form
      handleFormSubmit();
  }
}




// check if the element is valid
const isValidElement = element => {
  // both `name` and `value` properties must be non-empty
  return element.name && element.value;
};

// check if checkable fields are valid
const isValidValue = element => {
  // only checked elements are accepted 
  return (!['checkbox', 'radio'].includes(element.type) || element.checked);
};

// check if the element is a checkbox
const isCheckbox = element => element.type === 'checkbox';



// function to create a JSON string from the form elements
const formToJSON = elements => {

  // concatenate in *data* each `element`, making the necessary modifications
  const reducerFunction = (data, element) => {

    // make sure the element is valid and should be added
    if (isValidElement(element) && isValidValue(element)) {

      if (isCheckbox(element)) {
        // checkbox can have multiple values: store them in a list
        // concatenate the current value to the `data` dict, with key = element.name
        // either in the existing list or creating a new empty one

        dayPref = element.value.split(',');

        if (data[element.name] != null) {
          data[element.name].push(dayPref);
        }
        else {
          data[element.name] = [];
          data[element.name].push(dayPref);
        }

      } else {
        // add the current element to the dict `data`
        data[element.name] = element.value;
      }
    }

    return data;
  }

  // initial value of `data` in `reducerFunction()`
  const reducerInitialValue = {};


  // reduce by call Array.prototype.reduce()` on `elements`
  const formData = [].reduce.call(elements, reducerFunction, reducerInitialValue);

  return formData;
}




// handle the form content, parse it into JSON and send to the server
const handleFormSubmit = event => {


  // get the form data
  const data = formToJSON(form.elements);
  
  // `JSON.stringify()` to make the output valid, human-readable JSON
  dataContainer = JSON.stringify(data);

  // send via ajax to the webservice `/requestAppointment`
  $.ajax({
    type: "POST",
    url: "/requestAppointment",
    data: dataContainer,
    success: function () { },
    dataType: "json",
    contentType: "application/json"
  });

  window.location.href = "/html/requestAppointment.html";

};

const form = document.getElementById('appointmentRequest');
form.addEventListener('submit', formValidation);


