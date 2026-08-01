import streamlit as st
import speech_recognition as sr
from google import genai
from dotenv import load_dotenv
import pyttsx3
import os


# ---------------------------
# Load API Key
# ---------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key=API_KEY
)



# ---------------------------
# Streamlit Config
# ---------------------------

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Voice Assistant")

st.write(
    "Speak with AI using your voice"
)



# ---------------------------
# Language & Voice
# ---------------------------


language = st.selectbox(

    "🌐 Choose Language",

    [
        "English",
        "Hindi",
        "Spanish",
        "French"
    ]

)



voice_choice = st.selectbox(

    "🎙️ Choose Voice",

    [
        "Male",
        "Female"
    ]

)



language_map = {


    "English":
    "Answer in English",


    "Hindi":
    "Answer in Hindi",


    "Spanish":
    "Answer in Spanish",


    "French":
    "Answer in French"

}





# ---------------------------
# Memory
# ---------------------------


if "history" not in st.session_state:

    st.session_state.history = []


if "ai_response" not in st.session_state:

    st.session_state.ai_response = ""



if "speaking" not in st.session_state:

    st.session_state.speaking = False






# ---------------------------
# Speech To Text
# ---------------------------


def listen_voice():

    recognizer = sr.Recognizer()


    try:

        with sr.Microphone() as source:


            st.info(
                "🎤 Listening..."
            )


            recognizer.adjust_for_ambient_noise(
                source
            )


            audio = recognizer.listen(
                source,
                timeout=5
            )


        text = recognizer.recognize_google(
            audio
        )


        return text



    except Exception as e:

        st.error(
            f"Voice Error: {e}"
        )


        return None







# ---------------------------
# Gemini
# ---------------------------


def ask_ai(question):


    try:


        response = client.models.generate_content(


            model="gemini-2.5-flash",


            contents=f"""


            You are a helpful AI voice assistant.


            {language_map[language]}


            User:

            {question}

            """


        )


        return response.text



    except Exception as e:


        return f"AI Error: {e}"







# ---------------------------
# AI Voice
# ---------------------------


def start_voice(text):


    try:


        engine = pyttsx3.init()


        voices = engine.getProperty(
            "voices"
        )



        if voice_choice == "Female":


            engine.setProperty(

                "voice",

                voices[1].id

            )


        else:


            engine.setProperty(

                "voice",

                voices[0].id

            )



        engine.setProperty(
            "rate",
            150
        )



        engine.say(
            text
        )


        engine.runAndWait()



    except Exception as e:


        st.error(
            f"Voice error: {e}"
        )






# ---------------------------
# Stop Voice
# ---------------------------


def stop_voice():


    try:


        engine = pyttsx3.init()

        engine.stop()


        st.session_state.speaking = False



    except Exception as e:


        st.error(e)







# ---------------------------
# Start Speaking Button
# ---------------------------


if st.button(
    "🎤 Start Speaking"
):


    user_text = listen_voice()



    if user_text:


        st.subheader(
            "You said:"
        )


        st.write(
            user_text
        )



        answer = ask_ai(
            user_text
        )



        st.session_state.ai_response = answer



        st.subheader(
            "🤖 AI Response"
        )


        st.write(
            answer
        )



        st.session_state.history.append(

            {
                "user":user_text,

                "ai":answer
            }

        )







# ---------------------------
# Voice Controls
# ---------------------------


st.subheader(
    "🔊 AI Voice Control"
)



col1, col2 = st.columns(2)



with col1:


    if st.button(
        "▶ Start AI Voice"
    ):


        if st.session_state.ai_response:


            start_voice(
                st.session_state.ai_response
            )


        else:


            st.warning(
                "Generate AI response first"
            )





with col2:


    if st.button(
        "⛔ Close Voice"
    ):


        stop_voice()


        st.success(
            "Voice stopped"
        )







# ---------------------------
# Text Chat
# ---------------------------


text = st.text_input(
    "Or type your message"
)



if st.button(
    "Send"
):


    if text:


        answer = ask_ai(
            text
        )


        st.session_state.ai_response = answer



        st.write(
            answer
        )



        st.session_state.history.append(

            {

            "user":text,

            "ai":answer

            }

        )







# ---------------------------
# History
# ---------------------------


st.subheader(
    "🕘 Conversation History"
)



for chat in st.session_state.history:


    with st.expander(
        chat["user"]
    ):


        st.write(
            "You:"
        )


        st.write(
            chat["user"]
        )


        st.write(
            "AI:"
        )


        st.write(
            chat["ai"]
        )