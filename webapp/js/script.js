/**
 * Retrieves input data from a form and returns it as a JSON object.
 * @param  {HTMLFormControlsCollection} elements  the form elements
 * @return {Object}                               form data as an object literal
 */
// const formToJSON = elements => [].reduce.call(elements, (data, element) => {

//   data[element.name] = element.value;
//   return data;

// }, {});


/**
 * Checks if an element’s value can be saved (e.g. not an unselected checkbox).
 * @param  {Element} element  the element to check
 * @return {Boolean}          true if the value should be added, false if not
 */


const isValidValue = element => {
  return (!['checkbox', 'radio'].includes(element.type) || element.checked);
};

const isValidElement = element => {
  return element.name && element.value;
};

const isCheckbox = element => element.type === 'checkbox';

const formToJSON = elements => {
  const reducerFunction = (data, element) => {

    // Make sure the element has the required properties and should be added.
    if (isValidElement(element) && isValidValue(element)) {

      if (isCheckbox(element)) {
        // Add the current field to the array if more than one can be selected
        data[element.name] = (data[element.name] || []).concat(element.value);
      } else {
        // Add the current field to the object.
        data[element.name] = element.value;
      }
    }

    console.log(JSON.stringify(data));

    return data;
  }

  // This is used as the initial value of `data` in `reducerFunction()`.
  const reducerInitialValue = {};


  // Now we reduce by `call`-ing `Array.prototype.reduce()` on `elements`.
  const formData = [].reduce.call(elements, reducerFunction, reducerInitialValue);

  // The result is then returned for use elsewhere.
  return formData;
}




function formValidation() {

  // Stop the form from submitting since we’re handling that with AJAX.
  event.preventDefault();

  checkedDays = $("#days-form:checked").length;
  checkedPref = $("#pref-form:checked").length;

  if (!checkedDays) {
    alert("You must select at least one day.");
  }
  else {
    if (!checkedPref) {
      alert("You must select at least one preference for time of day.");
    }
    else {
      handleFormSubmit();
    }
  }
  
}


/**
 * A handler function to prevent default submission and run our custom script.
 * @param  {Event} event  the submit event triggered by the user
 * @return {void}
 */
const handleFormSubmit = event => {

  // Call our function to get the form data.
  const data = formToJSON(form.elements);
  console.log(data);

  // Use `JSON.stringify()` to make the output valid, human-readable JSON.
  dataContainer = JSON.stringify(data);

  console.log(dataContainer);

  $.ajax({
    type: "POST",
    url: "serverUrl",
    data: dataContainer,
    success: function () { },
    dataType: "json",
    contentType: "application/json"
  });
};

const form = document.getElementById('appointmentRequest');
form.addEventListener('submit', formValidation);



// function sendData() {


//   var formData = JSON.stringify($("#appointmentRequest").serializeArray());

//   $.ajax({
//     type: "POST",
//     url: "serverUrl",
//     data: formData,
//     success: function () { },
//     dataType: "json",
//     contentType: "application/json"
//   });
// }



