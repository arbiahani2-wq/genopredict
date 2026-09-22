import gradio as gr
from backend.logic import run_simulation_and_prediction
import json
import spaces

@spaces.GPU
def simulate(father_data_str, mother_data_str, age, sex_opts_str, family_history):
    # Parse the JSON strings back into Python objects
    father_data = json.loads(father_data_str)
    mother_data = json.loads(mother_data_str)
    sex_opts = json.loads(sex_opts_str)
    
    # Run the existing logic
    results = run_simulation_and_prediction(father_data, mother_data, int(age), sex_opts, int(family_history))
    
    # Return as JSON string for Gradio API
    return json.dumps(results)

# Create a minimal Gradio interface to satisfy ZeroGPU
demo = gr.Interface(
    fn=simulate,
    inputs=[
        gr.Textbox(label="Father Data (JSON)"),
        gr.Textbox(label="Mother Data (JSON)"),
        gr.Number(label="Age"),
        gr.Textbox(label="Sex Options (JSON)"),
        gr.Number(label="Family History")
    ],
    outputs=gr.Textbox(label="Results (JSON)"),
    title="GenoPredict API Endpoint",
    description="This is a headless API endpoint for GenoPredict. It is not meant to be used via UI."
)

if __name__ == "__main__":
    demo.launch()
