import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import ctypes

# ==========================================================
# 🎨 THEME & STYLE SETTINGS (Easy to Remix!)
# ==========================================================
# Feel free to change these hex codes to create your own theme.
# Popular hex codes: Purple (#7c3aed), Emerald (#10b981), Amber (#f59e0b)

THEMES = {
    "Gemini Dark": {
        "bg": "#050a15",          # Main background
        "card": "#0f172a",        # Counter card color
        "accent": "#3b82f6",      # Primary button color (Blue)
        "success": "#22c55e",     # Goal reached color (Green)
        "text_main": "#f8fafc",   # Primary numbers/text
        "text_dim": "#64748b",    # Titles/subtitles
        "border": "#1e293b"       # Card border color
    }
}

# Select active theme
UI = THEMES["Gemini Dark"]

# Fonts
FONT_MAIN = ("Segoe UI Variable Display", 32, "bold")
FONT_TITLE = ("Segoe UI", 8, "bold")
FONT_HUD = ("Segoe UI", 11, "bold")

# ==========================================================
# ⚙️ CORE LOGIC (The "Brain")
# ==========================================================

class CounterWidget:
    """Blueprint for a single counter card."""
    def __init__(self, parent, data, on_delete, on_change):
        self.parent = parent
        self.on_delete = on_delete
        self.on_change = on_change
        
        # Load data from the saved file
        self.id = data.get('id', str(os.urandom(4).hex()))
        self.title = data.get('title', 'New Subject')
        self.count = data.get('count', 0)
        self.mode = data.get('mode', 'up') # 'up' or 'down'
        self.goal = data.get('goal', 100)
        self.start_val = data.get('start_val', 100)

        # Draw the card
        self.frame = tk.Frame(parent, bg=UI["card"], bd=0, highlightthickness=1, highlightbackground=UI["border"])
        self.frame.pack(fill="x", padx=15, pady=8)

        # Card Header (Title & Delete Button)
        self.header = tk.Frame(self.frame, bg=UI["card"])
        self.header.pack(fill="x", padx=12, pady=(12, 0))
        
        self.title_label = tk.Label(self.header, text=self.title.upper(), bg=UI["card"], fg=UI["text_dim"], font=FONT_TITLE)
        self.title_label.pack(side="left")

        self.del_btn = tk.Button(self.header, text="✕", bg=UI["card"], fg="#ef4444", bd=0, 
                                 activebackground=UI["card"], activeforeground="#f87171",
                                 cursor="hand2", command=self.destroy, font=("Arial", 9))
        self.del_btn.pack(side="right")

        # Card Body (Display & Controls)
        self.body = tk.Frame(self.frame, bg=UI["card"])
        self.body.pack(fill="x", padx=12, pady=(5, 12))

        # The Counter Label (e.g. "42 / 100")
        self.count_label = tk.Label(self.body, text="", bg=UI["card"], fg=UI["text_main"], font=FONT_MAIN)
        self.count_label.pack(side="left")

        # Button Group
        self.btn_group = tk.Frame(self.body, bg=UI["card"])
        self.btn_group.pack(side="right")

        btn_opt = {"bd": 0, "activeforeground": "white", "cursor": "hand2", "width": 3}
        
        # Determine which button gets the "High Visibility" color based on mode
        plus_bg = UI["accent"] if self.mode == 'up' else UI["border"]
        plus_fg = "white" if self.mode == 'up' else UI["text_dim"]
        
        minus_bg = UI["accent"] if self.mode == 'down' else UI["border"]
        minus_fg = "white" if self.mode == 'down' else UI["text_dim"]

        self.plus_btn = tk.Button(self.btn_group, text="+", bg=plus_bg, fg=plus_fg, 
                                 command=self.increment, font=("Segoe UI", 18, "bold"), **btn_opt)
        self.plus_btn.pack(pady=2)

        self.minus_btn = tk.Button(self.btn_group, text="-", bg=minus_bg, fg=minus_fg, 
                                  command=self.decrement, font=("Segoe UI", 16, "bold"), **btn_opt)
        self.minus_btn.pack(pady=2)

        # Progress Bar at the bottom of the card
        self.progress_bg = tk.Frame(self.frame, bg="#020617", height=3)
        self.progress_bg.pack(fill="x", side="bottom")
        self.progress_bar = tk.Frame(self.progress_bg, bg=UI["accent"], height=3)
        
        self.update_ui()

    def increment(self):
        self.count += 1
        self.update_ui()
        self.on_change()

    def decrement(self):
        self.count = max(0, self.count - 1)
        self.update_ui()
        self.on_change()

    def update_ui(self):
        """Updates colors and labels based on the current count."""
        total = self.goal if self.mode == 'up' else self.start_val
        self.count_label.config(text=f"{self.count} / {total}")
        
        # Progress math
        if self.mode == 'up':
            percent = min(1.0, self.count / self.goal) if self.goal > 0 else 0
            is_done = self.count >= self.goal
        else:
            percent = max(0.0, self.count / self.start_val) if self.start_val > 0 else 0
            is_done = self.count == 0
            
        self.progress_bar.place(relwidth=percent, relheight=1)
        
        # Color feedback
        if is_done:
            self.progress_bar.config(bg=UI["success"])
            self.count_label.config(fg=UI["success"])
        else:
            self.progress_bar.config(bg=UI["accent"])
            self.count_label.config(fg=UI["text_main"])

    def destroy(self):
        """Removes the card from UI and memory."""
        if messagebox.askyesno("Confirm", f"Remove tracker '{self.title}'?"):
            self.frame.destroy()
            self.on_delete(self)

    def to_dict(self):
        """Convert this widget's data to a format we can save to a file."""
        return {
            "id": self.id, "title": self.title, "count": self.count,
            "mode": self.mode, "goal": self.goal, "start_val": self.start_val
        }

class App:
    """The main window shell."""
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Tracker")
        self.root.geometry("380x650")
        self.root.configure(bg=UI["bg"])
        
        # Default to Always on Top
        self.is_pinned = tk.BooleanVar(value=True)
        self.root.attributes("-topmost", True)

        # Header Navigation
        self.nav = tk.Frame(root, bg=UI["bg"])
        self.nav.pack(fill="x", padx=20, pady=(25, 15))

        tk.Label(self.nav, text="WIDGET HUB", bg=UI["bg"], fg="white", font=FONT_HUD).pack(side="left")
        
        self.pin_btn = tk.Checkbutton(self.nav, text="Pin", variable=self.is_pinned, 
                                     bg=UI["bg"], fg=UI["text_dim"], selectcolor=UI["bg"], 
                                     activebackground=UI["bg"], font=("Segoe UI", 8),
                                     command=self.toggle_pin)
        self.pin_btn.pack(side="right")

        # Scrollable View for many counters
        self.canvas = tk.Canvas(root, bg=UI["bg"], highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg=UI["bg"])
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=380)
        self.canvas.pack(fill="both", expand=True)
        
        # Footer "Add" Button
        self.footer = tk.Frame(root, bg=UI["bg"])
        self.footer.pack(fill="x", side="bottom", padx=20, pady=25)

        self.add_btn = tk.Button(self.footer, text="+ ADD NEW SUBJECT", bg=UI["accent"], fg="white", 
                                 font=("Segoe UI", 9, "bold"), bd=0, pady=12, cursor="hand2", 
                                 command=self.show_add_dialog)
        self.add_btn.pack(fill="x")

        self.widgets = []
        self.load_data()

    def toggle_pin(self):
        self.root.attributes("-topmost", self.is_pinned.get())

    def show_add_dialog(self):
        title = simpledialog.askstring("New Tracker", "Subject Name:")
        if not title: return
        mode_up = messagebox.askyesno("Mode", "Count UP to a limit?")
        
        if mode_up:
            limit = simpledialog.askinteger("Set Limit", "What is the daily limit?", initialvalue=100)
            data = {"title": title, "count": 0, "mode": "up", "goal": limit}
        else:
            start = simpledialog.askinteger("Set Start", "Starting number:", initialvalue=50)
            data = {"title": title, "count": start, "mode": "down", "start_val": start}

        w = CounterWidget(self.scroll_frame, data, self.remove_widget, self.save_data)
        self.widgets.append(w)
        self.save_data()

    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
            self.save_data()

    def save_data(self):
        data = [w.to_dict() for w in self.widgets]
        with open("tracker_save.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists("tracker_save.json"):
            try:
                with open("tracker_save.json", "r") as f:
                    data = json.load(f)
                    for item in data:
                        w = CounterWidget(self.scroll_frame, item, self.remove_widget, self.save_data)
                        self.widgets.append(w)
            except: pass

if __name__ == "__main__":
    root = tk.Tk()
    
    # Apply Windows 11 Dark Mode Title Bar
    try:
        hWnd = ctypes.windll.user32.GetParent(root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hWnd, 20, ctypes.byref(ctypes.c_int(1)), 4)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hWnd, 35, ctypes.byref(ctypes.c_int(0x150a05)), 4)
    except: pass
    
    app = App(root)
    root.mainloop()