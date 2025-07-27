#!/usr/bin/env python3
"""
Text-to-Audio Converter using Tortoise TTS

This script takes a text file as input and converts its entire content
into a single WAV audio file.

Usage:
    python convert_to_audio.py <input_text_file> <output_audio_file.wav>
"""

import os
import sys
import argparse
import re
import torch
import torchaudio

# --- Setup Paths and Environment ---

# Set TORTOISE_MODELS_DIR before importing Tortoise
models_dir = os.path.join(os.path.expanduser("~"), ".cache/tortoise/models/")
os.environ['TORTOISE_MODELS_DIR'] = models_dir

# Determine the base directory of the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Add the local tortoise-tts repo to the Python path
tortoise_path = os.path.join(script_dir, "tortoise-tts")
if tortoise_path not in sys.path:
    sys.path.insert(0, tortoise_path)

try:
    from tortoise.api import TextToSpeech
    from tortoise.utils.audio import load_voice
except ImportError:
    print("Error: Could not import Tortoise TTS. Make sure you've run the setup script")
    print(f"and the path '{tortoise_path}' is correct.")
    sys.exit(1)

def main():
    """Main function to handle argument parsing and conversion process."""
    parser = argparse.ArgumentParser(
        description='Convert a text file to a WAV audio file using Tortoise TTS.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input_file', type=str, nargs='?', default=os.path.join(script_dir, 'input', 'example.txt'), help='Path to the input text file. Defaults to input/example.txt')
    parser.add_argument('output_file', type=str, nargs='?', default=os.path.join(script_dir, 'output', 'output.wav'), help='Path to save the output WAV file. Defaults to output/output.wav')
    parser.add_argument(
        '--voice', type=str, default='random', 
        help='Voice to use for synthesis. Can be a name from the voices dir or \'random\'.'
    )
    parser.add_argument(
        '--preset', type=str, default='ultra_fast', 
        help='TTS preset to use (ultra_fast, fast, standard, high_quality).'
    )

    args = parser.parse_args()

    # --- Validate Inputs ---
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found at '{args.input_file}'")
        sys.exit(1)

    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    # --- Check for GPU ---
    if torch.cuda.is_available():
        print(f"\n✅ GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("\n⚠️ No GPU detected. Processing will be slow.")

    # --- Read Text ---
    print(f"📖 Reading text from: {args.input_file}")
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    if not text.strip():
        print("Error: Input file is empty.")
        sys.exit(1)

    # --- Initialize TTS ---
    print("🐢 Initializing Tortoise TTS... (this may take a moment)")
    # NOTE: DeepSpeed is temporarily disabled due to a version compatibility issue.
    # The script will still be much faster due to other optimizations.
    tts = TextToSpeech(use_deepspeed=False, kv_cache=True, half=True)

    # --- Load Voice ---
    print(f"🗣️ Loading voice: {args.voice}")
    if args.voice == 'random':
        voice_samples, conditioning_latents = None, None
    else:
        voice_samples, conditioning_latents = load_voice(args.voice)

    # --- Generate Speech in Chunks ---
    print(f"🔊 Generating speech with preset: {args.preset}")
    print("Splitting text into sentences...")
    # Filter out slide titles and join the rest of the text
    content_lines = [line for line in text.split('\n') if not line.strip().startswith('Slide ')]
    full_text = ' '.join(content_lines).replace('"', '')
    # Split into sentences using regex, preserving delimiters
    text_chunks = re.split(r'(?<=[.?!])\s+', full_text)
    text_chunks = [chunk.strip() for chunk in text_chunks if chunk.strip()]
    all_parts = []

    for i, chunk in enumerate(text_chunks):
        print(f"    -> Processing chunk {i+1}/{len(text_chunks)}...")
        # Using tts_with_preset and 'ultra_fast' is the most reliable way to ensure speed.
        # This preset is optimized to avoid expensive computations.
        gen = tts.tts_with_preset(
            chunk,
            voice_samples=voice_samples,
            conditioning_latents=conditioning_latents,
            preset='ultra_fast'
        )
        all_parts.append(gen.squeeze(0).cpu())

    # --- Concatenate and Save Audio ---
    print("🔗 Concatenating audio chunks...")
    full_audio = torch.cat(all_parts, dim=-1)

    print(f"💾 Saving final audio to: {args.output_file}")
    torchaudio.save(args.output_file, full_audio, 24000)

    print("\n✅ Conversion complete!")

if __name__ == '__main__':
    main()
