import os
import subprocess
from libqtile import hook

# Variables ----------------------------------------------
modifier = "mod4"
terminal = "kitty"
explorer = "thunar"
launcher = "rofi -show drun"

# Directories
home_dir = os.path.expanduser("~/")
images_dir = os.path.expanduser("~/images/")

# Font Style
font_size = 15,
font_family = "Ubuntu Regular"
font_family_bold = "Ubuntu Mono Regular"

# Startup/Scripts -----------------------------------------
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["picom", "--config", os.path.join(home_dir, ".config/picom/picom.conf")])
    subprocess.Popen(["feh", "--bg-fill", os.path.join(images_dir, "anime-girl.jpg")])

def toggle_keyboard_layout(qtile):
    current_layout = subprocess.run(['setxkbmap', '-query'], capture_output=True, text=True).stdout
    if 'br' in current_layout:
        # Switch to US English layout
        subprocess.run(['setxkbmap', 'us'])
    else:
        # Switch to Brazilian Portuguese ABNT2 layout
        subprocess.run(['setxkbmap', 'br', 'abnt2'])
        

