#!/bin/bash
#
# Setup script for the Tortoise TTS Environment on Ubuntu

# --- Configuration ---
CONDA_ENV_NAME="tortoise"
PYTHON_VERSION="3.9"

# --- Helper Functions ---
echo_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

echo_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

echo_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# --- Main Script ---
echo_info "Starting Tortoise TTS environment setup..."

# 1. Check for Conda
if ! command -v conda &> /dev/null; then
    echo_error "Conda is not installed or not in your PATH. Please install Miniconda or Anaconda first."
    exit 1
fi

# 2. Create Conda Environment
echo_info "Creating Conda environment '$CONDA_ENV_NAME' with Python $PYTHON_VERSION..."
conda create -n $CONDA_ENV_NAME python=$PYTHON_VERSION -y
if [ $? -ne 0 ]; then
    echo_error "Failed to create Conda environment. Aborting."
    exit 1
fi

# 3. Activate Environment and Install Dependencies
echo_info "Activating environment and installing dependencies from requirements.txt..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $CONDA_ENV_NAME

# Install PyTorch with CUDA support first
echo_info "Installing PyTorch with CUDA support..."
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install remaining packages
echo_info "Installing other required packages..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo_error "Failed to install Python packages. Please check the requirements.txt file and your network connection."
    exit 1
fi

# --- Final Instructions ---
echo_success "Setup complete!"
echo_info "To activate the environment, run: conda activate $CONDA_ENV_NAME"
echo_info "The first time you run the conversion script, Tortoise TTS will download the necessary models (~2GB). This is a one-time process."
echo_info "To run the conversion script with default settings, use: python convert_to_audio.py"
