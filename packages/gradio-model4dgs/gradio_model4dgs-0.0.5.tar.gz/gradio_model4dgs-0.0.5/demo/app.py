import gradio as gr
from gradio_model4dgs import Model4DGS
import os

image_dir = os.path.join(os.path.dirname(__file__), "assets")

if os.path.exists(image_dir) and os.path.isdir(image_dir) and os.listdir(image_dir):
    examples = [os.path.join(image_dir, file) for file in os.listdir(image_dir)]
else:
    examples = [os.path.join(os.path.dirname(__file__), example) for example in Model4DGS().example_inputs()]

with gr.Blocks() as demo:
    with gr.Row():
        Model4DGS(value=examples, label="4D Model", fps=8)

if __name__ == "__main__":
    demo.launch(share=True)