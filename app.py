import streamlit as st
import requests
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/to-be/donut-base-finetuned-invoices"
headers = {"Authorization": "Bearer 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"}

def query(image):
    img_byte_arr = image.convert('RGB')
    img_byte_arr.save("temp.jpg", format='JPEG')

    with open("temp.jpg", "rb") as f:
        response = requests.post(API_URL, headers=headers, files={"file": f})
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
        st.image(uploaded_image, use_column_width=True)
        if st.button("Use Uploaded Image"):
            output = query(uploaded_image)
            st.write("Extracted Text:")
            st.write(output)

if __name__ == "__main__":
    main()
