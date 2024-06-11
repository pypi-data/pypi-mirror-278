import os
import json
import logging
import inquirer
import argparse
from .audio_processor import AudioProcessor
from .config import whisper_models

# Set up logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def main():
    parser = argparse.ArgumentParser(description='Process some audio files.')
    parser.add_argument('--file_path', type=str, default='../sounds', help='Directory containing audio files')
    parser.add_argument('--device', type=str, default='cuda', help='Device to use for processing')
    parser.add_argument('--hf_auth_token', type=str, required=False, help='Pass Hugging Face Auth Token or set HF_AUTH_TOKEN environment variable')

    args = parser.parse_args()

    hf_auth_token = os.getenv("HF_AUTH_TOKEN", args.hf_auth_token)
    if not hf_auth_token:
        logging.error("Hugging Face Auth Token is required. Pass it as an argument or set the HF_AUTH_TOKEN environment variable.")
        return

    fastest_model = "distil-whisper/distil-large-v3"  
    recommended_model = "openai/whisper-large-v3"  

    # Create a dictionary to map displayed options to actual model names
    model_options = {
        f"{model} (fastest)" if model == fastest_model else f"{model} (recommended)" if model == recommended_model else model: model
        for model in whisper_models
    }

    questions = [
        inquirer.List('model',
                      message="Select a model for audio processing",
                      choices=list(model_options.keys()),
                      ),
    ]
    answers = inquirer.prompt(questions)
    model = model_options[answers['model']]

    file_path = args.file_path
    device = args.device

    processor = AudioProcessor(file_path, device, hf_auth_token, model)
    results = processor.process()

    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    print('''
        Results are saved in the results directory by default as a JSON file.
        You can change the output format in the audio_processor.py file.
    ''')
    
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    results_json_path = os.path.join(results_dir, f"{file_name_without_extension}.json")
    with open(results_json_path, "w") as results_json_file:
        json.dump(results, results_json_file, indent=4)

if __name__ == "__main__":
    main()
