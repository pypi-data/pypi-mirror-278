
import gradio as gr
from app import demo as app
import os

_docs = {'Model4DGS': {'description': 'Component allows users to upload or view 4D Gaussian Splatting files (.splat).', 'members': {'__init__': {'value': {'type': 'str | Callable | None', 'default': 'None', 'description': 'path to (.splat) file to show in model4DGS viewer. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'fps': {'type': 'float', 'default': '8', 'description': None}, 'height': {'type': 'int | None', 'default': 'None', 'description': 'height of the model4DGS component, in pixels.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': None}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': None}, 'every': {'type': 'float | None', 'default': 'None', 'description': None}, 'container': {'type': 'bool', 'default': 'True', 'description': None}, 'scale': {'type': 'int | None', 'default': 'None', 'description': None}, 'min_width': {'type': 'int', 'default': '160', 'description': None}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': None}, 'visible': {'type': 'bool', 'default': 'True', 'description': None}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': None}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': None}, 'render': {'type': 'bool', 'default': 'True', 'description': None}}, 'postprocess': {'value': {'type': 'List[str] | str | None', 'description': "The output data received by the component from the user's function in the backend."}}, 'preprocess': {'return': {'type': 'List[str] | None', 'description': "The preprocessed input data sent to the user's function in the backend."}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the Model4DGS changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the Model4DGS.'}, 'edit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user edits the Model4DGS (e.g. image) using the built-in editor.'}, 'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the Model4DGS using the X button for the component.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'Model4DGS': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_model4dgs`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_model4dgs/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_model4dgs"></a>  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_model4dgs
```

## Usage

```python
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
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `Model4DGS`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["Model4DGS"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["Model4DGS"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, the preprocessed input data sent to the user's function in the backend.
- **As output:** Should return, the output data received by the component from the user's function in the backend.

 ```python
def predict(
    value: List[str] | None
) -> List[str] | str | None:
    return value
```
""", elem_classes=["md-custom", "Model4DGS-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          Model4DGS: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
