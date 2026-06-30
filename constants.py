import os
import sys

def get_app_folder():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

APP_FOLDER    = get_app_folder()
ASSETS_FOLDER = os.path.join(APP_FOLDER, "assets")
SETTINGS_FILE = os.path.join(APP_FOLDER, "Settings.txt")
CONFIG_PATH   = os.path.join(
    os.environ.get("APPDATA", APP_FOLDER), "SaudiVACC", "config.json"
)

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
RED_WARN        = "#CC3300"
GREEN_SUCCESS   = "#1D9E75"

CARD_W           = 360
CARD_IMG_H       = 220
CARD_FOOT_H      = 76
CARD_GAP         = 16
SIDE_PAD         = 28
HEADER_H         = 96
FOLDER_H         = 64
LABEL_GAP_TOP    = 26
LABEL_H          = 22
LABEL_GAP_BOTTOM = 12
CARDS_GAP_BOTTOM = 16
BOTTOM_H         = 66

THEME_NAMES = ["DEFAULT", "DARK"]
THEME_DESCRIPTIONS = {
    "DEFAULT": "Real-world Indra ManagAir Theme",
    "DARK":    "Dark Edition of Indra ManagAir Theme",
}

RATING_MAP = {
    "Observer":             (0,  "OBS"),
    "Ground/Delivery":      (1,  "S1"),
    "Tower Controller":     (2,  "S2"),
    "TMA Controller":       (3,  "S3"),
    "Enroute Controller":   (4,  "C1"),
    "Senior Controller":    (6,  "C3"),
    "Instructor 1":         (7,  "I1"),
    "Instructor 2":         (8,  "I2"),
    "Instructor 3":         (9,  "I3"),
    "Supervisor":           (10, "SUP"),
    "Administrator":        (11, "ADM"),
}
RATINGS = list(RATING_MAP.keys())
RATING_VALUE_TO_LABEL = {v[0]: k for k, v in RATING_MAP.items()}