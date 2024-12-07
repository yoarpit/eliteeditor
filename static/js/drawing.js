const uploadForm = document.getElementById("upload-form");
const imagePreview = document.getElementById("image-preview");
const actions = document.getElementById("actions");

let currentImage = null;
let drawing = false;
let ctx;

uploadForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(uploadForm);
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        currentImage = data.filename;
        imagePreview.src = data.file_url;
        initCanvas();
    });
});

actions.addEventListener("click", function (e) {
    const action = e.target.dataset.action;
    if (action) {
        handleAction(action);
    }
});

function handleAction(action) {
    // Handle drawing and other actions
}

function initCanvas() {
    const canvas = document.createElement('canvas');
    canvas.width = imagePreview.width;
    canvas.height = imagePreview.height;
    imagePreview.parentElement.appendChild(canvas);
    ctx = canvas.getContext('2d');
    ctx.drawImage(imagePreview, 0, 0);
}

function draw(x, y, size, color) {
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
}