# Keys
from libqtile.config import Key 
from libqtile.lazy import lazy

# Mouse
from libqtile.config import Click, Drag

# Groups
from libqtile.config import Group, Match

# Layouts
from libqtile import layout

# Screens
from libqtile.config import Screen
from libqtile import bar, widget

# Screens/Extras
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

# Startup 
import os
import subprocess
from libqtile import hook

# Variables ----------------------------------------------
mod = "mod4"
terminal = "kitty"
explorer = "thunar"
launcher = "rofi -show drun"

theme = {
    "background": "#282738",
    "foreground": "#353446",
}

font_family = "DejaVu Sans Bold"
font_size = 15

images_dir = os.path.expanduser("~/images/")

widget_defaults = dict(
    font = font_family,
    fontsize = font_size,
    padding = 10,
)

extension_defaults = widget_defaults.copy()


# Startup/Scripts -----------------------------------------
# Set the wallpaper using feh
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["feh", "--bg-fill", os.path.join(images_dir, "comfy-1.jpg")])


# Key Bindings ------------------------------------------
keys = [
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
   
    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(launcher), desc="Spawn launcher"),
    
    # Spawn default file explorer
    Key([mod], "e", lazy.spawn(explorer), desc="Spawn file explorer"),
]


# Mouse Bindings ----------------------------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


# Groups -----------------------------------------------
groups = [Group(i) for i in ["\uf111 ", "\uf111", "\uea71 ",]]
group_hotkeys = "12345"

for g, k in zip(groups, group_hotkeys):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                k,
                lazy.group[g.name].toscreen(),
                desc=f"Switch to group {g.name}",
            ),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                k,
                lazy.window.togroup(g.name, switch_group=False),
                desc=f"Switch to & move focused window to group {g.name}"
            )
        ]
    )


# Layouts ---------------------------------------------
layouts = [
    layout.Columns(margin=(0, 5, 5, 5), border_focus='#a1b5ec', border_width=1),
    layout.Max(),
]


# Screens --------------------------------------------
screens = []
num_screens = 2  # Change this value to the number of screens you want

powerline_forward_slash = {
    "decorations": [
        PowerLineDecoration(
            path="forward_slash"
        )
    ]
}


for _ in range(num_screens):
    screen = Screen(
        top=bar.Bar(
            [
                widget.Image(
                    background = theme["background"], 
                    filename = os.path.join(images_dir, "arch-linux-icon.png"),                    
                    scale = True, 
                    margin_y = 5
                ),
                
                widget.GroupBox(
                    background = theme["background"], 
                    highlight_method = 'block', 
                    **powerline_forward_slash
                ),

                widget.Spacer(
                    background = theme["foreground"], 
                    **powerline_forward_slash
                ),
                
                widget.Clock(
                    background = theme["background"], 
                    format="%H:%M", 
                    padding=15
                ),
            ],
            30,
            margin=(5, 5, 5, 5),
        ),
    )
    screens.append(screen)


# General Configuration Variables ---------------------

# A function which generates group binding hotkeys. It takes a single argument, the DGroups object, and can use that to set up dynamic key bindings.
# A sample implementation is available in 'libqtile/dgroups.py' called `simple_key_binder()`, which will bind groups to "mod+shift+0-10" by default.
dgroups_key_binder = None

# A list of Rule objects which can send windows to various groups based on matching criteria.
dgroups_app_rules = []  # type: list

# Controls whether or not focus follows the mouse around as it moves across windows in a layout.
follow_mouse_focus = True

# When clicked, should the window be brought to the front or not. 
# If this is set to "floating_only", only floating windows will get affected (This sets the X Stack Mode to Above.)
bring_front_click = False

# If true, the cursor follows the focus as directed by the keyboard, warping to the center of the focused window. 
# When switching focus between screens, If there are no windows in the screen, the cursor will warp to the center of the screen.
cursor_warp = False

# The default floating layout to use. This allows you to set custom floating rules among other things if you wish.
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

# If a window requests to be fullscreen, it is automatically fullscreened. 
# Set this to false if you only want windows to be fullscreen if you ask them to be.
auto_fullscreen = False

# Behavior of the _NET_ACTIVATE_WINDOW message sent by applications
#
# urgent: urgent flag is set for the window
# focus: automatically focus the window
# smart: automatically focus if the window is in the current group
# never: never automatically focus any window that requests it
focus_on_window_activation = "smart"

# Controls whether or not to automatically reconfigure screens when there are changes in randr output configuration.
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None