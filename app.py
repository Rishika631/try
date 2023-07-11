import spacy
import re
import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import moviepy.editor as mp
import os
from transformers import pipeline
from urllib.parse import urlparse, parse_qs

# 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 -new api key - kartik

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



# Function to summarize transcript using OpenAI's text Meeting Summary model
def summarize_transcript(transcript):
    prompt = "Extract summary from the following transcript in 100 words:\n\n" + transcript
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text.strip()
    return summary


# Function to extract Image Summary from the video using moviepy
def extract_image_summary(video_path):
    clip = mp.VideoFileClip(video_path)
    duration = clip.duration
    key_frames = []
    image_summary = []

    # Extract key frames at desired intervals
    for i in range(10):
        time = duration * i / 10
        frame = clip.get_frame(time)
        key_frames.append(frame)
        image_summary.append(f"Key Point {i+1}")

    return key_frames, image_summary

# Function to extract action insights & Key Points from transcript 
def extract_action_insights(transcript):
    prompt = "Extract action insights and key points both from the following transcript:\n\n" + transcript
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    insights = response.choices[0].text.strip().split("\n")
    return insights


def analyze_sentiment(transcript):
    sentiment_analyzer = pipeline("sentiment-analysis")
    results = sentiment_analyzer(transcript)

    sentiments = [result["label"] for result in results]
    return sentiments

# Function to extract a given task 

def extract_task_from_transcript(transcript, task):
    prompt = f"{task} from the following transcript and mention to whome the task is given:\n\n{transcript}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    tasks = response.choices[0].text.strip().split("\n")
    return tasks



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

            st.info("Meeting processed successfully!")

            # Display options
            options = st.sidebar.multiselect("Select Options:", ["Meeting Summary", "Image Summary", "Action Insights & Key Points", "Sentiment Analysis", "Given Task", "Chatbot"])

            # Meeting Summary
            if "Meeting Summary" in options:
                st.subheader("Meeting Summary")
                st.text(summary)

            # Image Summary
            if "Image Summary" in options:
                st.subheader("Image Summary")
                key_frames, image_summary = extract_image_summary(youtube_video)
                for idx, key_frame in enumerate(key_frames):
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(image_summary[idx])

            # Action Insights & Key Points
            if "Action Insights & Key Points" in options:
                st.subheader("Action Insights & Key Points")
                insights = extract_action_insights(transcript)
                for insight in insights:
                    st.write(insight)

             #  Sentiment Analysis
            if "Sentiment Analysis" in options:
                st.subheader("Sentiment Analysis")
                sentiment_results = analyze_sentiment(transcript)
                for idx, sentiment in enumerate(sentiment_results):
                    st.write(f"Sentiment {idx+1}: {sentiment}")

            # Given Task
            if "Given Task" in options:
                st.subheader("Given Task")
                tasks = extract_task_from_transcript(transcript, "Extract task")
                for task in tasks:
                    st.write(task)
            
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
            options = st.sidebar.multiselect("Select Options:", ["Meeting Summary", "Image Summary", "Action Insights & Key Points", "Sentiment Analysis", "Given Task", "Chatbot"])

            # Meeting Summary
            if "Meeting Summary" in options:
                st.subheader("Meeting Summary")
                st.text(summary)

            # Image Summary
            if "Image Summary" in options:
                st.subheader("Image Summary")
                key_frames, image_summary = extract_image_summary(video_path)
                for idx, key_frame in enumerate(key_frames):
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(image_summary[idx])

            # Action Insights & Key Points
            if "Action Insights & Key Points" in options:
                st.subheader("Action Insights & Key Points")
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

           #  Sentiment Analysis
            if "Sentiment Analysis" in options:
                st.subheader("Sentiment Analysis")
                sentiment_results = analyze_sentiment(transcript)
                for idx, sentiment in enumerate(sentiment_results):
                    st.write(f"Sentiment {idx+1}: {sentiment}")

           # Given Task
            if "Given Task" in options:
                st.subheader("Given Task")
                tasks = extract_task_from_transcript(transcript, "Extract task")
                for task in tasks:
                    st.write(task)
         

            # Delete the uploaded video file
            os.remove(video_path)

if __name__ == "__main__":
    main()
