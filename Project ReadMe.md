# **📊 Pixel Tracker for Google Gemini**

A sleek, standalone Windows 11 utility designed to solve a specific problem: **tracking the "invisible" daily image generation limits in Google Gemini.**

## **💡 The Story**

As a frequent user of Google Gemini, I found it frustrating that there was no "fuel gauge" for my daily image generations. After hitting the 100-image limit one too many times without warning, I decided I needed a dedicated counter that could stay pinned on my screen while I worked.

Since I am new to coding, I collaborated with **Gemini (Google's AI)** to build this from scratch. I provided the vision and specific feature requests—like the "fraction display" and the "highlighted countdown mode"—while Gemini helped me write the Python logic to make it a reality.

## **✨ Features**

* **🎨 Live Skin Engine**: Cycle through custom themes (Gemini Dark, Winamp Tribute, The Matrix, Cyberpunk) instantly.  
* **📌 Always on Top**: Keep the tracker floating over your browser so you never lose count while chatting.  
* **🔄 Individual Resets**: Every tracker has a ↺ button to restart the count for the day.  
* **📜 Smart Scrolling**: The scrollbar stays hidden until you have more subjects than can fit on the screen.  
* **💾 Persistent Memory**: Automatically saves your counts and your chosen skin.  
* **Windows 11 Aesthetic**: Designed to look like a native system widget with dark mode support.

## **🚀 How to Run**

### **Path 1: The "Developer" Method (.py)**

If you have Python installed, simply run:

python windows\_counter.py

### **Path 2: The "Native Widget" Method (.pyw)**

Rename the file to windows\_counter.pyw and double-click it. This will launch the app without the black command window.

## **🛠️ Built With**

* **Python 3.14**  
* **Tkinter** (Standard GUI Library)  
* **JSON** (Local Data Persistence)  
* **Collaborative AI Development**

*Created out of necessity, built through collaboration.*