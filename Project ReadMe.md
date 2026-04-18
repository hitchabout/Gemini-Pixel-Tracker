# **📊 Pixel Tracker & Universal Hub**

### **A Multi-Purpose Windows 11 Utility for AI, Tracking, and Productivity**

**Pixel Tracker** is a sleek, standalone Windows utility designed to track anything from daily image generation limits in Google Gemini to scores, door counts, or session tallies.

## **💡 The Story**

Frequent AI users often hit "invisible" limits. I built this tool to act as a fuel gauge for my daily image generations in Google Gemini. However, as the project grew, it evolved into a **Universal Counter Hub** where you can manage multiple independent trackers with custom colors, goals, and behaviors.

This project was built through a collaboration between a vision-driven creator and **Gemini (Google's AI)**, proving that great tools can be built starting with zero coding knowledge.

## **✨ Features**

* **🎨 Designer System (DS)**: Complete skinning engine. Use dropdown menus to pick named colors for the Background, Cards, Borders, and Fonts.  
* **💾 Design Favorites**: Save up to 3 custom hub skins and swap between them instantly.  
* **🚀 Turbo Hold**: Click and hold the \+ or \- buttons to zip through large numbers (ideal for high-limit tracking).  
* **🔢 Multi-Subject Hub**: Add as many counters as you need. Perfect for use as a scoreboard, inventory tally, or door-clicker.  
* **📌 Always on Top**: Keep the widget pinned over your browser or work apps so you never lose count.  
* **🔄 Individual Resets**: Use the ↺ button to reset specific counters without affecting the rest of the board.  
* **💾 Persistence**: Your counts, settings, and custom skins are saved automatically to a local json file.  
* **🎵 Haptic Sounds**: Satisfying retro system blips for every click (can be toggled in Options).

## **🚀 How to Run**

### **Option 1: The "Native Widget" (.pyw)**

Rename the script to windows\_counter.pyw and double-click. This launches the app as a smooth background process without a console window.

### **Option 2: The "Developer" Method (.py)**

Run via terminal to see background logs:

python windows\_counter.py

## **🛠️ Built With**

* **Python 3.14**  
* **Tkinter** (Standard GUI Library)  
* **JSON** (Local Data Persistence)  
* **Collaborative AI Development**

*Created out of necessity, built through collaboration.*

python productivity open-source counter widget tkinter scoreboard image-generation multiple-counters windows-11 ai-tools skinnable google-gemini universal-counter door-clicker-counter