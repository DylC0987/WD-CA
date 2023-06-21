// Get the button and modal elements
let infoButton = document.querySelector("#infoButton");
let infoModal = document.querySelector("#infoModal");

// When the button is clicked, show the modal
infoButton.addEventListener("click", function() {
  infoModal.style.display = "block";
});

// When the close button is clicked, hide the modal
let closeButton = infoModal.querySelector(".close");
closeButton.addEventListener("click", function() {
  infoModal.style.display = "none";
});

// When the user clicks outside the modal, hide it
window.addEventListener("click", function(event) {
  if (event.target === infoModal) {
    infoModal.style.display = "none";
  }
});
