#!/bin/bash

# Run Script for Cool Python Tools
# This script checks the environment and runs the selected application

set -e  # Exit on error
set -u  # Exit on undefined variable

echo "🚀 Cool Python Tools - Launcher"
echo "==============================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment (.venv) not found!"
    echo ""
    read -p "Would you like to run the setup script now? (y/n): " run_setup
    if [[ "$run_setup" =~ ^[Yy]$ ]]; then
        if [ -f "./setup.sh" ]; then
            chmod +x ./setup.sh
            ./setup.sh
        else
            echo "❌ setup.sh not found. Please ensure you have the full repository."
            exit 1
        fi
    else
        echo "Please run ./setup.sh to create the environment first."
        exit 1
    fi
fi

# Activate virtual environment
source .venv/bin/activate

# Get Python info
PY_VERSION=$(python --version)
PY_PATH=$(which python)

echo "✅ Using Environment:"
echo "   Version: $PY_VERSION"
echo "   Path:    $PY_PATH"
echo ""

echo "Please select the project you want to run:"
echo "1) PyDocFlow-Studio (PDF & eBook Utilities)"
echo "2) Py-YT-Downloader (YouTube Downloader)"
echo "3) Exit"

read -p "Enter your choice [1-3]: " project_choice

case $project_choice in
    1)
        echo "🚀 Preparing PyDocFlow-Studio..."
        if [ -f "PyDocFlow-Studio/requirements.txt" ]; then
            echo "📥 Checking dependencies for PyDocFlow-Studio..."
            pip install -r PyDocFlow-Studio/requirements.txt -q
        fi
        echo "▶️ Running PyDocFlow-Studio..."
        streamlit run PyDocFlow-Studio/app.py
        ;;
    2)
        echo "🚀 Preparing Py-YT-Downloader..."
        if [ -f "Py-YT-Downloader/requirements.txt" ]; then
            echo "📥 Checking dependencies for Py-YT-Downloader..."
            pip install -r Py-YT-Downloader/requirements.txt -q
        fi
        echo "▶️ Running Py-YT-Downloader..."
        streamlit run Py-YT-Downloader/youtube_downloader.py
        ;;
    3)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
