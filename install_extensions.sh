#!/bin/bash

# ┌────────────────────────────────────────────┐
# │ VS Code Extension Installer                │
# └────────────────────────────────────────────┘
# Installs essential VS Code extensions for Python development.
# Safe to run multiple times (idempotent).

# ─── Dry-run safety ──────────────────────────
set -e  # Exit on error
trap 'echo "Something went wrong. Try rerunning or ask for help."' ERR

# ─── Shared Extensions ───────────────────────
SHARED_EXTENSIONS=(
  ms-python.python
  ms-python.vscode-pylance
  ms-toolsai.jupyter
  ms-python.black-formatter
  ms-python.debugpy
  ms-python.vscode-python-envs
  github.copilot
  github.copilot-chat
  github.vscode-pull-request-github
  kevinrose.vsc-python-indent
)

# ─── Install Function ────────────────────────
install_extensions() {
  for ext in "${@}"; do
    echo "Installing: $ext"
    code --install-extension "$ext" || echo "Already installed or failed: $ext"
  done
}

# ─── Run Installer ───────────────────────────
install_extensions "${SHARED_EXTENSIONS[@]}"
