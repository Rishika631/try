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
    for index, image_path in enumerate(sample_images):
        col = st.columns(2)
        with col[0]:
            image = Image.open(image_path)
            st.image(image, use_column_width=True)
            if st.button(f"Use Image {index+1}", key=f"use_image_{index}"):
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                output = query(image_bytes)
                st.write("Extracted Text:")
                st.write(output)

    

if __name__ == "__main__":
    main()
