import spacy
import re
import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import moviepy.editor as mp
import os
from transformers import pipeline
from urllib.parse import urlparse, parse_qs

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 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 -new api key - kartik
# 132899854032-jb5gpnuh5fbllo8d08mb1dpqeilafkku.apps.googleusercontent.com (Client ID- g calander-kartik)
# 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  (Client secret  g calander-kartik) 
# list down  all the taks given from the following transcript and mention to whome the task was given :


# Set OpenAI API credentials
openai.api_key = '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'

# Set Streamlit page configuration
st.set_page_config(page_title="YouTube Video Summarizer and Insights")

# Define the necessary constant for the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

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
    
    
# Function to authenticate with Google Calendar API
def authenticate_google_calendar():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES, redirect_uri='http://localhost:8501/callback')
            auth_url, _ = flow.authorization_url()
            st.write(f"Please authorize the app by clicking the following link:\n[Authorize]({auth_url})")
            if 'code' not in st.session_state:
                st.stop()
            else:
                flow.fetch_token(authorization_response=request.url)
                creds = flow.credentials
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                return creds
    return creds



# Function to create a Google Calendar event
def create_google_calendar_event(service, summary, start_time, end_time, location, description):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',  # Replace with your desired timezone
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',  # Replace with your desired timezone
        },
        'location': location,
        'description': description,
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event['id']

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
            
            # Authenticate with Google Calendar API
            creds = authenticate_google_calendar()
            service = build('calendar', 'v3', credentials=creds)

            # Create the event on Google Calendar
            event_id = create_google_calendar_event(service, 'Meeting Summary', '2023-07-15T09:00:00',
                                                   '2023-07-15T10:00:00', 'Event Location', summary)

            st.success("Event created on Google Calendar!")

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

            # Authenticate with Google Calendar API
            creds = authenticate_google_calendar()
            service = build('calendar', 'v3', credentials=creds)

            # Create the event on Google Calendar
            event_id = create_google_calendar_event(service, 'Meeting Summary', '2023-07-15T09:00:00',
                                                   '2023-07-15T10:00:00', 'Event Location', summary)

            st.success("Event created on Google Calendar!")

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
