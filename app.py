
import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import moviepy.editor as mp
import os

# Set OpenAI API credentials
openai.api_key = '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'

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

# Function to summarize transcript using OpenAI's text summarization model
def summarize_transcript(transcript):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=transcript,
        max_tokens=200,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text.strip()
    return summary

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
    # Define the action-oriented keywords
    keywords = ["do", "perform", "execute", "implement", "take action"]
    insights = []

    # Generate action insights using OpenAI's GPT-3 model
    response = openai.Completion.create(
        engine="davinci",
        prompt=transcript,
        max_tokens=100,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n = 5
    )
    answer = response.choices[0].text.strip()

    # Process the answer and extract relevant insights
    sentences = answer.split(".")
    for sentence in sentences:
        sentence = sentence.strip()
        for keyword in keywords:
            if keyword in sentence:
                insights.append(sentence)
                break

    return insights

# Function to perform chatbot interaction
def chatbot_interaction(transcript, question):
    # Use LangChain API or any other OpenAI model API for chatbot
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Transcript: {transcript}\nQuestion: {question}",
        max_tokens=75,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    answer = response.choices[0].text.strip()

    if answer:
        return answer
    else:
        return "I'm sorry, I don't have an answer for that question."

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
            options = st.sidebar.multiselect("Select Options:", ["Summarization", "Key Points", "Action Insights", "Chatbot"])

            # Summarization
            if "Summarization" in options:
                st.subheader("Transcript Summary")
                st.text(summary)

            # Key Points
            if "Key Points" in options:
                st.subheader("Key Points")
                key_frames, key_points = extract_key_points(youtube_video)
                for idx, key_frame in enumerate(key_frames):
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(key_points[idx])

            # Action Insights
            if "Action Insights" in options:
                st.subheader("Action Insights")
                insights = extract_action_insights(transcript)
                for insight in insights:
                    st.write(insight)

            # Chatbot
            if "Chatbot" in options:
                st.subheader("Chatbot")
                user_question = st.text_input("Ask a question:")
                if user_question:
                    response = chatbot_interaction(transcript, user_question)
                    st.write(response)

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
            options = st.sidebar.multiselect("Select Options:", ["Summarization", "Key Points", "Action Insights", "Chatbot"])

            # Summarization
            if "Summarization" in options:
                st.subheader("Transcript Summary")
                st.text(summary)

            # Key Points
            if "Key Points" in options:
                st.subheader("Key Points")
                key_frames, key_points = extract_key_points(video_path)
                for idx, key_frame in enumerate(key_frames):
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(key_points[idx])

            # Action Insights
            if "Action Insights" in options:
                st.subheader("Action Insights")
                insights = extract_action_insights(transcript)
                for insight in insights:
                    st.write(insight)

            # Chatbot
            if "Chatbot" in options:
                st.subheader("Chatbot")
                user_question = st.text_input("Ask a question:")
                if user_question:
                    response = chatbot_interaction(transcript, user_question)
                    st.write(response)

            # Delete the uploaded video file
            os.remove(video_path)

if __name__ == "__main__":
    main()

