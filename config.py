from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile import bar, layout, widget, hook
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
import os
import subprocess


# Definitions
mod = "mod4"
terminal = "kitty"
explorer = "thunar"
launcher = "rofi -show drun"

widget_defaults = dict(
    font="sans",
    fontsize=15,
    padding=10,
    foreground='#a1b5ec'
)
extension_defaults = widget_defaults.copy()


# Default and Custom Keys
keys = [
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
   
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(launcher), desc="Spawn launcher"),
    
    # -- custom --
    # Spawn default file explorer
    Key([mod], "e", lazy.spawn(explorer), desc="Spawn file explorer"),
]

# Groups 
groups = [Group(i) for i in ["a", "b", "c", "d", "e"]]
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


# Layouts
layouts = [
    layout.Columns(margin=(0, 5, 5, 5), border_focus='#a1b5ec', border_width=1),
    layout.Max(),
]


# Topside bar
powerline = {
    "decorations": [
        PowerLineDecoration(
            path="forward_slash"
        )
    ]
}

screens = []
num_screens = 2  # Change this value to the number of screens you want

for _ in range(num_screens):
    screen = Screen(
        top=bar.Bar(
            [
                widget.Image(filename="~/images/arch-linux-icon.jpg", background="282738", scale=True),
                widget.GroupBox(highlight_method='block', background="282738", **powerline),
                widget.Spacer(background="353446", **powerline),
                widget.Clock(format="%H:%M", background="282738", padding=15),
            ],
            24,
            margin=(5, 5, 5, 5),
        ),
    )
    screens.append(screen)


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
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
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


# -- custom --
# Set the wallpaper using feh
wallpaper_path = os.path.expanduser("~/images/comfy-1.jpg")
subprocess.Popen(["feh", "--bg-fill", wallpaper_path])

picom_path = os.path.expanduser("~/.config/picom/picom.conf")
subprocess.Popen(["picom", "--config", picom_path])