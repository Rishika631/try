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

    st.subheader("Selected Image:")

    image = Image.open(selected_image)
    st.image(image, use_column_width=True)

    if st.button("Use this Image"):
        with open(selected_image, "rb") as f:
            image_bytes = f.read()
        output = query(image_bytes)
        st.write("Extracted Text:")
        st.write(output)

if __name__ == "__main__":
    main()
