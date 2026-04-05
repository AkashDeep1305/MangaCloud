
let images = [];
let loadedImages = {};
let index = 0;
let isComplete = false;
let isData = false;

const BASE = "http://127.0.0.1:2400";

async function fetchManga() {
    document.getElementById('status').innerText = "loading...";

    const manga = document.getElementById('manga').value;
    const chapter = document.getElementById('chapter').value;

    index = 0;
    loadedImages = {};
    images = [];

    startPolling(manga, chapter);
}

function startPolling(manga, chapter) {
    const interval = setInterval(async () => {
        const res = await fetch(`${BASE}/fetch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ manga, chapter })
        });

        const data = await res.json();

        images = data.images;
        isComplete = data.complete;
        isData = data.error;

        if (isData) {
            document.getElementById('status').innerText = "Manga / Chapter not available..";

            drawLoading("Manga not available");

            clearInterval(interval);
            return
        }

        // Show once 5 images available
        if (images.length >= 5 && index === 0) {
            preloadInitial();
        }

        updateDownloadButton();

        if (isComplete) {
            document.getElementById('status').innerText = " ";
            clearInterval(interval);
        }

    }, 2000); // every 2 sec
}

function preloadInitial() {
    let count = 0;
    let limit = Math.min(5, images.length);

    for (let i = 0; i < limit; i++) {
        loadImage(i, () => {
            count++;
            if (count === limit) {
                document.getElementById('status').innerText = "";
                showPage();
            }
        });
    }
}

function loadImage(i, callback) {
    if (loadedImages[i]) {
        callback && callback();
        return;
    }

    const img = new Image();
    img.src = `${BASE}/images/${images[i]}?t=${Date.now()}`; // cache fix

    img.onload = () => {
        loadedImages[i] = img;
        callback && callback();
    };

    img.onerror = () => {
        console.log("Retry loading:", i);
        setTimeout(() => loadImage(i, callback), 1000); // retry
    };
}

function drawLoading(text = "Loading...") {
    const canvas = document.getElementById('viewer');
    const ctx = canvas.getContext('2d');

    canvas.height = 400;

    ctx.fillStyle = "#1e293b";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.textAlign = "center";
    ctx.fillText(text, canvas.width / 2, canvas.height / 2);
}

function showPage() {
    if (!images.length) return;

    const canvas = document.getElementById('viewer');
    const ctx = canvas.getContext('2d');

    if (loadedImages[index]) {
        const img = loadedImages[index];
        canvas.height = img.height * (600 / img.width);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        return;
    }

    drawLoading("Loading page...");

    loadImage(index, () => {
        showPage();
    });
}

function nextPage() {
    if (isData) {
        drawLoading("Manga not available.");
        return
    }


    if (index < images.length - 1) {
        index++;
        showPage();
    } else if (!isComplete) {
        drawLoading("loading more pages...");
        fetchMore(); // get more pages
    }
    else {
        drawLoading("No more pages.")
    }
}

function prevPage() {
    if (index > 0) {
        index--;
        showPage();
    }
}

// Fetch more pages dynamically
async function fetchMore() {
    const manga = document.getElementById('manga').value;
    const chapter = document.getElementById('chapter').value;

    const res = await fetch(`${BASE}/fetch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ manga, chapter })
    });

    const data = await res.json();

    images = data.images;
    isComplete = data.complete;

    updateDownloadButton();
    showPage();
}

// Show button only when fully downloaded
function updateDownloadButton() {
    const btn = document.querySelector("button[onclick='downloadPDF()']");
    if (!btn) return;

    if (isComplete) {
        btn.style.display = "inline-block";
    } else {
        btn.style.display = "none";
    }
}

async function downloadPDF() {
    const manga = document.getElementById('manga').value;
    const chapter = document.getElementById('chapter').value;

    const res = await fetch(`${BASE}/download`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ manga, chapter })
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `${manga}_${chapter}.pdf`;
    a.click();
}