import os
import json
import logging
import inquirer
from .audio_processor import AudioProcessor
import argparse
from .config import whisper_models

# Set up logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def main():
    parser = argparse.ArgumentParser(description='Process some audio files.')
    parser.add_argument('--audio_dir', type=str, default='../sounds', help='Directory containing audio files')
    parser.add_argument('--device', type=str, default='cpu', help='Device to use for processing')
    parser.add_argument('--hf_auth_token', type=str, required=False, help='Pass Hugging Face Auth Token or set HF_AUTH_TOKEN environment variable')

    args = parser.parse_args()

    hf_auth_token = os.getenv("HF_AUTH_TOKEN", args.hf_auth_token)
    if not hf_auth_token:
        logging.error("Hugging Face Auth Token is required. Pass it as an argument or set the HF_AUTH_TOKEN environment variable.")
        return

    # Model selection using inquirer
    questions = [
        inquirer.List('model',
                      message="Select a model for audio processing",
                      choices=whisper_models,
                      ),
    ]
    answers = inquirer.prompt(questions)
    model = answers['model']

    audio_dir = args.audio_dir
    device = args.device

  

    processor = AudioProcessor(audio_dir, device, hf_auth_token, model)
    results = processor.process()
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    results_json_path = os.path.join(results_dir, "results.json")
    with open(results_json_path, "w") as results_json_file:
        json.dump(results, results_json_file, indent=4)

if __name__ == "__main__":
    main()
