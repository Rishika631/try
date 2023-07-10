import streamlit as st
from pytube import YouTube
from PIL import Image
import imageio

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

# Extract key frames from the video using pytube3 and imageio
def extract_key_frames(youtube_link):
    yt = YouTube(youtube_link)
    video = yt.streams.get_highest_resolution()
    video_path = video.download()
    key_frames = []

    # Read key frames using imageio
    reader = imageio.get_reader(video_path)
    for idx, frame in enumerate(reader):
        # Extract key frames at desired intervals
        if idx % 60 == 0:
            key_frames.append(frame)

    return key_frames

# Display the key frames as an image summary
def display_summary(key_frames):
    st.subheader("Video Image Summary")
    if key_frames:
        for idx, key_frame in enumerate(key_frames):
            image = Image.fromarray(key_frame)
            st.image(image, caption=f"Key Frame {idx+1}")
    else:
        st.warning("No key frames found in the video")

# Run the Streamlit app
if __name__ == "__main__":
    main()
