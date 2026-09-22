import uvicorn
from backend.api import app
import os

# Satisfy Hugging Face ZeroGPU checks even though we only use CPU for scikit-learn
try:
    import spaces
    @spaces.GPU
    def dummy_gpu_fn():
        pass
except ImportError:
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
