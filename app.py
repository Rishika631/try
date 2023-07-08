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

    selected_image = st.sidebar.selectbox("Select Sample Image", sample_images)
    selected_index = sample_images.index(selected_image)

    st.subheader("Select a Sample Image:")

    images_col = st.columns(3)

    for index, image_path in enumerate(sample_images):
        image = Image.open(image_path)

        # Resize the image to fit within a column
        max_image_width = int(st.columns(3)[0].width / 3)
        image.thumbnail((max_image_width, max_image_width))

        images_col[index].image(image, use_column_width=True)

        if st.button(f"Use Image {index+1}", key=f"use_image_{index+1}"):
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            output = query(image_bytes)
            st.write("Extracted Text:")
            st.write(output)

if __name__ == "__main__":
    main()
