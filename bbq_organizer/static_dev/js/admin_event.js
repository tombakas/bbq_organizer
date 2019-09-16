var confirmModal = document.getElementById("confirm-modal");

document.getElementById("delete-event").onclick = function() {
  confirmModal.classList.add("is-active");
};

function closeModal() {
  confirmModal.classList.remove("is-active");
};

document.getElementsByClassName("modal-close")[0].onclick = closeModal;
document.getElementsByClassName("cancel-delete")[0].onclick = closeModal;

var confirmDelete = document.getElementsByClassName("confirm-delete")[0];
confirmDelete.onclick = function() {
  fetch("/events/delete/", {
    method: 'POST', // or 'PUT'
    body: JSON.stringify({
      slug: confirmDelete.getAttribute("data-slug")
    }),
    headers:{
      'Content-Type': 'application/json'
    }
  }).then()
    .then((resp) => {
      if (resp.status == 200) {
        window.location = "/";
      }
    })
    .catch(error => console.log(error));
};
