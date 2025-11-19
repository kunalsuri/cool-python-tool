#!/bin/bash

# Quick Start Script for eBook & PDF Utilities Suite
# This script sets up the environment and runs the Streamlit application

set -e  # Exit on error
set -u  # Exit on undefined variable

echo "📚 eBook & PDF Utilities Suite - Quick Start"
echo "============================================="
echo ""

# Function to add Python installation to arrays
add_python() {
    local path=$1
    if [ -x "$path" ]; then
        local version=$($path --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        if [ -n "$version" ]; then
            PYTHON_PATHS+=("$path")
            PYTHON_VERSIONS+=("$version")
        fi
    fi
}

# Function to check if path is duplicate
is_duplicate() {
    local path=$1
    local real_path=$(readlink -f "$path" 2>/dev/null || realpath "$path" 2>/dev/null || echo "$path")
    
    for unique in "${UNIQUE_PATHS[@]}"; do
        local unique_real=$(readlink -f "$unique" 2>/dev/null || realpath "$unique" 2>/dev/null || echo "$unique")
        if [ "$real_path" = "$unique_real" ]; then
            return 0  # Is duplicate
        fi
    done
    return 1  # Not duplicate
}

echo "🔍 Searching for Python installations..."
echo ""

# Arrays to store Python paths and versions
declare -a PYTHON_PATHS=()
declare -a PYTHON_VERSIONS=()

# Search common locations
# Homebrew installations
if command -v brew &> /dev/null; then
    BREW_PREFIX=$(brew --prefix)
    for py in "$BREW_PREFIX"/bin/python3*; do
        [ -f "$py" ] && add_python "$py"
    done
fi

# System Python
add_python "/usr/bin/python3"

# pyenv installations
if command -v pyenv &> /dev/null; then
    while IFS= read -r py_version; do
        add_python "$HOME/.pyenv/versions/$py_version/bin/python3"
    done < <(pyenv versions --bare 2>/dev/null)
fi

# Check /usr/local/bin
for py in /usr/local/bin/python3*; do
    [ -f "$py" ] && add_python "$py"
done

# Remove duplicates based on actual path (follow symlinks)
declare -a UNIQUE_PATHS=()
declare -a UNIQUE_VERSIONS=()
for i in "${!PYTHON_PATHS[@]}"; do
    if ! is_duplicate "${PYTHON_PATHS[$i]}"; then
        UNIQUE_PATHS+=("${PYTHON_PATHS[$i]}")
        UNIQUE_VERSIONS+=("${PYTHON_VERSIONS[$i]}")
    fi
done

# Display found Python installations
if [ ${#UNIQUE_PATHS[@]} -eq 0 ]; then
    echo "❌ No Python installations found!"
    echo "   Please install Python 3.8 or higher."
    exit 1
fi

echo "Found ${#UNIQUE_PATHS[@]} Python installation(s):"
echo ""
for i in "${!UNIQUE_PATHS[@]}"; do
    echo "[$((i+1))] Python ${UNIQUE_VERSIONS[$i]}"
    echo "    Path: ${UNIQUE_PATHS[$i]}"
    echo ""
done

# Select Python version
PYTHON_PATH=""
PYTHON_VERSION=""

if [ ${#UNIQUE_PATHS[@]} -eq 1 ]; then
    # Auto-select if only one found
    PYTHON_PATH="${UNIQUE_PATHS[0]}"
    PYTHON_VERSION="${UNIQUE_VERSIONS[0]}"
    echo "✅ Auto-selected: Python $PYTHON_VERSION"
else
    # Get user choice
    while true; do
        read -p "Select Python version [1-${#UNIQUE_PATHS[@]}]: " choice
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#UNIQUE_PATHS[@]}" ]; then
            PYTHON_PATH="${UNIQUE_PATHS[$((choice-1))]}"
            PYTHON_VERSION="${UNIQUE_VERSIONS[$((choice-1))]}"
            break
        else
            echo "❌ Invalid selection. Please enter a number between 1 and ${#UNIQUE_PATHS[@]}"
        fi
    done
    
    echo ""
    echo "✅ Selected: Python $PYTHON_VERSION"
fi

echo "   Path: $PYTHON_PATH"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment with Python $PYTHON_VERSION..."
    "$PYTHON_PATH" -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip -q

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

echo "✅ Dependencies installed"
echo ""

# Check for Tesseract (optional)
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract OCR found: $(tesseract --version | head -1)"
else
    echo "⚠️  Tesseract OCR not found (optional for OCR functionality)"
    echo "   Install with: brew install tesseract (macOS) or apt-get install tesseract-ocr (Linux)"
fi

echo ""
echo "📌 VS Code Setup (Optional):"
echo "   1. Press Cmd+Shift+P (or Ctrl+Shift+P on Windows/Linux)"
echo "   2. Type 'Python: Select Interpreter'"
echo "   3. Choose the interpreter from venv/bin/python"
echo "   Or click on the Python version in the bottom-right status bar."
echo ""

# Try to trigger VS Code interpreter selection if code command is available
if command -v code &> /dev/null; then
    echo "🔧 Attempting to set VS Code interpreter..."
    code --command python.setInterpreter "$(pwd)/venv/bin/python" 2>/dev/null || true
fi

echo ""
echo "🚀 Starting application..."
echo ""
echo "   The application will open in your default browser"
echo "   Press Ctrl+C to stop the application"
echo ""
echo "============================================="
echo ""

# Run the Streamlit app
streamlit run app.py
