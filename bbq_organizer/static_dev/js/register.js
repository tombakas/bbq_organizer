var register = document.getElementById("register");

register.onclick = function addMeat() {
  var extras = document.getElementById("extras");
  var name = document.getElementById("name");
  var meats = document.getElementsByClassName("meat-option");
  var location = document.URL.split("/");
  var slug = location[location.length - 1];

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
    method: 'POST', // or 'PUT'
    body: JSON.stringify(body), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  }).then()
    .then((resp) => {
      if (resp.status == 200) {
        window.location = "/thank_you";
      } else if (resp.status == 404){
        window.location = "/does_not_exist";
      } else if (resp.status == 400) {
        window.location = "/already_registered";
      }
    })
    .catch(error => console.log(error));
};
