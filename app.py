import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/to-be/donut-base-finetuned-invoices"
headers = {"Authorization": "Bearer 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"}

def query(file):
    response = requests.post(API_URL, headers=headers, data=file)
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
    for image_url in sample_images:
        col = st.columns(2)
        with col[0]:
            image = st.image(image_url, use_column_width=True)
            if image.button("Use this Image"):
                output = query(requests.get(image_url).content)
                st.write("Extracted Text:")
                st.write(output)

    if uploaded_file is not None:
        output = query(uploaded_file.read())
        st.write("Extracted Text:")
        st.write(output)

if __name__ == "__main__":
    main()
