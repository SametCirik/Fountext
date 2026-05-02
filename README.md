<p align="center">
  <a href="./README.md">
    <img src="[https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/gb.svg](https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/gb.svg)" alt="English" width="40">
  </a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="./README_tr.md">
    <img src="[https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/tr.svg](https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/tr.svg)" alt="Türkçe" width="40">
  </a>
</p>

<h1 align="center">Fountext Screenwriting Editor for Linux</h1>

<p align="center">
  <strong>A blazing fast, professional screenwriting environment built with Python, PyQt6, and a custom C++ layout engine.</strong>
</p>

---

## 🎬 What is Fountext?

Fountext is a modern, lightweight, and powerful screenwriting editor that fully embraces the **Fountain** syntax. Forget about formatting struggles; just write. Fountext's custom-built C++ rendering engine instantly parses your text and paginates it into industry-standard script format in real-time.

| ![Fountext Workspace](RESİM_LINKI_BURAYA_1) |
| :---: |
| *Fountext Editor Workspace & Real-time Formatting* |

## ✨ Key Features (v1.2)

* **C++ Powered Layout Engine:** A bespoke backend that handles pagination, line-wrapping, and cursor positioning with pinpoint accuracy.
* **Smart Selection & Highlighting:** Native-feeling text selection with a custom amber/gold theme, perfectly synced between the UI and the C++ backend.
* **Project Dashboard:** Organize your scripts by episodes and projects effortlessly.
* **Schema (Detective Board):** Visualize your plot points, character arcs, and scenes in a node-based environment.
* **Flawless PDF Export:** Generate pristine, industry-standard PDFs ready for production. Highlights and cursors are intelligently hidden during export.
* **Dynamic Viewport Footer:** The status bar smartly tracks which page is currently most visible on your screen.
* **Multilanguage UI:** Full support for English, Turkish, French, Spanish, and Russian.

| ![Project Dashboard](RESİM_LINKI_BURAYA_2) |
| :---: |
| *Project Management & Episode Dashboard* |

## 🚀 Installation (Linux)

Fountext is currently optimized for Linux environments.

**1. Clone the repository or download the latest release:**

[Buraya kod bloğu işareti gelecek - bash]
wget [https://github.com/SametCirik/Fountext-Screenwriting-Editor/releases/download/v1.2.0/Fountext-v1.2-Linux.tar.gz](https://github.com/SametCirik/Fountext-Screenwriting-Editor/releases/download/v1.2.0/Fountext-v1.2-Linux.tar.gz)
tar -xzvf Fountext-v1.2-Linux.tar.gz
cd Fountext
[Buraya kod bloğu işareti kapanışı gelecek]

**2. Set up a virtual environment and install dependencies:**

[Buraya kod bloğu işareti gelecek - bash]
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
[Buraya kod bloğu işareti kapanışı gelecek]

**3. Run Fountext:**

[Buraya kod bloğu işareti gelecek - bash]
python src/main.py
[Buraya kod bloğu işareti kapanışı gelecek]

| ![Schema Board](RESİM_LINKI_BURAYA_3) |
| :---: |
| *Schema Editor - Map out your story* |

## 🛠 Building the C++ Engine from Source

If you need to recompile the fountext_engine, ensure you have g++ and pybind11 installed:

[Buraya kod bloğu işareti gelecek - bash]
cd src_cpp
g++ -O3 -Wall -shared -std=c++17 -fPIC $(python -m pybind11 --includes) bindings.cpp layout_engine.cpp -o ../src/fountext_engine$(python-config --extension-suffix)
[Buraya kod bloğu işareti kapanışı gelecek]

## 📜 License
Copyright (c) 2026 Samet Cırık. All rights reserved.