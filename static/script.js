const inputFile = document.getElementById("dropzone-file");
const fileLabel = document.querySelector("#fileLabel");

inputFile.addEventListener("change", function() {
  let fileNames = "";
  for (let i = 0; i < inputFile.files.length; i++) {
    fileNames += inputFile.files[i].name + ", ";
  }
  fileNames = fileNames.slice(0, -2);
  fileLabel.innerHTML = fileNames || "Clique para selecionar";
});

// Prevent the default drag behavior
document.addEventListener('dragover', (event) => {
  event.preventDefault();
});

// Handle the file drop
document.addEventListener('drop', (event) => {
  event.preventDefault();
  const files = event.dataTransfer.files;
  inputFile.files = files;
  const changeEvent = new Event('change');
  inputFile.dispatchEvent(changeEvent);
});

