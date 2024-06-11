
import gradio as gr
from app import demo as app
import os

_docs = {'ModifiableGallery': {'description': 'Creates a gallery component that allows displaying a grid of images, and optionally captions. If used as an input, the user can upload images to the gallery.\nIf used as an output, the user can click on individual images to view them at a higher resolution.\n', 'members': {'__init__': {'value': {'type': 'list[\n        numpy.ndarray\n        | PIL.Image.Image\n        | str\n        | pathlib.Path\n        | tuple\n    ]\n    | Callable\n    | None', 'default': 'None', 'description': 'List of images to display in the gallery by default. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'format': {'type': 'str', 'default': '"webp"', 'description': "Format to save images before they are returned to the frontend, such as 'jpeg' or 'png'. This parameter only applies to images that are returned from the prediction function as numpy arrays or PIL Images. The format should be supported by the PIL library."}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'columns': {'type': 'int | tuple | None', 'default': '2', 'description': 'Represents the number of images that should be shown in one row, for each of the six standard screen sizes (<576px, <768px, <992px, <1200px, <1400px, >1400px). If fewer than 6 are given then the last will be used for all subsequent breakpoints'}, 'rows': {'type': 'int | tuple | None', 'default': 'None', 'description': 'Represents the number of rows in the image grid, for each of the six standard screen sizes (<576px, <768px, <992px, <1200px, <1400px, >1400px). If fewer than 6 are given then the last will be used for all subsequent breakpoints'}, 'height': {'type': 'int | float | None', 'default': 'None', 'description': 'The height of the gallery component, specified in pixels if a number is passed, or in CSS units if a string is passed. If more images are displayed than can fit in the height, a scrollbar will appear.'}, 'allow_preview': {'type': 'bool', 'default': 'False', 'description': 'If True, images in the gallery will be enlarged when they are clicked. Default is True.'}, 'preview': {'type': 'bool | None', 'default': 'False', 'description': 'If True, ModifiableGallery will start in preview mode, which shows all of the images as thumbnails and allows the user to click on them to view them in full size. Only works if allow_preview is True.'}, 'selected_index': {'type': 'int | None', 'default': 'None', 'description': 'The index of the image that should be initially selected. If None, no image will be selected at start. If provided, will set ModifiableGallery to preview mode unless allow_preview is set to False.'}, 'object_fit': {'type': '"contain" | "cover" | "fill" | "none" | "scale-down" | None', 'default': 'None', 'description': 'CSS object-fit property for the thumbnail images in the gallery. Can be "contain", "cover", "fill", "none", or "scale-down".'}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.'}, 'show_download_button': {'type': 'bool | None', 'default': 'True', 'description': 'If True, will show a download button in the corner of the selected image. If False, the icon does not appear. Default is True.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'If True, the gallery will be interactive, allowing the user to upload images. If False, the gallery will be static. Default is True.'}, 'type': {'type': '"numpy" | "pil" | "filepath"', 'default': '"filepath"', 'description': 'The format the image is converted to before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image. If the image is SVG, the `type` is ignored and the filepath of the SVG is returned.'}, 'deletable': {'type': 'bool', 'default': 'True', 'description': None}}, 'postprocess': {'value': {'type': 'list[\n        numpy.ndarray\n        | PIL.Image.Image\n        | pathlib.Path\n        | str\n        | tuple[\n            numpy.ndarray\n            | PIL.Image.Image\n            | pathlib.Path\n            | str,\n            str,\n        ]\n    ]\n    | None', 'description': 'Expects the function to return a `list` of images, or `list` of (image, `str` caption) tuples. Each image can be a `str` file path, a `numpy` array, or a `PIL.Image` object.'}}, 'preprocess': {'return': {'type': 'list[tuple[str, str | None]]\n    | list[tuple[PIL.Image.Image, str | None]]\n    | list[tuple[numpy.ndarray, str | None]]\n    | None', 'description': 'Passes the list of images as a list of (image, caption) tuples, or a list of (image, None) tuples if no captions are provided (which is usually the case). The image can be a `str` file path, a `numpy` array, or a `PIL.Image` object depending on `type`.'}, 'value': None}}, 'events': {'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the ModifiableGallery. Uses event data gradio.SelectData to carry `value` referring to the label of the ModifiableGallery, and `selected` to refer to state of the ModifiableGallery. See EventData documentation on how to use this event data'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the ModifiableGallery.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the ModifiableGallery changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'delete_image': {'type': None, 'default': None, 'description': ''}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'ModifiableGallery': []}}}

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
# `gradio_modifiablegallery`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_modifiablegallery
```

## Usage

```python
from pathlib import Path

import gradio as gr
from gradio_modifiablegallery import ModifiableGallery

example = ModifiableGallery().example_value()


def delete_image(current_images, event: gr.EventData):

    image_to_delete_name = event._data

    new_images = []
    for image, caption in current_images:
        if Path(image).name != image_to_delete_name:
            new_images.append((image, caption))

    return new_images


with gr.Blocks() as demo:
    with gr.Row():
        ModifiableGallery(label="Blank")  # blank component
        gallery = ModifiableGallery(value=example, label="Populated")
        gallery.delete_image(fn=delete_image, inputs=gallery, outputs=gallery)


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `ModifiableGallery`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["ModifiableGallery"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["ModifiableGallery"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the list of images as a list of (image, caption) tuples, or a list of (image, None) tuples if no captions are provided (which is usually the case). The image can be a `str` file path, a `numpy` array, or a `PIL.Image` object depending on `type`.
- **As output:** Should return, expects the function to return a `list` of images, or `list` of (image, `str` caption) tuples. Each image can be a `str` file path, a `numpy` array, or a `PIL.Image` object.

 ```python
def predict(
    value: list[tuple[str, str | None]]
    | list[tuple[PIL.Image.Image, str | None]]
    | list[tuple[numpy.ndarray, str | None]]
    | None
) -> list[
        numpy.ndarray
        | PIL.Image.Image
        | pathlib.Path
        | str
        | tuple[
            numpy.ndarray
            | PIL.Image.Image
            | pathlib.Path
            | str,
            str,
        ]
    ]
    | None:
    return value
```
""", elem_classes=["md-custom", "ModifiableGallery-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          ModifiableGallery: [], };
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
