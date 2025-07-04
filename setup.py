#!/usr/bin/env python3
"""
Setup script for Excel Translator App
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required Python packages."""
    print("Installing dependencies...")
    
    try:
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"✗ Python 3.10+ required, current version: {version.major}.{version.minor}")
        return False
    
    print(f"✓ Python version: {version.major}.{version.minor}")
    return True

def create_directories():
    """Create necessary directories."""
    directories = [
        "config",
        "i18n", 
        "assets",
        "translator",
        "excel",
        "ui"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✓ Directories created")

def setup_environment():
    """Set up the development environment."""
    print("Setting up Excel Translator App...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    print("\n✓ Setup completed successfully!")
    print("\nTo run the application:")
    print("  python main.py")
    print("\nBefore using the app:")
    print("  1. Get your DeepL API key from https://www.deepl.com/pro-api")
    print("  2. Open the app and go to Settings to enter your API key")
    print("  3. Select an Excel file and start translating!")
    
    return True

if __name__ == "__main__":
    if setup_environment():
        sys.exit(0)
    else:
        sys.exit(1)
