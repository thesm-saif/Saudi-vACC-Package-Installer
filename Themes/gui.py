import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os
import sys

def _get_app_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

APP_FOLDER    = _get_app_folder()
SETTINGS_FILE = os.path.join(APP_FOLDER, "Settings.txt")
LOGO_PATH     = os.path.join(APP_FOLDER, "logo.png")
THEMES_FOLDER = os.path.join(APP_FOLDER, "assets")

GREEN_PRIMARY   = "#3E8F26"
GREEN_HOVER     = "#2d6b1c"
GREEN_SECONDARY = "#7EBF4A"
GOLD            = "#F4B223"
WHITE           = "#FFFFFF"
BG_DARK         = "#1A1A1A"
BG_CARD         = "#232323"
BG_CARD_ACTIVE  = "#1c2b1c"
BG_HEADER       = "#0f0f0f"
GREY_TEXT       = "#666666"
GREY_DIM        = "#2a2a2a"
BORDER_DEFAULT  = "#2a2a2a"
BORDER_ACTIVE   = "#3E8F26"

THEME_DESCRIPTIONS = {
    "DEFAULT": "Real-world Indra ManagAir Theme",
    "DARK":    "Dark Edition of Indra ManagAir Theme",
}

CARD_W      = 360
CARD_IMG_H  = 220
CARD_FOOT_H = 76
CARD_GAP    = 16
SIDE_PAD    = 28
HEADER_H    = 96
FOLDER_H    = 64
LABEL_GAP_TOP = 26
LABEL_H     = 22
LABEL_GAP_BOTTOM = 12
CARDS_GAP_BOTTOM = 16
BOTTOM_H    = 66

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class ThemeSwitcherApp:
    def __init__(self, root, themes, apply_fn):
        self.root = root
        self.themes = themes
        self.apply_fn = apply_fn
        self.theme_names = list(themes.keys())
        self.selected = ctk.StringVar(value=self.theme_names[0])
        self.cards = {}
        self.root_folder = None
        self._refs = []

        num = len(self.theme_names)
        win_w = SIDE_PAD * 2 + CARD_W * num + CARD_GAP * (num - 1)
        win_h = (
            HEADER_H
            + FOLDER_H
            + LABEL_GAP_TOP + LABEL_H + LABEL_GAP_BOTTOM
            + (CARD_IMG_H + CARD_FOOT_H)
            + CARDS_GAP_BOTTOM
            + BOTTOM_H
        )

        root.title("Saudi Arabian vACC - Theme Switcher")
        root.geometry(f"{win_w}x{win_h}")
        root.resizable(False, False)
        root.configure(fg_color=BG_DARK)

        ico_path = os.path.join(APP_FOLDER, "app.ico")
        try:
            root.iconbitmap(ico_path)
        except Exception:
            pass

        try:
            from PIL import ImageTk
            app_png_path = os.path.join(APP_FOLDER, "app.png")
            ico_img = ImageTk.PhotoImage(Image.open(app_png_path).resize((32, 32)))
            root.iconphoto(True, ico_img)
            self._refs.append(ico_img)
        except Exception:
            pass

        self._build_header()
        self._build_folder_bar()
        self._build_theme_section()
        self._build_bottom_bar()

        self._highlight_card(self.theme_names[0])

    def _build_header(self):
        ctk.CTkFrame(self.root, height=3, fg_color=GOLD, corner_radius=0).pack(fill="x")

        header = ctk.CTkFrame(self.root, fg_color=BG_HEADER, height=HEADER_H - 3, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.place(relx=0.0, rely=0.5, anchor="w", x=SIDE_PAD)

        try:
            img = Image.open(LOGO_PATH)
            logo_img = ctk.CTkImage(img, size=(70, 70))
            ctk.CTkLabel(left, image=logo_img, text="").pack(side="left")
            self._refs.append(logo_img)
        except Exception:
            pass

        ctk.CTkLabel(
            header, text="Themes",
            font=ctk.CTkFont("Segoe UI", 24, weight="bold"), text_color=WHITE
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            header, text="© 2026 VATSIM Saudi Arabia",
            font=ctk.CTkFont("Segoe UI", 9), text_color=GREY_TEXT
        ).place(relx=1.0, rely=0.5, anchor="e", x=-SIDE_PAD)

        ctk.CTkFrame(self.root, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")

    def _build_folder_bar(self):
        bar = ctk.CTkFrame(self.root, fg_color="#141414", height=FOLDER_H, corner_radius=0)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        inner = ctk.CTkFrame(bar, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=SIDE_PAD, pady=12)

        ctk.CTkLabel(
            inner, text="INSTALLATION\nPACKAGE",
            font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, width=110,
            anchor="w", justify="left"
        ).pack(side="left")

        self.folder_label = ctk.CTkLabel(
            inner, text="No installation package selected",
            font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT,
            fg_color=BG_CARD, corner_radius=5, anchor="w", padx=12
        )
        self.folder_label.pack(side="left", fill="both", expand=True)

        ctk.CTkButton(
            inner, text="Browse",
            font=ctk.CTkFont("Segoe UI", 10, weight="bold"),
            fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, text_color=WHITE,
            corner_radius=5, width=88, command=self._browse_folder
        ).pack(side="left", padx=(10, 0), fill="y")

        ctk.CTkFrame(self.root, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")

    def _build_theme_section(self):
        label_wrap = ctk.CTkFrame(self.root, fg_color="transparent", height=LABEL_H)
        label_wrap.pack(fill="x", padx=SIDE_PAD, pady=(LABEL_GAP_TOP, LABEL_GAP_BOTTOM))
        label_wrap.pack_propagate(False)

        ctk.CTkLabel(
            label_wrap, text="SELECT A COLOUR THEME",
            font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, anchor="w"
        ).pack(fill="both", expand=True)

        cards_row = ctk.CTkFrame(self.root, fg_color="transparent",
                                  height=CARD_IMG_H + CARD_FOOT_H)
        cards_row.pack(fill="x", padx=SIDE_PAD, pady=(0, CARDS_GAP_BOTTOM))
        cards_row.pack_propagate(False)

        for i, name in enumerate(self.theme_names):
            self._build_card(cards_row, name, is_last=(i == len(self.theme_names) - 1))

        ctk.CTkFrame(self.root, height=1, fg_color=GREY_DIM, corner_radius=0).pack(fill="x")

    def _build_card(self, parent, name, is_last):
        card = ctk.CTkFrame(
            parent, fg_color=BG_CARD, corner_radius=10,
            border_width=1, border_color=BORDER_DEFAULT,
            width=CARD_W, height=CARD_IMG_H + CARD_FOOT_H
        )
        card.pack(side="left", padx=(0, 0 if is_last else CARD_GAP))
        card.pack_propagate(False)
        self.cards[name] = card

        img_box = ctk.CTkFrame(card, fg_color="transparent",
                                width=CARD_W - 24, height=CARD_IMG_H - 12)
        img_box.pack(padx=12, pady=(12, 0))
        img_box.pack_propagate(False)

        preview_path = os.path.join(THEMES_FOLDER, f"{name}.png")
        if os.path.exists(preview_path):
            try:
                raw = Image.open(preview_path)
                target_w = CARD_W - 24
                target_h = CARD_IMG_H - 12
                src_ratio = raw.width / raw.height
                box_ratio = target_w / target_h
                if src_ratio > box_ratio:
                    new_h = target_h
                    new_w = int(new_h * src_ratio)
                else:
                    new_w = target_w
                    new_h = int(new_w / src_ratio)
                resized = raw.resize((new_w, new_h))
                left = (new_w - target_w) // 2
                top = (new_h - target_h) // 2
                cropped = resized.crop((left, top, left + target_w, top + target_h))

                prev_img = ctk.CTkImage(cropped, size=(target_w, target_h))
                lbl = ctk.CTkLabel(img_box, image=prev_img, text="")
                lbl.place(x=0, y=0)
                self._refs.append(prev_img)
                lbl.bind("<Button-1>", lambda e, n=name: self._on_select(n))
            except Exception:
                self._placeholder(img_box, name)
        else:
            self._placeholder(img_box, name)

        ctk.CTkFrame(card, height=1, fg_color=GREY_DIM, corner_radius=0).pack(
            fill="x", padx=12, pady=(10, 0)
        )

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 12))

        rb = ctk.CTkRadioButton(
            row, text="", variable=self.selected, value=name,
            fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, border_color="#555555",
            width=20, command=lambda n=name: self._on_select(n)
        )
        rb.pack(side="left")

        txt = ctk.CTkFrame(row, fg_color="transparent")
        txt.pack(side="left", padx=(10, 0))

        ctk.CTkLabel(
            txt, text=name.title() + " Theme",
            font=ctk.CTkFont("Segoe UI", 13, weight="bold"), text_color=WHITE, anchor="w"
        ).pack(anchor="w")

        desc = THEME_DESCRIPTIONS.get(name.upper(), "")
        if desc:
            ctk.CTkLabel(
                txt, text=desc,
                font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, anchor="w"
            ).pack(anchor="w", pady=(0, 0))

        for w in (card, row, txt):
            w.bind("<Button-1>", lambda e, n=name: self._on_select(n))

    def _placeholder(self, parent, name):
        colors = {"DEFAULT": "#3a3a3a", "DARK": "#0d1117"}
        parent.configure(fg_color=colors.get(name.upper(), "#2a2a2a"))
        ctk.CTkLabel(
            parent, text="Preview coming soon",
            font=ctk.CTkFont("Segoe UI", 10), text_color="#555555"
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _build_bottom_bar(self):
        bottom = ctk.CTkFrame(self.root, fg_color=BG_HEADER, height=BOTTOM_H, corner_radius=0)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)

        inner = ctk.CTkFrame(bottom, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=SIDE_PAD, pady=14)

        self.status_var = ctk.StringVar(
            value="Browse to your sector file installation package, then select a theme."
        )
        ctk.CTkLabel(
            inner, textvariable=self.status_var,
            font=ctk.CTkFont("Segoe UI", 10), text_color=GREY_TEXT, anchor="w"
        ).pack(side="left", fill="both", expand=True)

        ctk.CTkButton(
            inner, text="Cancel",
            font=ctk.CTkFont("Segoe UI", 11),
            fg_color=GREY_DIM, hover_color="#3a3a3a", text_color=WHITE,
            corner_radius=6, width=88, command=self.root.destroy
        ).pack(side="right", padx=(10, 0), fill="y")

        self.apply_btn = ctk.CTkButton(
            inner, text="Apply Theme",
            font=ctk.CTkFont("Segoe UI", 11, weight="bold"),
            fg_color=GREEN_PRIMARY, hover_color=GREEN_HOVER, text_color=WHITE,
            corner_radius=6, width=130, command=self._on_apply
        )
        self.apply_btn.pack(side="right", fill="y")

    def _highlight_card(self, name):
        for n, card in self.cards.items():
            if n == name:
                card.configure(border_color=BORDER_ACTIVE, fg_color=BG_CARD_ACTIVE)
            else:
                card.configure(border_color=BORDER_DEFAULT, fg_color=BG_CARD)

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Select your Sector File installation package")
        if folder:
            self.root_folder = folder
            display = folder if len(folder) < 55 else "..." + folder[-52:]
            self.folder_label.configure(text=display, text_color=WHITE)
            self.status_var.set("Installation package set — select a theme and click Apply Theme.")

    def _on_select(self, name):
        self.selected.set(name)
        self._highlight_card(name)
        self.status_var.set(f"{name.title()} Theme selected.")

    def _on_apply(self):
        if not self.root_folder:
            messagebox.showwarning(
                "No Installation Package Selected",
                "Please browse to your sector file installation package first."
            )
            return

        theme = self.selected.get()
        self.status_var.set(f"Applying {theme.title()} Theme...")
        self.apply_btn.configure(state="disabled", text="Applying...")
        self.root.update()

        try:
            self.apply_fn(theme, self.themes, self.root_folder)
            self.status_var.set(
                f"{theme.title()} Theme applied. Reload EuroScope to see changes."
            )
            self.apply_btn.configure(state="normal", text="Apply Theme")
            messagebox.showinfo(
                "Theme Applied",
                f'"{theme.title()} Theme" applied successfully.\n\nReload EuroScope to see the changes.'
            )
        except Exception as e:
            self.status_var.set("Error — see popup for details.")
            self.apply_btn.configure(state="normal", text="Apply Theme")
            messagebox.showerror("Error", str(e))