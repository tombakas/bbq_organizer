var register = document.getElementById("register");

register.onclick = function addMeat() {
  extras = document.getElementById("extras");
  meats = document.getElementsByClassName("meat-option");
  var location = document.URL.split("/");
  var slug = location[location.length - 1];
  console.log(slug);

  var chosen = [];

  for (var meat of meats) {
    if (meat.checked) {
      chosen.push(meat.value);
    }
  }

  var body = {
    meats: chosen,
    extras: extras.value
  };

  fetch(`/events/invite/register/${slug}`, {
    method: 'POST', // or 'PUT'
    body: JSON.stringify(body), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  }).then()
    .then(response => window.location= "/thank_you")
    .catch(error => console.log(error));
};
