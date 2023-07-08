import streamlit as st
import requests
from PIL import Image
import io

API_URL = "https://api-inference.huggingface.co/models/to-be/donut-base-finetuned-invoices"
headers = {"Authorization": "Bearer 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"}

def query(image_bytes):
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.text

def main():
    st.title("Documented Form Text Extraction")
    st.write("Upload an image of a handwritten form to extract the text.")

    sample_images = [
        "image.jpg",
        "image2.jpg",
        "image3.jpg"
    ]

    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        output = query(image_bytes)
        st.write("Extracted Text:")
        st.write(output)

    st.subheader("Select a Sample Image:")

    row_images = []
    for index, image_path in enumerate(sample_images):
        image = Image.open(image_path)
        row_images.append(image)

        if len(row_images) == 3:
            st.image(row_images, use_column_width=True)

            # Add padding between images using st.sidebar container
            with st.sidebar:
                st.text("")  # Add empty text to create space

            buttons_col1, buttons_col2, buttons_col3 = st.columns(3)

            if buttons_col1.button(f"Use Image {index-1}", key=f"use_image_{index-1}"):
                with open(sample_images[index-1], "rb") as f:
                    image_bytes = f.read()
                output = query(image_bytes)
                st.write("Extracted Text:")
                st.write(output)

            if buttons_col2.button(f"Use Image {index}", key=f"use_image_{index}"):
                with open(sample_images[index], "rb") as f:
                    image_bytes = f.read()
                output = query(image_bytes)
                st.write("Extracted Text:")
                st.write(output)

            if buttons_col3.button(f"Use Image {index+1}", key=f"use_image_{index+1}"):
                with open(sample_images[index+1], "rb") as f:
                    image_bytes = f.read()
                output = query(image_bytes)
                st.write("Extracted Text:")
                st.write(output)

            row_images = []

    # If there are remaining images not displayed in a row
    if row_images:
        st.image(row_images, use_column_width=True)

        # Add padding between images using st.sidebar container
        with st.sidebar:
            st.text("")  # Add empty text to create space

        buttons_col = st.columns(len(row_images))

        for index, image_path in enumerate(sample_images[-len(row_images):]):
            if buttons_col[index].button(f"Use Image {index+1}", key=f"use_image_{index+1}"):
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                output = query(image_bytes)
                st.write("Extracted Text:")
                st.write(output)

if __name__ == "__main__":
    main()
