# import streamlit
import streamlit as st
import os

# import image from python library
from PIL import Image

# import Gemini AI
import google.generativeai as genai

# Google Text-to-Speech(gtts) library
from gtts import gTTS

from dotenv import load_dotenv

# Configure Google  API
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')



def generate_scene_description(image):
    try:
        response = model.generate_content([
            "Describe this image in detail for a visually impaired person. Focus on the main elements, their positions, and any potential hazards or obstacles.",
            image
        ])
        return response.text
    except Exception as e:
        return f"Error generating scene description: {str(e)}"



def detect_objects(image):
    try:
        response = model.generate_content([
            "Analyze the following image and list the main objects present. "
            "For each object, provide its approximate location in the image (e.g., top-left, center, bottom-right). "
            "Also, highlight any potential obstacles or hazards for a visually impaired person.",
            image
        ])
        return response.text
    except Exception as e:
        return f"Error detecting objects: {str(e)}"



def text_to_speech(text, language):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save("output.mp3")
        return "output.mp3"
    except Exception as e:
        return f"Error converting text to speech: {str(e)}"


def main():
    st.set_page_config(page_title="AI Assistant for Visually Impaired", layout="wide")
    st.title("AI Assistant for Visually Impaired")

    features = [
        "Real-Time Scene Understanding",
        "Object and Obstacle Detection",
        "Text-to-Speech Conversion",
    ]

    selected_feature = st.sidebar.radio("Select a feature:", features)

    if selected_feature in ["Real-Time Scene Understanding", "Object and Obstacle Detection"]:
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_container_width=True)

            if selected_feature == "Real-Time Scene Understanding":
                scene_description = generate_scene_description(image)
                st.subheader("Scene Description")
                st.write(scene_description)
                
                if st.button("Convert Description to Speech"):
                    audio_file = text_to_speech(scene_description, "en")
                    st.audio(audio_file, format='audio/mp3')

            elif selected_feature == "Object and Obstacle Detection":
                objects_detected = detect_objects(image)
                st.subheader("Objects Detected")
                st.write(objects_detected)
                
                if st.button("Convert Object Detection to Speech"):
                    audio_file = text_to_speech(objects_detected, "en")
                    st.audio(audio_file, format='audio/mp3')

    elif selected_feature == "Text-to-Speech Conversion":
        st.subheader("Text-to-Speech Conversion")
        text_input = st.text_area("Enter text to convert to speech:")
        language = st.selectbox("Select language:", ["en", "es", "fr", "de", "it"])
        
        if st.button("Convert to Speech"):
            if text_input:
                audio_file = text_to_speech(text_input, language)
                st.audio(audio_file, format='audio/mp3')
                st.download_button(label="Download Audio", data=open(audio_file, "rb"), file_name="speech.mp3", mime="audio/mp3")
            else:
                st.warning("Please enter some text to convert.")

if __name__ == "__main__":
    main()