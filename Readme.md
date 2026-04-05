# 📚 MangaCloud (Download & Read Manga)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)
![UI](https://img.shields.io/badge/UI-Canvas%20Reader-orange)

A powerful **Flask + JavaScript** web app to download, read, and export manga chapters with a smooth in-browser reader.

---

## 🚀 Features

### 🖼️ Interactive Manga Reader
- Displays manga at canvas to read
- Canvas-based rendering for smooth viewing
- Shows **loading screen** if next page is not ready
- Supports **Prev / Next navigation**

---

### ⚡ Background Download System
- Downloads manga in **background thread**
- Real-time updates using polling
- No UI blocking or freezing

---

### 📄 PDF Export
- Generate PDF from downloaded images
- Safe cleanup with retry system
- Logging supported (`cleanup.log`)

---

### 🎯 Smart UI Controls
- ⬇ Download button 
- ⬅➡ Navigation button

---


---

## ⚙️ Installation

### 1️⃣ Install Dependencies
```bash
pip install flask requests pillow
```

### 2️⃣ Run Application
```bash
python app.py
```

### 3️⃣ Open in Browser
```bash
http://127.0.0.1:2400
```

---

## 🎮 Usage

### 1️⃣ Enter manga name
- 👉 Example: naruto
### 2️⃣ Enter chapter
- 👉 Example: 1
### 3️⃣ Click Fetch
### 4️⃣ Start reading instantly ⚡
### 5️⃣ Download PDF

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Rendering:** HTML5 Canvas API  
- **Image Processing:** Pillow  
- **HTTP Requests:** Python Requests  

---

## ❌ Canvas Not Displaying

- Ensure the Flask server is running  
- Check if images are being downloaded in the background  
- Verify correct API endpoint (`/fetch`) is being called  
- Open browser console (F12) and check for errors  
- Make sure JavaScript file is correctly loaded from `/static`  

---

## ❌ Manga Not Loading

- Check if the manga name is correct (use lowercase, proper format)  
- Ensure the chapter number exists  
- Verify internet connection  
- If manga is invalid, the app will display **"Manga not available"**  
- Check backend logs for request errors  

---

## ⚠️ Disclaimer

- This project uses publicly available manga image sources  
- It is intended for **educational and personal use only**  
- Do not use this project for redistribution or commercial purposes  