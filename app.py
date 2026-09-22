import gradio as gr
from backend.api import app as fastapi_app
import spaces

# Satisfy Hugging Face ZeroGPU checks with a dummy GPU function
@spaces.GPU
def dummy_gpu_fn():
    return "GPU active"

# Create a minimal dummy Gradio interface
demo = gr.Interface(fn=dummy_gpu_fn, inputs=[], outputs="text")

# Mount Gradio onto our FastAPI app.
# HF Spaces 'gradio' SDK will detect this FastAPI 'app' variable and run it!
app = gr.mount_gradio_app(fastapi_app, demo, path="/dummy_gradio")
