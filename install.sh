#!/bin/bash

set -e

PROJECT_NAME="bobinadora"
INSTALL_DIR="$HOME/Desktop/$PROJECT_NAME"
START_SCRIPT="$HOME/Desktop/start_bobinadora.sh"
UPDATE_SCRIPT="$HOME/Desktop/update_bobinadora.sh"
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

cat << EOF > "$UPDATE_SCRIPT"
#!/bin/bash
cd "$INSTALL_DIR"
echo "Actualizando el codigo..."
git pull
sleep 5
EOF

chmod +x "$UPDATE_SCRIPT"

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

# --------------------------------------
# 5. Configuración GPIO estado seguro
# --------------------------------------
echo "[5/5] Configurando GPIO en estado seguro (LOW al boot)..."

if [ -f /boot/firmware/config.txt ]; then
    BOOT_CONFIG="/boot/firmware/config.txt"
elif [ -f /boot/config.txt ]; then
    BOOT_CONFIG="/boot/config.txt"
else
    echo "No se encontró config.txt"
    exit 1
fi

add_gpio_line () {
    LINE="$1"
    if ! grep -q "^$LINE$" "$BOOT_CONFIG"; then
        echo "$LINE" | sudo tee -a "$BOOT_CONFIG" > /dev/null
        echo "  Agregado: $LINE"
    else
        echo "  Ya existe: $LINE"
    fi
}

add_gpio_line "gpio=17=op,dh"
add_gpio_line "gpio=22=op,dh"
add_gpio_line "gpio=27=op,dh"

echo "GPIO configurados ✔ (requiere reinicio)"

# --------------------------------------
# Ocultar advertencias de bajo voltaje
# --------------------------------------
echo "[POWER] Configurando ocultar advertencias de bajo voltaje..."

if ! grep -q "^avoid_warnings=1$" "$BOOT_CONFIG"; then
    echo "avoid_warnings=1" | sudo tee -a "$BOOT_CONFIG" > /dev/null
    echo "  avoid_warnings=1 agregado"
else
    echo "  avoid_warnings=1 ya existe"
fi

echo "Advertencias de bajo voltaje deshabilitadas ✔ (requiere reinicio)"