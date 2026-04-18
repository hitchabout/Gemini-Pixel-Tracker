import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import ctypes

# Windows sound library for retro blips
try:
    import winsound
except ImportError:
    winsound = None

# ==========================================================
# 🎨 THE COLOR VAULT
# ==========================================================

COLOR_MAP = {
    "Deep Blue": "#050a15",
    "Pitch Black": "#000000",
    "Dark Grey": "#121212",
    "Soft Navy": "#1a1b26",
    "Slate": "#1e293b",
    "Steel": "#2d3748",
    "Charcoal": "#111827",
    "Midnight": "#0f172a",
    "Cyber Purple": "#2d002d",
    "Electric Purple": "#6b21a8",
    "Terminal Green": "#051505",
    "Bright Blue": "#3b82f6",
    "Nirvana Blue": "#0ea5e9",
    "Emerald": "#22c55e",
    "Amethyst": "#a855f7",
    "Hot Pink": "#ec4899",
    "Lava Orange": "#ea580c",
    "Vibrant Orange": "#f97316",
    "Cyan": "#06b6d4",
    "Ghost White": "#f8fafc",
    "Silver": "#64748b",
    "Solid White": "#ffffff"
}

HEX_TO_NAME = {v: k for k, v in COLOR_MAP.items()}

# Individual tracker accent colors (buttons/bars)
ACCENT_COLORS = [
    {"name": "Blue", "hex": "#3b82f6"},
    {"name": "Green", "hex": "#22c55e"},
    {"name": "Purple", "hex": "#a855f7"},
    {"name": "Pink", "hex": "#ec4899"},
    {"name": "Orange", "hex": "#f97316"},
    {"name": "Cyan", "hex": "#06b6d4"},
    {"name": "White", "hex": "#ffffff"}
]

# Preset Hub Skins
GLOBAL_THEMES = {
    "Gemini": {"bg": "#050a15", "card": "#0f172a", "border": "#1e293b", "font": "#f8fafc"},
    "Terminal": {"bg": "#000000", "card": "#050505", "border": "#00ff41", "font": "#00ff41"},
    "Classic": {"bg": "#121212", "card": "#1e1e1e", "border": "#333333", "font": "#ffffff"}
}

# ==========================================================
# 🧩 COUNTER WIDGET
# ==========================================================

class CounterWidget:
    def __init__(self, parent, data, app_instance):
        self.parent = parent
        self.app = app_instance
        self.id = data.get('id', str(os.urandom(4).hex()))
        self.after_id = None 
        
        self.frame = tk.Frame(parent, bd=0, highlightthickness=1)
        self.frame.pack(fill="x", padx=15, pady=8)

        self.header = tk.Frame(self.frame)
        self.header.pack(fill="x", padx=12, pady=(12, 0))
        
        self.title_label = tk.Label(self.header, font=("Segoe UI", 8, "bold"), cursor="hand2")
        self.title_label.pack(side="left")
        self.title_label.bind("<Button-1>", lambda e: self.app.open_drawer(self))

        self.del_btn = tk.Button(self.header, text="✕", fg="#ef4444", bd=0, cursor="hand2", command=self.destroy)
        self.del_btn.pack(side="right")
        
        self.reset_btn = tk.Button(self.header, text="↺", bd=0, cursor="hand2", command=self.reset_count, font=("Segoe UI", 10))
        self.reset_btn.pack(side="right", padx=8)

        self.body = tk.Frame(self.frame)
        self.body.pack(fill="x", padx=12, pady=(5, 12))

        self.count_label = tk.Label(self.body, font=("Segoe UI Variable Display", 32, "bold"))
        self.count_label.pack(side="left")

        self.btn_group = tk.Frame(self.body)
        self.btn_group.pack(side="right")

        self.plus_btn = tk.Button(self.btn_group, text="+", font=("Segoe UI", 18, "bold"), bd=0, width=3, cursor="hand2")
        self.plus_btn.pack(pady=2)
        self.plus_btn.bind("<ButtonPress-1>", lambda e: self.start_turbo(1))
        self.plus_btn.bind("<ButtonRelease-1>", lambda e: self.stop_turbo())

        self.minus_btn = tk.Button(self.btn_group, text="-", font=("Segoe UI", 16, "bold"), bd=0, width=3, cursor="hand2")
        self.minus_btn.pack(pady=2)
        self.minus_btn.bind("<ButtonPress-1>", lambda e: self.start_turbo(-1))
        self.minus_btn.bind("<ButtonRelease-1>", lambda e: self.stop_turbo())

        self.progress_bg = tk.Frame(self.frame, bg="#000", height=3)
        self.progress_bg.pack(fill="x", side="bottom")
        self.progress_bar = tk.Frame(self.progress_bg, height=3)
        
        self.apply_data(data)

    def start_turbo(self, delta):
        self.change_count(delta)
        self.after_id = self.app.root.after(400, lambda: self.turbo_loop(delta))

    def turbo_loop(self, delta):
        self.change_count(delta)
        self.after_id = self.app.root.after(80, lambda: self.turbo_loop(delta))

    def stop_turbo(self):
        if self.after_id:
            self.app.root.after_cancel(self.after_id)
            self.after_id = None

    def change_count(self, delta):
        if delta > 0:
            self.count += 1
            self.app.play_sound("up")
        else:
            self.count = max(0, self.count - 1)
            self.app.play_sound("down")
        self.update_ui()
        self.app.save_data()

    def apply_data(self, data):
        self.title = data.get('title', 'New Subject')
        self.count = data.get('count', 0)
        self.mode = data.get('mode', 'up')
        self.goal = data.get('goal', 0)
        self.color = data.get('color', ACCENT_COLORS[0]["hex"])
        self.update_appearance()

    def update_appearance(self):
        ui = self.app.theme
        self.frame.config(bg=ui["card"], highlightbackground=ui["border"])
        self.header.config(bg=ui["card"])
        self.body.config(bg=ui["card"])
        self.title_label.config(text=self.title.upper(), bg=ui["card"], fg=ui["font"])
        self.del_btn.config(bg=ui["card"], activebackground=ui["card"])
        self.reset_btn.config(bg=ui["card"], fg=ui["font"], activebackground=ui["card"])
        self.count_label.config(bg=ui["card"], fg=ui["font"])
        self.btn_group.config(bg=ui["card"])
        self.update_ui()

    def reset_count(self, silent=False):
        if silent or messagebox.askyesno("Reset", f"Reset '{self.title}'?"):
            self.count = self.goal if self.mode == 'down' else 0
            self.update_ui()
            self.app.save_data()

    def update_ui(self):
        display_goal = self.goal if self.goal > 0 else "∞"
        self.count_label.config(text=f"{self.count} / {display_goal}")
        
        plus_active = self.mode == 'up'
        border = self.app.theme["border"]
        self.plus_btn.config(bg=self.color if plus_active else border, fg="white" if plus_active else "#64748b")
        self.minus_btn.config(bg=self.color if not plus_active else border, fg="white" if not plus_active else "#64748b")

        if self.goal > 0:
            percent = min(1.0, self.count / self.goal) if self.mode == 'up' else max(0.0, self.count / self.goal)
            is_done = (self.mode == 'up' and self.count >= self.goal) or (self.mode == 'down' and self.count == 0)
            self.progress_bar.place(relwidth=percent, relheight=1)
            self.progress_bar.config(bg="#22c55e" if is_done else self.color)
            self.count_label.config(fg="#22c55e" if is_done else self.app.theme["font"])
        else:
            self.progress_bar.place(relwidth=0)
            self.count_label.config(fg=self.app.theme["font"])

    def destroy(self):
        if messagebox.askyesno("Confirm", f"Remove '{self.title}'?"):
            self.frame.destroy()
            self.app.remove_widget(self)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "count": self.count, "mode": self.mode, "goal": self.goal, "color": self.color}

# ==========================================================
# 🚀 MAIN HUB
# ==========================================================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Tracker")
        self.root.geometry("420x820")
        
        # State
        self.sound_enabled = tk.BooleanVar(value=True)
        self.is_pinned = tk.BooleanVar(value=True)
        self.theme = GLOBAL_THEMES["Gemini"]
        self.favorites = [None, None, None]
        self.editing_widget = None
        self.widgets = []

        # UI Layout
        self.root.configure(bg=self.theme["bg"])
        self.root.attributes("-topmost", True)

        # Navigation
        self.nav = tk.Frame(root, bg=self.theme["bg"])
        self.nav.pack(fill="x", padx=20, pady=(25, 10))

        self.hub_label = tk.Label(self.nav, text="WIDGET HUB", bg=self.theme["bg"], fg="white", font=("Segoe UI", 11, "bold"))
        self.hub_label.pack(side="left")
        
        self.opt_btn = tk.Button(self.nav, text="⚙ OPTIONS", bg=self.theme["bg"], fg="#64748b", bd=0, 
                                font=("Segoe UI", 7, "bold"), cursor="hand2", command=lambda: self.open_drawer(mode="options"))
        self.opt_btn.pack(side="left", padx=15)

        self.pin_btn = tk.Checkbutton(self.nav, text="Pin", variable=self.is_pinned, bg=self.theme["bg"], fg="#64748b", 
                                     selectcolor=self.theme["bg"], font=("Segoe UI", 8), command=self.toggle_pin)
        self.pin_btn.pack(side="right")

        # Scrollable Area
        self.container = tk.Frame(root, bg=self.theme["bg"])
        self.container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.container, bg=self.theme["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=self.theme["bg"])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Footer
        self.footer = tk.Frame(root, bg=self.theme["bg"])
        self.footer.pack(fill="x", side="bottom", padx=20, pady=25)
        self.add_btn = tk.Button(self.footer, text="+ ADD NEW SUBJECT", bg=ACCENT_COLORS[0]["hex"], fg="white", 
                                 font=("Segoe UI", 9, "bold"), bd=0, pady=12, cursor="hand2", command=self.open_drawer)
        self.add_btn.pack(fill="x")

        # Drawer
        self.drawer = tk.Frame(root, bg=self.theme["card"], highlightthickness=1, highlightbackground=self.theme["border"])
        self.drawer.place(relx=0, rely=1, relwidth=1, relheight=0.96)
        self.build_drawer_ui()

        self.load_data()
        self.apply_global_theme()

    def play_sound(self, type):
        if not self.sound_enabled.get() or winsound is None: return
        try:
            if type == "up": winsound.Beep(800, 30)
            else: winsound.Beep(500, 30)
        except: pass

    def build_drawer_ui(self):
        lbl_style = {"bg": self.theme["card"], "fg": "#64748b", "font": ("Segoe UI", 8, "bold")}
        ent_style = {"bg": "#000", "fg": "white", "insertbackground": "white", "bd": 0, "font": ("Segoe UI", 10)}

        self.drawer_content = tk.Frame(self.drawer, bg=self.theme["card"])
        self.drawer_content.pack(fill="both", expand=True, padx=25, pady=20)

        # --- Tab 1: Configure Tracker ---
        self.config_tab = tk.Frame(self.drawer_content, bg=self.theme["card"])
        tk.Label(self.config_tab, text="CONFIGURE TRACKER", **lbl_style).pack(pady=(0, 10))
        self.name_entry = tk.Entry(self.config_tab, **ent_style)
        self.name_entry.pack(fill="x", ipady=8)
        tk.Label(self.config_tab, text="GOAL (BLANK FOR ∞)", **lbl_style).pack(pady=(15, 5), anchor="w")
        self.goal_entry = tk.Entry(self.config_tab, **ent_style)
        self.goal_entry.pack(fill="x", ipady=8)
        self.dir_var = tk.StringVar(value="up")
        radio_f = tk.Frame(self.config_tab, bg=self.theme["card"])
        radio_f.pack(fill="x", pady=10)
        tk.Radiobutton(radio_f, text="Count Up (+)", variable=self.dir_var, value="up", bg=self.theme["card"], fg="white", selectcolor="#000").pack(side="left")
        tk.Radiobutton(radio_f, text="Count Down (-)", variable=self.dir_var, value="down", bg=self.theme["card"], fg="white", selectcolor="#000").pack(side="left", padx=20)
        self.color_var = tk.StringVar(value=ACCENT_COLORS[0]["hex"])
        color_f = tk.Frame(self.config_tab, bg=self.theme["card"])
        color_f.pack(fill="x", pady=5)
        for c in ACCENT_COLORS:
            tk.Radiobutton(color_f, bg=c["hex"], indicatoron=0, width=2, height=1, variable=self.color_var, value=c["hex"], selectcolor="white").pack(side="left", padx=2)
        tk.Button(self.config_tab, text="SAVE / CREATE", command=self.drawer_submit, bg=ACCENT_COLORS[0]["hex"], fg="white", bd=0, font=("Segoe UI", 8, "bold")).pack(fill="x", pady=20, ipady=10)

        # --- Tab 2: Options & Designer ---
        self.options_tab = tk.Frame(self.drawer_content, bg=self.theme["card"])
        tk.Checkbutton(self.options_tab, text="Enable Button Click Sounds", variable=self.sound_enabled, 
                       bg=self.theme["card"], fg="white", selectcolor="#000", font=("Segoe UI", 9)).pack(anchor="w")

        tk.Label(self.options_tab, text="HUB SKIN DESIGNER", **lbl_style).pack(pady=(15, 5), anchor="w")
        color_names = sorted(list(COLOR_MAP.keys()))
        
        def build_dropdown(label, key):
            row = tk.Frame(self.options_tab, bg=self.theme["card"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, width=12, anchor="w", **lbl_style).pack(side="left")
            cb = ttk.Combobox(row, values=color_names, state="readonly", width=22)
            cb.pack(side="left", padx=5)
            cb.bind("<<ComboboxSelected>>", lambda e: self.on_dropdown_change(key, cb.get()))
            return cb

        self.cb_bg = build_dropdown("Background", "bg")
        self.cb_card = build_dropdown("Card Color", "card")
        self.cb_border = build_dropdown("Border Color", "border")
        self.cb_font = build_dropdown("Font Color", "font")

        tk.Label(self.options_tab, text="SKIN FAVORITE SLOTS", **lbl_style).pack(pady=(15, 5), anchor="w")
        fav_f = tk.Frame(self.options_tab, bg=self.theme["card"])
        fav_f.pack(fill="x")
        self.fav_btns = []
        for i in range(3):
            btn = tk.Button(fav_f, text=f"LOAD {i+1}", font=("Segoe UI", 7), bg="#334155", fg="white", bd=0, width=10, command=lambda idx=i: self.load_favorite(idx))
            btn.pack(side="left", padx=2)
            self.fav_btns.append(btn)
        
        save_f = tk.Frame(self.options_tab, bg=self.theme["card"])
        save_f.pack(fill="x", pady=2)
        for i in range(3):
            tk.Button(save_f, text=f"SAVE TO {i+1}", font=("Segoe UI", 6, "bold"), bg=self.theme["card"], fg="#64748b", bd=1, width=13, command=lambda idx=i: self.save_favorite(idx)).pack(side="left", padx=2)

        tk.Label(self.options_tab, text="ALWAYS-ON QUICK GUIDE", **lbl_style).pack(pady=(15, 5), anchor="w")
        guide_text = "• HOLD +/- for TURBO counting\n• Click TITLE to edit name/color\n• ↺ Resets one tracker to start\n• RESET ALL (top) clears the board\n• Design favorites save your skins"
        tk.Label(self.options_tab, bg="#000", fg="#22c55e", font=("Consolas", 8), justify="left", padx=10, pady=10, text=guide_text).pack(fill="x")

        tk.Button(self.drawer, text="CLOSE DESIGNER", command=self.close_drawer, bg="#334155", fg="white", bd=0, font=("Segoe UI", 8, "bold")).pack(side="bottom", fill="x", ipady=12)

    def on_dropdown_change(self, key, name):
        self.theme[key] = COLOR_MAP[name]
        self.apply_global_theme()
        self.save_data()

    def save_favorite(self, index):
        self.favorites[index] = self.theme.copy()
        self.fav_btns[index].config(text="SAVED!", bg="#22c55e")
        self.root.after(1000, lambda idx=index: self.fav_btns[idx].config(text=f"LOAD {idx+1}", bg="#334155"))
        self.save_data()

    def load_favorite(self, index):
        if self.favorites[index]:
            self.theme = self.favorites[index].copy()
            self.apply_global_theme()
            # Update the dropdowns to match loaded skin
            self.cb_bg.set(HEX_TO_NAME.get(self.theme["bg"], "Custom"))
            self.cb_card.set(HEX_TO_NAME.get(self.theme["card"], "Custom"))
            self.cb_border.set(HEX_TO_NAME.get(self.theme["border"], "Custom"))
            self.cb_font.set(HEX_TO_NAME.get(self.theme["font"], "Custom"))
            self.save_data()
        else: messagebox.showinfo("Slot Empty", "Nothing saved here yet!")

    def open_drawer(self, widget=None, mode="config"):
        self.editing_widget = widget
        self.config_tab.pack_forget(); self.options_tab.pack_forget()
        if mode == "options":
            self.options_tab.pack(fill="both")
            self.cb_bg.set(HEX_TO_NAME.get(self.theme["bg"], "Custom"))
            self.cb_card.set(HEX_TO_NAME.get(self.theme["card"], "Custom"))
            self.cb_border.set(HEX_TO_NAME.get(self.theme["border"], "Custom"))
            self.cb_font.set(HEX_TO_NAME.get(self.theme["font"], "Custom"))
        else:
            self.config_tab.pack(fill="both")
            if widget:
                d = widget.to_dict()
                self.name_entry.delete(0, tk.END); self.name_entry.insert(0, d['title'])
                self.goal_entry.delete(0, tk.END); self.goal_entry.insert(0, str(d['goal']) if d['goal'] > 0 else "")
                self.dir_var.set(d['mode']); self.color_var.set(d['color'])
            else:
                self.name_entry.delete(0, tk.END); self.name_entry.insert(0, f"Counter {len(self.widgets)+1}")
                self.goal_entry.delete(0, tk.END); self.dir_var.set("up")
        self.drawer.place(rely=0.04) 

    def close_drawer(self): self.drawer.place(rely=1)

    def apply_global_theme(self):
        ui = self.theme
        self.root.config(bg=ui["bg"]); self.nav.config(bg=ui["bg"])
        self.hub_label.config(bg=ui["bg"], fg=ui["font"])
        self.pin_btn.config(bg=ui["bg"], fg="#64748b", selectcolor=ui["bg"])
        self.opt_btn.config(bg=ui["bg"], fg="#64748b")
        self.container.config(bg=ui["bg"]); self.canvas.config(bg=ui["bg"])
        self.scroll_frame.config(bg=ui["bg"]); self.footer.config(bg=ui["bg"])
        self.drawer.config(bg=ui["card"], highlightbackground=ui["border"])
        for w in self.widgets: w.update_appearance()

    def drawer_submit(self):
        try: g = int(self.goal_entry.get().strip() or 0)
        except: return messagebox.showerror("Error", "Goal must be a number.")
        res = {"title": self.name_entry.get() or "Untitled", "goal": g, "mode": self.dir_var.get(), "color": self.color_var.get()}
        if self.editing_widget: self.editing_widget.apply_data(res)
        else:
            res['count'] = g if res['mode'] == 'down' else 0
            self.widgets.append(CounterWidget(self.scroll_frame, res, self))
        self.save_data(); self.close_drawer()

    def on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.scroll_frame.winfo_reqheight() > self.canvas.winfo_height(): self.scrollbar.pack(side="right", fill="y")
        else: self.scrollbar.forget()

    def toggle_pin(self): self.root.attributes("-topmost", self.is_pinned.get())
    def remove_widget(self, w): 
        if w in self.widgets: self.widgets.remove(w); self.save_data()

    def save_data(self):
        data = {"theme": self.theme, "sound": self.sound_enabled.get(), "favorites": self.favorites, "items": [w.to_dict() for w in self.widgets]}
        with open("tracker_save.json", "w") as f: json.dump(data, f)

    def load_data(self):
        if os.path.exists("tracker_save.json"):
            try:
                with open("tracker_save.json", "r") as f:
                    d = json.load(f)
                    self.theme = d.get("theme", GLOBAL_THEMES["Gemini"])
                    if "font" not in self.theme: self.theme["font"] = "#f8fafc"
                    self.sound_enabled.set(d.get("sound", True))
                    self.favorites = d.get("favorites", [None, None, None])
                    for item in (d.get("items", d) if isinstance(d, dict) else d):
                        self.widgets.append(CounterWidget(self.scroll_frame, item, self))
            except: pass

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('vista')
    try:
        hWnd = ctypes.windll.user32.GetParent(root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hWnd, 20, ctypes.byref(ctypes.c_int(1)), 4)
    except: pass
    app = App(root)
    root.mainloop()