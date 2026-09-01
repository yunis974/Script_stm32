#!/usr/bin/env bash
set -e

INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="scriptInit"  # final command name
SOURCE_FILE="mcu_project.py"

# Create the directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy the script to its destination, with the right name
cp "$SOURCE_FILE" "$INSTALL_DIR/$SCRIPT_NAME"

# Make the script executable
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

echo "Installed: $INSTALL_DIR/$SCRIPT_NAME"

# Check if ~/.local/bin is in the PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "WARNING: $INSTALL_DIR is not in your PATH."
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi