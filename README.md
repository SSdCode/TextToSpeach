# Text-to-Speech (TTS) Conversion with Tortoise

This repository provides a complete, self-contained environment for converting text files into high-quality speech audio using the powerful Tortoise TTS model. It has been structured for ease of use and is designed to work seamlessly on Ubuntu.

## Features

- **High-Quality Synthesis**: Leverages the Tortoise TTS model for natural-sounding speech.
- **GPU Accelerated**: Automatically uses a CUDA-enabled GPU if available for significantly faster processing.
- **Handles Long Text**: Intelligently splits large text files into sentences to avoid model limitations.
- **Portable Environment**: Self-contained script and library, easy to clone and run anywhere.
- **Easy Setup**: A simple setup script to create the Conda environment and install all dependencies.
- **Customizable**: Choose from a variety of voices and generation presets (`ultra_fast`, `fast`, `standard`, `high_quality`).

## Prerequisites

Before you begin, ensure you have the following installed on your Ubuntu system:

1.  **Git**: For cloning the repository.
    ```bash
    sudo apt update && sudo apt install git
    ```
2.  **Miniconda or Anaconda**: For managing the Python environment. We recommend [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for a lightweight installation.

## Setup Instructions

Follow these steps to get the project up and running.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <your-repository-url>
```

### 2. Run the Setup Script

The provided setup script will create a Conda environment and install all the necessary Python packages, including PyTorch with CUDA support.

Make the script executable and run it:

```bash
chmod +x setup.sh
./setup.sh
```

The script will handle everything. Once it's finished, you're ready to go!

### 3. Automatic Model Download

**Important**: The first time you run the conversion script, Tortoise TTS will automatically download its pre-trained models. This is a **one-time download of about 2GB**. Please be patient, as this can take a few minutes depending on your internet connection.

The models will be cached in `~/.cache/tortoise/models/` for all future runs.

## Usage

### 1. Activate the Conda Environment

Before running the script, you must activate the `tortoise` environment:

```bash
conda activate tortoise
```

### 2. Run the Conversion Script

The `convert_to_audio.py` script is flexible. You can run it with or without arguments.

**Default Conversion:**

To convert the sample `input/example.txt` file and save it to `output/output.wav`, simply run:

```bash
python convert_to_audio.py
```

**Custom Conversion:**

You can specify your own input file, output file, voice, and preset.

```bash
python convert_to_audio.py <path_to_input_file> <path_to_output_file> --voice <voice_name> --preset <preset_name>
```

**Example:**

This command converts `my_script.txt` into `my_audio.wav` using the `tom` voice and the `ultra_fast` preset for maximum speed.

```bash
python convert_to_audio.py input/my_script.txt output/my_audio.wav --voice tom --preset ultra_fast
```

### Available Voices

You can use any of the pre-configured voices located in the `tortoise-tts/tortoise/voices/` directory. Common options include: `tom`, `emma`, `daniel`, `freeman`, `weaver`, and `random` (for a new, unique voice).
