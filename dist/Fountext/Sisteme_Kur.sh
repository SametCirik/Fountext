#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Fountext KDE/Wayland için sisteme entegre ediliyor..."

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

# İŞTE BURASI: Klasörün içine de şık logolu taşınabilir bir kısayol bırakalım!
cp ~/.local/share/applications/Fountext-Editor.desktop "$DIR/Fountext-Başlatıcı.desktop"
chmod +x "$DIR/Fountext-Başlatıcı.desktop"

kbuildsycoca5 &> /dev/null || kbuildsycoca6 &> /dev/null || update-desktop-database ~/.local/share/applications/ &> /dev/null || true

echo ""
echo "Kurulum tamamlandı!"
echo "Uygulamanızı başlat menüsünden veya bu klasörde yeni oluşan 'Fountext-Başlatıcı' kısayolundan açabilirsiniz."
echo ""
read -p "Çıkmak için Enter'a basın..."
