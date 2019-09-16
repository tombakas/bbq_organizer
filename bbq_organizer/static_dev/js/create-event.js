var meats = {};
var select = document.getElementById("meat-select");
var chosen = document.getElementById("meats-chosen");

function removeMeat(item) {
  var target = item.target;
  var id = target.id.split("-")[1];

  meats[id] = false;
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
  var meat = select[select.selectedIndex];

  if (meats[meat.value] === undefined || meats[meat.value] === false) {
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
    chosen.appendChild(entry);

    meats[meat.value] = true;
  }
};
