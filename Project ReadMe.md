# **📊 Pixel Tracker for Google Gemini**

A sleek, standalone Windows 11 utility designed to solve a specific problem: **tracking the "invisible" daily image generation limits in Google Gemini.**

*(Note: To show your app image, rename your screenshot to "https://www.google.com/search?q=screenshot.png" and upload it to your GitHub folder\!)*

## **💡 The Story**

As a frequent user of Google Gemini, I found it frustrating that there was no "fuel gauge" for my daily image generations. After hitting the 100-image limit one too many times without warning, I decided I needed a dedicated counter that could stay pinned on my screen while I worked.

Since I am new to coding, I collaborated with **Gemini (Google's AI)** to build this from scratch. I provided the vision, the drive for specific features like the "fraction display" and "countdown mode," and Gemini helped me write the Python logic to make it a reality.

## **✨ Features**

* **Always on Top (Pin)**: Keep the tracker floating over your browser so you never lose count while chatting.  
* **Dual Tracking Modes**:  
  * **Count Up**: Great for tracking images against a daily limit (e.g., 42 / 100).  
  * **Countdown**: Perfect for tracking remaining credits or a limited session.  
* **Remixable Themes**: Easy-to-edit color codes at the top of the file for custom styles.  
* **Persistent Memory**: Automatically saves your counts to a local json file so you never lose progress.  
* **Windows 11 Aesthetic**: Designed to look like a native system widget with dark mode support.

## **🚀 How to Run**

### **Option 1: The "Developer" Way (.py)**

If you have Python installed, simply run:

python windows\_counter.py

### **Option 2: The "Widget" Way (.pyw)**

Rename the file to windows\_counter.pyw and double-click it. This will launch the app without the black command window, making it feel like a native Windows application.

## **🛠️ Built With**

* **Python 3.14**  
* **Tkinter** (Standard GUI Library)  
* **JSON** (Local Data Persistence)  
* **Collaborative AI Development**

*Created out of necessity, built through collaboration.*