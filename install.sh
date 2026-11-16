#!/usr/bin/env bash
set -e

INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="mcu"  # final command name
SOURCE_FILE="mcu_project.py"
DATA_DIR="$HOME/.local/share/mcu/data"

# Create the directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Remove the old install, the command used to be called mcuProjectInit
find "$INSTALL_DIR" -maxdepth 1 \( -iname "mcuprojectinit" -o -iname "mcuprojectinit.py" \) -print -delete

# Copy the script to its destination, with the right name
cp "$SOURCE_FILE" "$INSTALL_DIR/$SCRIPT_NAME"

# Install the templates and point the installed script to them
mkdir -p "$DATA_DIR"
cp -r data/. "$DATA_DIR/"
sed -i "s|copytree(\"data\"|copytree(\"$DATA_DIR\"|" "$INSTALL_DIR/$SCRIPT_NAME"

# Make the script executable
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

echo "Installed: $INSTALL_DIR/$SCRIPT_NAME"

# Check if ~/.local/bin is in the PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "WARNING: $INSTALL_DIR is not in your PATH."
    read -rp "Add to path ? [Y/n] " ans
    if [[ "$ans" =~ ^[yY]?$ ]]; then
        [[ "$SHELL" == */zsh ]] && RC_FILE="$HOME/.zshrc" || RC_FILE="$HOME/.bashrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC_FILE"
        echo " Done. Run: source $RC_FILE"
    fi
    echo ""
fi

