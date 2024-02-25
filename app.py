import streamlit as st
from google.cloud import vision
from googletrans import Translator
from google.cloud import dialogflow_v2beta1 as DialogflowV2Client

# Set the Google Cloud project ID


# Replace with your Google Cloud project ID
project_id = "aiboot-414616"

# Function to translate image text using Cloud Vision
def translate_image(image, source_lang, target_lang):
  """
  Extracts text from image using Cloud Vision and translates it.

  Args:
      image: The image to translate text from.
      source_lang: The source language code (e.g., 'en').
      target_lang: The target language code (e.g., 'es').

  Returns:
      The translated text.
  """
  # Create a Vision client object
  client = vision.ImageAnnotatorClient()

  # Read the image data
  with open(image, 'rb') as image_file:
    content = image_file.read()

  # Prepare the image request
  image = vision.Image(content=content)

  # Extract text using document text detection
  response = client.text_detection(image=image)
  full_text = response.full_text_annotation.text

  # Translate the extracted text
  translator = Translator()
  translated_text = translator.translate(full_text, src=source_lang, dest=target_lang)
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
def dialogflow_chat(text, language_code):
  """
  Sends user query to Dialogflow agent and returns the response.

  Args:
      text: The user's query.
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
st.set_page_config(page_title="Linguify", page_icon=":globe:")  # Set app name and icon

# ... rest of the code remains the same ...

 


 
