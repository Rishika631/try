import cv2
import streamlit as st
import numpy as np
import pafy
from PIL import Image

# Streamlit app
def main():
    st.title("YouTube Video Image Summary")

    # Get YouTube link from user
    youtube_link = st.text_input("Enter YouTube video link")

    # Generate summary button
    if st.button("Generate Summary"):
        if youtube_link:
            try:
                # Extract key frames from the video
                key_frames = extract_key_frames(youtube_link)

                # Display the key frames as an image summary
                display_summary(key_frames)
            except Exception as e:
                st.error("An error occurred: " + str(e))
        else:
            st.warning("Please enter a YouTube video link")

# Extract key frames from the video using OpenCV
def extract_key_frames(youtube_link):
    video = pafy.new(youtube_link)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)

    key_frames = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 60 == 0:  # Change key frame interval as desired
            key_frames.append(frame)
        frame_count += 1

    cap.release()
    return key_frames

# Display the key frames as an image summary
def display_summary(key_frames):
    st.subheader("Video Image Summary")
    if key_frames:
        for key_frame in key_frames:
            image = Image.fromarray(key_frame)
            st.image(image, caption="Key Frame")
    else:
        st.warning("No key frames found in the video")

# Run the Streamlit app
if __name__ == "__main__":
    main()
