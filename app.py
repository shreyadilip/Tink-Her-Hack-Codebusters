import streamlit as st
import pytesseract
from PIL import Image
from googletrans import Translator
from dialogflow import DialogflowV2Client

# Set Tesseract path (adjust based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to translate image text
def translate_image(image, source_lang, target_lang):
  """
  Extracts text from image, translates it, and returns the translated text.

  Args:
      image: The image to translate text from.
      source_lang: The source language code (e.g., 'en').
      target_lang: The target language code (e.g., 'es').

  Returns:
      The translated text.
  """
  text = pytesseract.image_to_string(image)
  translator = Translator()
  translated_text = translator.translate(text, src=source_lang, dest=target_lang)
  return translated_text.text

# Function to translate text
def translate_text(text, source_lang, target_lang):
  """
  Translates text from source language to target language.

  Args:
      text: The text to translate.
      source_lang: The source language code (e.g., 'en').
      target_lang: The target language code (e.g., 'es').

  Returns:
      The translated text.
  """
  translator = Translator()
  translated_text = translator.translate(text, src=source_lang, dest=target_lang)
  return translated_text.text

# Function to interact with Dialogflow chatbot
def dialogflow_chat(text, project_id, language_code):
  """
  Sends user query to Dialogflow agent and returns the response.

  Args:
      text: The user's query.
      project_id: Your Dialogflow project ID.
      language_code: The language code for the conversation (e.g., 'en').

  Returns:
      The chatbot's response.
  """
  dialogflow_session = DialogflowV2Client.SessionsClient()
  session = dialogflow_session.session_path(project_id, st.session_state.get('session_id', '12345'))
  text_input = dialogflow_session.text_input(text=text, language_code=language_code)
  query_input = dialogflow_session.query_input(session=session, input_=text_input)
  try:
    response = dialogflow_session.detect_intent(request=query_input)
    return response.query_result.fulfillment_text
  except Exception as e:
    return f"Error: {e}"

# App layout
st.title("Multi-lingual Translator & Chatbot")

# Select translation mode
translation_mode = st.selectbox("Choose Mode", ["Image Translation", "Text Translation"])

# Image translation section
if translation_mode == "Image Translation":
  uploaded_image = st.file_uploader("Upload image of signboard:")

  # Language selection dropdowns
  source_languages = translator.get_languages()
  target_languages = translator.get_languages()

  source_lang = st.selectbox("Source Language", source_languages)
  target_lang = st.selectbox("Target Language", target_languages)

  # Translate button
  if uploaded_image is not None:
    image = Image.open(uploaded_image)
    translated_text = translate_image(image, source_lang, target_lang)
    st.image(image, caption="Uploaded Image")
    st.write(f"Translated Text: {translated_text}")

# Text translation section
elif translation_mode == "Text Translation":
  text_to_translate = st.text_area("Enter text to translate:")

  # Language selection dropdowns
  source_languages = translator.get_languages()
  target_languages = translator.get_languages()

  source_lang = st.selectbox("Source Language", source_languages)
  target_lang = st.selectbox("Target Language", target_languages)

  # Translate button
  if text_to_translate:
    translated_text = translate
