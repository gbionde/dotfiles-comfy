# Keys
from libqtile.lazy import lazy
from libqtile.config import Key

# Mouse
from libqtile.config import Click, Drag

# Groups
from libqtile.config import Group, Match

# Layouts
from libqtile import layout

# Screens
from libqtile import bar, widget
from libqtile.config import Screen

# Screens/Extras
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

# Startup
import os
from scripts import *
from themes import current_theme as theme

widget_defaults = dict(
    font = font_family,
    fontsize = 15,
    padding = 10,
)

extension_defaults = widget_defaults.copy()

# Key Bindings ------------------------------------------
keys = [
    # Switch between windows
    Key([modifier], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([modifier], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([modifier], "down", lazy.layout.down(), desc="Move focus down"),
    Key([modifier], "up", lazy.layout.up(), desc="Move focus up"),
    Key(["mod1"], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Key(["mod1"], "Tab", lazy.spawn(os.path.join(home_dir, ".config/rofi/launchers/type-3/launcher.sh")), desc="Spawn launcher"),

    # Move windows between left/right columns or move up/down in current stack.
    Key([modifier, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([modifier, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([modifier, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([modifier, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    Key([modifier, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([modifier, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([modifier, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([modifier, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([modifier], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key([modifier], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([modifier, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts
    Key([modifier], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([modifier], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([modifier, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([modifier], "r", lazy.spawn(os.path.join(home_dir, ".config/rofi/launchers/type-7/launcher.sh")), desc="Spawn launcher"),
    Key([modifier, "shift"], "q", lazy.spawn(os.path.join(home_dir, ".config/rofi/powermenu/type-5/powermenu.sh")), desc="Shutdown Qtile"),

    # Spawn default file explorer
    Key([modifier], "e", lazy.spawn(explorer), desc="Spawn file explorer"),

    # Raise, lower and mute volume
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+"), desc="Increase volume using amixer"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%-"), desc="Decrease volume using amixer"),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle"), desc="Mute volume using amixer"),

    # Key to increase and decrease screen brightness using brightnessctl
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%"), desc="Increase brightness using brightnessctl"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-"), desc="Decrease brightness using brightnessctl"),

    # Key to toggle between Brazilian Portuguese ABNT2 and US English
    Key(["mod1"], "Shift_L", lazy.function(toggle_keyboard_layout), desc="Toggle keyboard layout between BR ABNT2 and US"),

    # Printscreen
    Key([], "Print", lazy.spawn("scrot")),
    Key([modifier, "shift"], "s", lazy.spawn("scrot -s")),

    Key([modifier], "f", lazy.window.toggle_floating()),
]

# Mouse Bindings --------------------------------------
mouse = [
    Drag([modifier], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([modifier], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([modifier], "Button2", lazy.window.bring_to_front()),
]

# Layouts ---------------------------------------------
layouts = [
    layout.Columns(margin=(0, 3, 3, 3), border_focus='#a1b5ec', border_width=2),
    layout.Max(),
]

# Groups -----------------------------------------------
group_icon = "\uf111 "
group_icon_selected = "\uebb4 "
group_hotkeys = "123"

for hotkey in group_hotkeys:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key(
            [modifier],
            hotkey,
            lazy.group[hotkey].toscreen(),
            desc=f"Switch to group {hotkey}",
        ),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key(
            [modifier, "shift"],
            hotkey,
            lazy.window.togroup(hotkey, switch_group=False),
            desc=f"Switch to & move focused window to group {hotkey}",
        )    
    ])

groups = [Group(hotkey, label=group_icon) for hotkey in group_hotkeys]


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

powerline_rounded_left = {
    "decorations": [
        PowerLineDecoration(
            path="rounded_left"
        )
    ]
}

powerline_rounded_right = {
    "decorations": [
        PowerLineDecoration(
            path="rounded_right"
        )
    ]
}

for _ in range(num_screens):
    screen = Screen(
        top=bar.Bar(
            [
                widget.Image(
                    background = theme["base"],
                    filename = os.path.join(images_dir, "icons/arch-linux-icon.png"),
                    scale = True,
                    margin_y = 9,
                ),

                widget.GroupBox(
                    background = theme["base"],
                    highlight_method = 'block',
                    inactive="#FFFFFF",
                    foreground="#FFFFFF",
                    **powerline_rounded_left,
                ),

                widget.Spacer(
                    background = "#00000000",
                    **powerline_rounded_right,
                ),

                # Current volume, uses amixer
                widget.Volume(
                    fmt = '\uf028   {}',
                    background = theme["base"],
                    font = font_family_bold,
                    **powerline_rounded_right,
                ),

                # Current battery
                widget.Battery(
                    format = '{char}   {percent:2.0%}',
                    background = theme["base"],
                    font = font_family_bold,

                    unknown_char = "\U000f0091",    # Material Design icon for unknown battery state
                    discharge_char = "\U000f0083",  # Material Design icon for discharging battery
                    charge_char = "\U000f0084",     # Material Design icon for charging battery
                    full_char = "\U000f0079",       # Material Design icon for full battery (same as charging)

                    low_percentage = 0.15,
                    low_foreground = "FF0000",
                    **powerline_rounded_right,
                ),

                # Current time
                widget.Clock(
                    background = theme["base"],
                    format="\uf43a   %H:%M  ",
                    font=font_family_bold,
                ),
            ],
            40,
            background = "#00000000",
            margin=(5, 10, 15, 10),
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