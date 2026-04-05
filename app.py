# ================= BACKEND (Python - Flask) ===============
from system import *


if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


def format_manga_name(name):
    # convert "kaiju no 8" -> "kaiju_no_8"
    return name.lower().strip().replace(" ", "_")


def download_manga_async(manga, chapter):
    manga = format_manga_name(manga)
    folder = os.path.join(SAVE_DIR, f"{manga}_{chapter}")

    os.makedirs(folder, exist_ok=True)

    key = f"{manga}_{chapter}"
    download_status[key] = {"complete": False, "error": False}

    page = 1
    downloaded = 0

    while True:
        url = f"{BASE_URL}/{manga}/{manga}_{chapter}/{manga}_{chapter}_{page}.jpg"
        try:
            res = requests.get(url, timeout=10)

            if res.status_code != 200:
                break

            img_path = os.path.join(folder, f"{page}.jpg")

            with open(img_path, "wb") as f:
                f.write(res.content)

            page += 1
            downloaded += 1

        except:
            break

    
    if downloaded == 0:
        try:
            if os.path.exists(folder):
                os.rmdir(folder)  # remove empty folder
        except:
            pass

        download_status[key]["error"] = True
        download_status[key]["complete"] = False
        return
    
    download_status[key]["complete"] = True


@app.route("/fetch", methods=["POST"])
def fetch():
    data = request.json
    manga = format_manga_name(data["manga"])
    chapter = data["chapter"]

    key = f"{manga}_{chapter}"
    folder = os.path.join(SAVE_DIR, key)

    # Start background download if not started
    if key not in download_status:
        threading.Thread(target=download_manga_async, args=(manga, chapter), daemon=True).start()
    
    # If error occurred
    if download_status.get(key, {}).get("error"):
        return jsonify({
            "images": [],
            "complete": False,
            "error": True
        })
    

    # Get currently downloaded images
    if os.path.exists(folder):
        files = sorted(
            [f for f in os.listdir(folder) if f.endswith(".jpg")],
            key=lambda x: int(x.split(".")[0])
        )
        images = [f"{key}/{f}" for f in files]
    else:
        images = []

    return jsonify({
        "images": images,
        "complete": download_status.get(key, {}).get("complete", False),
        "error": False
    })


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    manga = format_manga_name(data["manga"])
    chapter = data["chapter"]

    folder = os.path.join(SAVE_DIR, f"{manga}_{chapter}")

    if not os.path.exists(folder):
        return jsonify({"error": "Manga not downloaded yet"}), 400

    files = [f for f in os.listdir(folder) if f.endswith(".jpg")]
    files.sort(key=lambda x: int(x.split(".")[0]))

    image_paths = [os.path.join(folder, f) for f in files]

    pdf_path = os.path.join(folder, f"{manga}_{chapter}.pdf")

    images = []

    for img_path in image_paths:
        try:
            img = Image.open(img_path).convert("RGB")
            images.append(img)
        except:
            continue

    if not images:
        return jsonify({"error": "No images found"}), 400

    # Create PDF
    images[0].save(pdf_path, save_all=True, append_images=images[1:])

    # Safe delete function
    def safe_delete(path):
        time.sleep(60)  # wait 1 minute

        retries = 5
        for attempt in range(retries):
            try:
                if os.path.exists(path):
                    os.remove(path)
                    cleanup_logger.info(f"Deleted PDF: {path}")
                    return
            except PermissionError:
                cleanup_logger.warning(f"File in use, retry {attempt+1}: {path}")
                time.sleep(5)
            except Exception as e:
                cleanup_logger.error(f"Unexpected error deleting {path}: {e}")
                return

        cleanup_logger.error(f"Failed to delete after retries: {path}")

    #  Run cleanup in background
    threading.Thread(target=safe_delete, args=(pdf_path,), daemon=True).start()

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{manga}_{chapter}.pdf"
    )


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(SAVE_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True, port=2400)
