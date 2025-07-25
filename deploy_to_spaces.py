#!/usr/bin/env python3
"""
Deployment script for Hugging Face Spaces

This script helps you deploy the NSFW Novel Generator to Hugging Face Spaces
with proper configuration and file preparation.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    try:
        import huggingface_hub
        print("✅ huggingface_hub is installed")
    except ImportError:
        print("❌ huggingface_hub not found. Install with: pip install huggingface_hub")
        return False
    
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is available")
        else:
            print("❌ Git not found. Please install Git")
            return False
    except FileNotFoundError:
        print("❌ Git not found. Please install Git")
        return False
    
    return True

def prepare_deployment_files():
    """Prepare files for deployment"""
    print("📁 Preparing deployment files...")
    
    # Files needed for Spaces deployment
    required_files = [
        'Dockerfile',
        'app_spaces.py',
        'model_integration_pipeline.py',
        'requirements.txt',
        'README_SPACES.md',
        'spaces_config.yaml'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files are present")
    return True

def create_spaces_directory(space_name):
    """Create a directory for Spaces deployment"""
    spaces_dir = f"spaces_{space_name}"
    
    if os.path.exists(spaces_dir):
        print(f"📁 Directory {spaces_dir} already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            return None
        shutil.rmtree(spaces_dir)
    
    os.makedirs(spaces_dir)
    print(f"✅ Created directory: {spaces_dir}")
    return spaces_dir

def copy_deployment_files(spaces_dir):
    """Copy necessary files to the Spaces directory"""
    files_to_copy = [
        'Dockerfile',
        'app_spaces.py',
        'model_integration_pipeline.py',
        'requirements.txt',
        'README_SPACES.md'
    ]
    
    for file in files_to_copy:
        shutil.copy2(file, spaces_dir)
        print(f"📄 Copied {file}")
    
    # Copy and rename spaces config
    shutil.copy2('spaces_config.yaml', os.path.join(spaces_dir, 'README.md'))
    
    # Create a proper README.md for the Space
    readme_content = """
---
title: NSFW Novel Generator
sdk: gradio
sdk_version: 4.0.0
app_file: app_spaces.py
pinned: false
license: mit
short_description: AI-powered NSFW novel generator using UnfilteredAI/NSFW-3B
tags:
  - text-generation
  - creative-writing
  - nsfw
  - transformers
  - pipeline
models:
  - UnfilteredAI/NSFW-3B
hardware: t4-small
suggest_hardware: t4-small
---

# NSFW Novel Generator

🚀 **AI-powered NSFW novel generator using UnfilteredAI/NSFW-3B with pipeline optimization!**

## Features

- **Pipeline Optimization**: Uses Hugging Face pipeline for efficient inference
- **GPU Acceleration**: Automatic GPU detection and utilization
- **Interactive UI**: Clean Gradio interface with real-time generation
- **Parameter Control**: Temperature, top-p, max tokens adjustment
- **Genre Selection**: Multiple genre options for guided generation

## Usage

1. Enter your story prompt
2. Select genre and length preferences
3. Adjust creativity parameters
4. Click "Generate Story"

## ⚠️ Content Warning

This application generates adult content. Use responsibly and ensure compliance with local laws.

## Technical Details

- **Model**: UnfilteredAI/NSFW-3B
- **Framework**: Hugging Face Transformers with Pipeline API
- **Interface**: Gradio
- **Optimization**: Automatic device mapping and memory management
"""
    
    with open(os.path.join(spaces_dir, 'README.md'), 'w') as f:
        f.write(readme_content)
    
    print("✅ All files copied successfully")

def initialize_git_repo(spaces_dir, space_url):
    """Initialize git repository and set up remote"""
    os.chdir(spaces_dir)
    
    # Initialize git repo
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit: NSFW Novel Generator'], check=True)
    
    # Add remote
    subprocess.run(['git', 'remote', 'add', 'origin', space_url], check=True)
    
    print("✅ Git repository initialized")

def main():
    print("🚀 Hugging Face Spaces Deployment Script")
    print("=========================================\n")
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Prepare files
    if not prepare_deployment_files():
        print("❌ File preparation failed.")
        sys.exit(1)
    
    # Get user input
    print("\n📝 Space Configuration")
    username = input("Enter your Hugging Face username: ")
    space_name = input("Enter your Space name (e.g., nsfw-novel-generator): ")
    
    if not username or not space_name:
        print("❌ Username and space name are required")
        sys.exit(1)
    
    space_url = f"https://huggingface.co/spaces/{username}/{space_name}"
    
    print(f"\n🎯 Deployment Target: {space_url}")
    
    # Create deployment directory
    spaces_dir = create_spaces_directory(space_name)
    if not spaces_dir:
        print("❌ Directory creation cancelled")
        sys.exit(1)
    
    # Copy files
    copy_deployment_files(spaces_dir)
    
    # Initialize git
    try:
        initialize_git_repo(spaces_dir, space_url)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git initialization failed: {e}")
        sys.exit(1)
    
    print("\n🎉 Deployment preparation complete!")
    print("\n📋 Next Steps:")
    print(f"1. Create a new Space at: https://huggingface.co/new-space")
    print(f"   - Owner: {username}")
    print(f"   - Space name: {space_name}")
    print(f"   - SDK: Gradio")
    print(f"   - Hardware: T4 small (recommended)")
    print(f"   - Visibility: Private (recommended for NSFW content)")
    print(f"\n2. Push your code:")
    print(f"   cd {spaces_dir}")
    print(f"   git push origin main")
    print(f"\n3. Your Space will be available at: {space_url}")
    print(f"\n⚠️  Remember to set appropriate content warnings and age restrictions!")

if __name__ == "__main__":
    main()