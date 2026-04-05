import os
import requests
from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from PIL import Image

import threading
import time
import logging

download_status = {}  # global tracker


cleanup_logger = logging.getLogger("cleanup_logger")
cleanup_logger.setLevel(logging.INFO)

handler = logging.FileHandler("cleanup.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
cleanup_logger.addHandler(handler)

cleanup_logger.propagate = False  # VERY IMPORTANT

BASE_URL = "https://images.mangafreak.me/mangas"
SAVE_DIR = "manga_collection"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")



