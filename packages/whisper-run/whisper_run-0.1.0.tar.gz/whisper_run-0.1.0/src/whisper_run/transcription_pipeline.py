from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
import time
from typing import List, Dict
class TranscriptionPipeline:
    def __init__(self, model_name: str, device: str) -> None:
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(model_name, torch_dtype=torch_dtype, low_cpu_mem_usage=True)
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )

    def run(self, file_path: str) -> List[Dict[str, float]]:
        start_time = time.time()
        #result = self.pipe(file_path, batch_size=8, generate_kwargs={"language": "turkish"})
        result = self.pipe(file_path, batch_size=8)

        elapsed_time = time.time() - start_time
        segments = []
        for chunk in result['chunks']:
            start = chunk.get('timestamp', [None, None])[0]
            end = chunk.get('timestamp', [None, None])[1]
            text = chunk.get('text', '')
            if start is not None and end is None:
                end = start + 2.0  # Default duration if end is missing
            if start is not None:
                segments.append({
                    'start': round(start, 2),
                    'end': round(end, 2) if end is not None else None,
                    'text': text
                })
        print(f"Transcription completed in {elapsed_time:.2f} seconds")
        return segments
