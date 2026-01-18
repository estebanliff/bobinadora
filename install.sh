#!/bin/bash

set -e

PROJECT_NAME="bobinadora"
INSTALL_DIR="$HOME/Desktop/$PROJECT_NAME"
START_SCRIPT="$HOME/Desktop/start_bobinadora.sh"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/bobinadora.desktop"

echo "==============================="
echo " Instalando Bobinadora"
echo "==============================="

# --------------------------------------
# 1. Dependencias
# --------------------------------------
echo "[1/4] Instalando dependencias..."

sudo apt update
sudo apt install -y \
    python3-pil \
    python3-pil.imagetk \
    python3-tk \
    libjpeg-dev \
    zlib1g-dev \
    fonts-noto-color-emoji \
    fonts-dseg

echo "Dependencias instaladas ✔"

# --------------------------------------
# 2. Script de arranque
# --------------------------------------
echo "[3/4] Creando script de arranque..."

cat << EOF > "$START_SCRIPT"
#!/bin/bash
cd "$INSTALL_DIR"
python3 app/main.py
EOF

chmod +x "$START_SCRIPT"

echo "Script de arranque creado ✔"

# --------------------------------------
# 4. Autostart
# --------------------------------------
echo "[4/4] Configurando inicio automático..."

mkdir -p "$AUTOSTART_DIR"

cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Type=Application
Name=Bobinadora
Exec=$START_SCRIPT
Terminal=false
X-GNOME-Autostart-enabled=true
EOF

echo "Inicio automático configurado ✔"

echo "==============================="
echo " Instalación finalizada"
echo " Reinicie la Raspberry"
echo "==============================="
