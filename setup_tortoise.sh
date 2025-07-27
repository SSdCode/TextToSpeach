#!/bin/bash

echo "🔧 Setting up Tortoise TTS on Ubuntu..."

# Exit if any command fails
set -e

# Step 1: Ensure Miniconda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Miniconda first from https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Step 2: Create new Conda environment
echo "📦 Creating Conda environment..."
conda create -n tortoise python=3.9 -y

# ✅ Enable conda commands in this script
source ~/miniconda3/etc/profile.d/conda.sh

conda activate tortoise

# Step 3: Install PyTorch with CUDA support for RTX 4060 (CUDA 11.8)
echo "🔥 Installing PyTorch with CUDA support..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Step 4: Install required packages
echo "📚 Installing Tortoise-compatible transformers & tokenizers..."
pip install transformers==4.31.0 tokenizers==0.13.3

# Step 5: Clone Tortoise repo
echo "📁 Cloning Tortoise repo..."
cd ~/Downloads || exit
git clone https://github.com/neonbjb/tortoise-tts.git
cd tortoise-tts

# Step 6: Install requirements
echo "📦 Installing Python requirements..."
pip install -r requirements.txt

# Step 7: Download models (first-time run will trigger this automatically too)
echo "⬇️ Downloading Tortoise models..."
python tortoise/utils/download_models.py

# Step 8: Test synthesis
echo "🎤 Running test TTS synthesis..."
python tortoise/do_tts.py --text "Hello, this is a test of Tortoise TTS on an RTX 4060." --voice "daniel"

echo "✅ Tortoise TTS setup complete!"
