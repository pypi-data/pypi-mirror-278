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
