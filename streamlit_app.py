from openai import OpenAI
import streamlit as st
from youtube import FetchTranscript

def get_transcript(url):
    """Fetches the transcript for a given YouTube video URL."""
    try:
        fetch_transcript = FetchTranscript(url=url)
        text = fetch_transcript.get_text()
        return text
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    youtube_url = st.text_input("YouTube URL", key="youtube_url")
    "Enter Youtube URL"

st.title("💬 YouTube Insights")
st.caption("🚀 Ask me about the YT Video")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Initialize session state for transcript and last used URL
if "transcript" not in st.session_state:
    st.session_state.transcript = None  # Store transcript

if "last_youtube_url" not in st.session_state:
    st.session_state.last_youtube_url = None  # Store last processed URL

# If youtube_url is changed, fetch a new transcript with a loading spinner
if youtube_url and youtube_url != st.session_state.last_youtube_url:
    with st.spinner("Analysing Video... Please wait."):
        st.session_state.transcript = get_transcript(youtube_url)  # Fetch transcript
        st.session_state.last_youtube_url = youtube_url  # Update last used URL

    if st.session_state.transcript:
        st.success("Analysed Video successfully!")

if "transcript" in st.session_state:
    content = f"""
                You are an advanced AI assistant designed to provide detailed and accurate answers based on the YouTube video transcript provided by the user.

                ### Context:
                The user is watching a YouTube video and wants to understand it better. They have provided the exact transcript of the video. Your task is to analyze this transcript and answer the user's questions with clear, accurate, and detailed explanations, strictly based on the given transcript.

                ### Instructions:
                1. **Context-Driven Responses Only**
                - Your responses must be strictly based on the provided transcript.
                - Do not use word transcript.
                - Do NOT add external knowledge, assumptions, or opinions.
                - If use greets you You should only greet them back. Don't say like this : 'How can I assist you today based on the information from the video transcript?'
                - Do Not mention that you are telling user based on the transcript. 
                - If the answer is not found in the transcript, politely state that you do not have enough information.

                2. **Detailed and Clear Explanations**
                - Provide comprehensive answers that explain concepts in depth.
                - Break down complex topics step by step if necessary.
                - Use examples or references from the transcript when relevant.

                3. **Maintain Accuracy & Relevance**
                - Do not speculate or infer beyond what is stated in the transcript.
                - Ensure responses are well-structured, clear, and relevant to the user's query.

                4. **Politeness & User Experience**
                - If the answer is unavailable in the transcript, respond politely (e.g., "Based on the provided transcript, this information is not mentioned.").
                - Offer to assist with any other related queries the user may have.

                ### Provided Transcript:
                {st.session_state.transcript}

                Answer all user questions strictly based on this transcript.
                """
    st.session_state["messages"] = [{"role": "system", "content": content}]

# if st.session_state.transcript:
#     st.write("### Transcript Preview:")
#     st.write(st.session_state.messages)

for msg in st.session_state.messages:
    if msg['role'] != 'system':
        st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if not youtube_url:
        st.info("Please enter youtube url.")
        st.stop()
    
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)