# **📊 Pixel Tracker for Google Gemini**

A sleek, standalone Windows 11 utility designed to solve a specific problem: **tracking the "invisible" daily image generation limits in Google Gemini.**

## **💡 The Story**

As a frequent user of Google Gemini, I found it frustrating that there was no "fuel gauge" for my daily image generations. After hitting the 100-image limit one too many times without warning, I decided I needed a dedicated counter that could stay pinned on my screen while I worked.

Since I am new to coding, I collaborated with **Gemini (Google's AI)** to build this from scratch. I provided the vision and specific feature requests—like the "fraction display" and the "highlighted countdown mode"—while Gemini helped me write the Python logic to make it a reality.

## **✨ Features**

* **Always on Top (Pin)**: Keep the tracker floating over your browser so you never lose count while chatting.  
* **Dual Tracking Modes (Smart Highlighting)**:  
  * **Count Up**: The \+ button is highlighted in blue. Best for tracking images against a limit (e.g., 42 / 100).  
  * **Countdown**: The \- button is highlighted in blue. Perfect for tracking remaining credits or a limited session.  
* **Remixable Themes**: Easy-to-edit color codes at the top of the file for custom styles.  
* **Persistent Memory**: Automatically saves your counts to a local json file so you never lose progress.  
* **Windows 11 Aesthetic**: Designed to look like a native system widget with dark mode support.

## **🚀 How to Run (Two Paths)**

I have provided the app in two formats to make it as accessible as possible:

### **Path 1: The "Developer" Method (.py)**

If you want to see the code or run it from your terminal:

1. Install [Python](https://www.python.org/).  
2. Open your terminal and run:  
   python windows\_counter.py

### **Path 2: The "Native Widget" Method (.pyw)**

If you want to use it like a regular Windows app without the black command window:

1. Rename the file from windows\_counter.py to **windows\_counter.pyw**.  
2. Double-click it to launch.  
3. *Tip: You can right-click this file and "Send to Desktop (create shortcut)" to launch it instantly.*

## **🤝 Why Open Source?**

I decided to share the raw Python files (.py and .pyw) rather than a locked .exe for three reasons:

1. **Trust**: You can read every line of code yourself to see exactly how it works. No hidden "black boxes."  
2. **Customization**: I’ve added a "Themes" section at the top. You can change the colors to match your own setup.  
3. **Collaboration**: If you're a "nerd" like me and want to improve the logic or add features, you are free to remix it\!

## **🛠️ Built With**

* **Python 3.14**  
* **Tkinter** (Standard GUI Library)  
* **JSON** (Local Data Persistence)  
* **Collaborative AI Development**

*Created out of necessity, built through collaboration.*