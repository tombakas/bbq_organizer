import bulmaCalendar from 'bulma-calendar/dist/js/bulma-calendar.min.js';
import '../scss/create_event.scss';

var meats = {};
var choice = document.getElementById("meat-select");
var meatsChosen = document.getElementById("meats-chosen");
var entries = document.getElementsByClassName("entry");


for (var item of entries) {
  var children = item.children;
  var id = children[1].id.split("-")[1];
  children[1].onclick = removeMeat;
  meats[id] = {
    selected: true,
    name: children[0].innerHTML
  };
}

function removeMeat(item) {
  var target = item.target;
  var id = target.id.split("-")[1];

  meats[id].selected = false;
  target.parentElement.remove();
}

function checkIfSelected() {
  for (meat in meats) {
    if (meat) {
      return true;
    }
  }
  return false;
}

var form = document.getElementById("create-event-form");
form.onsubmit = function(event) {
  event.preventDefault();

  var input = document.createElement("input");
  input.setAttribute("type", "hidden");
  input.setAttribute("name", "meats");
  input.setAttribute("value", JSON.stringify(meats));

  form.appendChild(input);
  form.submit();
};

document.getElementById("add-meat").onclick = function addMeat() {
  var meat = choice[choice.selectedIndex];

  if (meats[meat.value] === undefined || meats[meat.value].selected === false) {
    var entry = document.createElement("div");
    var name = document.createElement("span");
    var button = document.createElement("div");

    entry.classList.add("entry");

    name.innerHTML = meat.text;

    button.classList.add("button", "is-danger");
    button.id = `meat-${meat.value}`;
    button.innerHTML = "-";
    button.onclick = removeMeat;

    entry.appendChild(name);
    entry.appendChild(button);
    meatsChosen.appendChild(entry);

    meats[meat.value] = {
      selected: true,
      name: meat.innerHTML
    };
  }
};

// Set up bulma calendar
var options = {
  type: "date",
  dateFormat: "YYYY-MM-DD",
  displayMode: "default"
};

bulmaCalendar.attach('[type="date"]', options);
