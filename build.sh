#!/usr/bin/env bash
# set -e
killall sublime_text
PKG="ColorSwitch"
DIR="/home/ninj0x/.config/sublime-text-3/Packages"
# zip -r $PKG *
rm -fr "$DIR"/"$PKG"
cp -r ../"$PKG" "$DIR"
subl
