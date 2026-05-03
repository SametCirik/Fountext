#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Integrating Fountext into the system (KDE/Wayland/App Menu)..."

mkdir -p ~/.local/share/applications/
cat << INI > ~/.local/share/applications/Fountext-Editor.desktop
[Desktop Entry]
Name=Fountext
Comment=Screenwriting Editor
Exec="$DIR/Fountext"
Path=$DIR
Icon=$DIR/Fountext_Logo.png
Terminal=false
Type=Application
Categories=Office;TextEditor;
StartupWMClass=Fountext-Editor
INI

# Klasör içi Fountext-Launcher kısayolunu oluşturalım
cp ~/.local/share/applications/Fountext-Editor.desktop "$DIR/Fountext-Launcher.desktop"
chmod +x "$DIR/Fountext-Launcher.desktop"

kbuildsycoca5 &> /dev/null || kbuildsycoca6 &> /dev/null || update-desktop-database ~/.local/share/applications/ &> /dev/null || true

echo ""
echo "Installation complete!"
echo "You can now launch Fountext from your App Menu, or use the new 'Fountext-Launcher' shortcut in this folder."
echo ""
read -p "Press Enter to exit..."
