from transformers import AutoTokenizer, AutoModelForCausalLM
from app.config import MODEL_NAME
import threading

_lock = threading.Lock()
_model = None
_tokenizer = None

def get_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        with _lock:
            if _model is None or _tokenizer is None:
                _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
                _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    return _model, _tokenizer
