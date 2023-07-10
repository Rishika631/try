import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import moviepy.editor as mp
import os

# Set Streamlit page configuration
st.set_page_config(page_title="YouTube Video Summarizer and Insights")

# Function to extract transcript from YouTube video
def extract_transcript(youtube_video):
    video_id = youtube_video.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    transcript_text = ""
    for segment in transcript:
        transcript_text += segment['text'] + " "

    return transcript_text

# Function to summarize transcript
def summarize_transcript(transcript):
    # Split transcript into chunks of 1000 characters (for T5 model limitation)
    chunks = [transcript[i:i+1000] for i in range(0, len(transcript), 1000)]

    # Initialize summarization model
    summarizer = pipeline('summarization')

    # Summarize each chunk and combine the summaries
    summarized_text = []
    for chunk in chunks:
        out = summarizer(chunk)
        out = out[0]['summary_text']
        summarized_text.append(out)

    return summarized_text

# Function to extract key points from the video using moviepy
def extract_key_points(video_path):
    clip = mp.VideoFileClip(video_path)
    duration = clip.duration
    key_frames = []
    key_points = []

    # Extract key frames at desired intervals
    for i in range(10):
        time = duration * i / 10
        frame = clip.get_frame(time)
        key_frames.append(frame)
        key_points.append(f"Key Point {i+1}")

    return key_frames, key_points

# Function to extract action insights from transcript
def extract_action_insights(transcript):
    # Placeholder logic - Extract sentences containing action-oriented keywords
    keywords = ["do", "perform", "execute", "implement", "take action"]
    insights = []

    # Split transcript into sentences
    sentences = transcript.split(".")
    
    for sentence in sentences:
        sentence = sentence.strip()
        for keyword in keywords:
            if keyword in sentence:
                insights.append(sentence)
                break
    
    return insights

# Function to perform chatbot interaction
def chatbot_interaction(transcript, question):
    # Placeholder logic - Simple matching based on keywords in transcript and question
    keywords = ["how", "what", "why"]
    response = "I'm sorry, I don't have an answer for that question."

    # Check if question keywords are present in the transcript
    for keyword in keywords:
        if keyword in transcript.lower() and keyword in question.lower():
            response = "The answer to your question can be found in the video."
            break

    return response



# Streamlit app
def main():
    st.header("YouTube Video Summarizer and Insights")

    # Option to upload local file or enter YouTube video URL
    option = st.selectbox("Choose an option:", ["YouTube Video", "Local File"])

    if option == "YouTube Video":
        # Get YouTube video URL from user
        youtube_video = st.text_input("Enter the YouTube video URL:")

        if youtube_video:
            # Extract transcript from YouTube video
            transcript = extract_transcript(youtube_video)

            # Summarize transcript
            summary = summarize_transcript(transcript)

            st.info("Transcript processed successfully!")

            # Display options
            options = st.sidebar.multiselect("Select Options:", ["Summarization", "Key Points"])

            # Summarization
            if "Summarization" in options:
                st.subheader("Transcript Summary")
                st.text('\n'.join(summary))

            # Key Points
            if "Key Points" in options:
                st.subheader("Key Points")
                key_frames, key_points = extract_key_points(youtube_video)
                for idx, key_frame in enumerate(key_frames):
                    image_filename = f"key_frame_{idx}.png"
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(key_points[idx])
                    # Save key frame as PNG image
                    key_frame.save(image_filename)

    elif option == "Local File":
        # File upload feature
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

        if uploaded_file:
            # Save the uploaded file
            video_path = "uploaded_video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract transcript from video
            transcript = ""  # Placeholder, replace with your logic to extract transcript from the local video

            # Summarize transcript
            summary = summarize_transcript(transcript)

            st.info("Transcript processed successfully!")

            # Display options
            options = st.sidebar.multiselect("Select Options:", ["Summarization", "Key Points"])

            # Summarization
            if "Summarization" in options:
                st.subheader("Transcript Summary")
                st.text('\n'.join(summary))

            # Key Points
            if "Key Points" in options:
                st.subheader("Key Points")
                key_frames, key_points = extract_key_points(video_path)
                for idx, key_frame in enumerate(key_frames):
                    image_filename = f"key_frame_{idx}.png"
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(key_points[idx])
                    # Save key frame as PNG image
                    key_frame.save(image_filename)

            # Delete the uploaded video file
            os.remove(video_path)

if __name__ == "__main__":
    main()
