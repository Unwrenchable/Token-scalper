#!/usr/bin/env bash
# Build script for Render.com and other deployment platforms
# This script upgrades pip to the latest version before installing dependencies

set -e  # Exit on error

echo "===> Upgrading pip to latest version..."
pip install --upgrade pip

echo "===> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "===> Build completed successfully!"
