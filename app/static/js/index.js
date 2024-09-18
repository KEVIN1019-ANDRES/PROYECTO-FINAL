var mainListDiv = document.getElementById("mainListDiv");
var mediaButton = document.getElementById('mediaButton');

mediaButton.onclick = function () {
    mainListDiv.classList.toggle('show_list');
    mediaButton.classList.toggle('active');
}
