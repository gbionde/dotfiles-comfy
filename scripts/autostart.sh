#!/bin/sh
picom -b --config ~/.config/picom/picom.conf &
xrandr --output HDMI-0 --auto --right-of DP-2