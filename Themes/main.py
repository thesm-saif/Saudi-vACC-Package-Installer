import customtkinter as ctk
from patcher import read_themes, apply_theme
from gui import ThemeSwitcherApp
import os
import sys

def get_app_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

APP_FOLDER = get_app_folder()
SETTINGS_FILE = os.path.join(APP_FOLDER, "Settings.txt")

if __name__ == "__main__":
    try:
        themes = read_themes(SETTINGS_FILE)
    except FileNotFoundError:
        import tkinter as tk
        import tkinter.messagebox as mb
        r = tk.Tk(); r.withdraw()
        mb.showerror("Error", f"Settings.txt not found at:\n{SETTINGS_FILE}")
        raise SystemExit

    if not themes:
        import tkinter as tk
        import tkinter.messagebox as mb
        r = tk.Tk(); r.withdraw()
        mb.showerror("Error", "No themes found in Settings.txt")
        raise SystemExit

    root = ctk.CTk()
    app = ThemeSwitcherApp(root, themes, apply_theme)
    root.mainloop()