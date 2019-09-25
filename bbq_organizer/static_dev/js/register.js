var register = document.getElementById("register");
var extras = document.getElementById("extras");
var name = document.getElementById("name");
var meats = document.getElementsByClassName("meat-option");
var location = document.URL.split("/");
var slug = location[location.length - 1];
var nameEror = document.getElementById("no-name-error");
var numberError = document.getElementById("invalid-number-error");

register.onclick = function addMeat() {
  nameEror.classList.add("is-hidden");
  numberError.classList.add("is-hidden");

  if (checkErrors() === true) {
    return;
  }

  var chosen = [];
  for (var meat of meats) {
    if (meat.checked) {
      chosen.push(meat.value);
    }
  }

  var body = {
    meats: chosen,
    extras: extras.value,
    name: name.value
  };

  fetch(`/events/invite/register/${slug}`, {
    method: 'POST',
    body: JSON.stringify(body),
    headers:{
      'Content-Type': 'application/json'
    }
  }).then()
    .then(resp => {
      if (resp.status == 200) {
        window.location = "/thank_you";
      } else if (resp.status == 404){
        window.location = "/does_not_exist";
      } else if (resp.status == 403) {
        window.location = "/already_registered";
      } else if (resp.status == 400) {
        resp.text().then(text =>{
          if (text === "name cannot be blank") {
            nameEror.classList.remove("is-hidden");
          }
          if (text === "invalid numeric value") {
            numberError.classList.remove("is-hidden");
          }
        });
      }
    })
    .catch(error => console.log(error));
};

function checkErrors() {
  var errorState = false;

  if (name.value === "") {
    nameEror.classList.remove("is-hidden");
    errorState = true;
  }

  if (isNaN(extras.value)) {
    numberError.innerHTML = "Invalid numeric value";
    numberError.classList.remove("is-hidden");
    errorState = true;
  }

  if (!isNaN(extras.value) && extras.value < 0) {
    numberError.innerHTML = "Extras cannot be less than zero";
    numberError.classList.remove("is-hidden");
    errorState = true;
  }
}
