import os
from functools import lru_cache
from typing import Dict
LOCAL_MODEL = os.path.join("models", "moodmate-emotion-model")
FALLBACK_MODEL = "j-hartmann/emotion-english-distilroberta-base"
@lru_cache(maxsize=1)
def _get_classifier():
 from transformers import pipeline
 model = LOCAL_MODEL if os.path.isdir(LOCAL_MODEL) else FALLBACK_MODEL
 return pipeline("text-classification", model=model, top_k=None)
def detect_emotions(text: str, threshold: float = 0.15) -> Dict[str, float]:
 """Return emotions scoring above threshold, e.g. {'sadness': 0.81}."""
 results = _get_classifier()(text)[0]
 return {r["label"]: round(r["score"], 3)
 for r in results if r["score"] >= threshold}
if __name__ == "__main__":
 print(detect_emotions("I feel so alone lately and nobody understands me"))