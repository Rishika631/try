import streamlit as st
import requests
from PIL import Image
import io
import base64

API_URL = "https://api-inference.huggingface.co/models/to-be/donut-base-finetuned-invoices"
headers = {"Authorization": "Bearer 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"}

def image_to_base64(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')
    return encoded_image

def query(image):
    encoded_image = image_to_base64(image)
    data = {
        'file': encoded_image
    }
    response = requests.post(API_URL, headers=headers, json=data)
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

    st.subheader("Select a Sample Image:")
    for index, image_path in enumerate(sample_images):
        col = st.columns(2)
        with col[0]:
            image = Image.open(image_path)
            st.image(image, use_column_width=True)
            if st.button(f"Use Image {index+1}", key=f"use_image_{index}"):
                output = query(image)
                st.write("Extracted Text:")
                st.write(output)

    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file)
        output = query(uploaded_image)
        st.write("Extracted Text:")
        st.write(output)

if __name__ == "__main__":
    main()
