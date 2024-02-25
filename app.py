import streamlit as st
from google.cloud import vision
from googletrans import Translator

# Replace with your Google Cloud project ID
project_id = "aiboot-414616"

translator = Translator()  # Create the translator object globally

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

  # Translate the extracted text using the global translator object
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
  # Use the global translator object
  translated_text = translator.translate(text, src=source_lang, dest=target_lang)
  return translated_text.text

# App layout
st.title("Linguify")  # Set the app name

# Select translation mode
translation_mode = st.selectbox("Choose Mode", ["Image Translation", "Text Translation"])

# Image translation section
if translation_mode == "Image Translation":
  uploaded_image = st.file_uploader("Upload image of signboard:")

  # Language selection dropdowns (using the global translator object)
  source_languages = translator.get_languages()
  target_languages = translator.get_languages()

  source_lang = st.selectbox("Source Language", source_languages)
  target_lang = st.selectbox("Target Language", target_languages)

  # Translate button
  if uploaded_image is not None:
    translated_text = translate_image(uploaded_image.name, source_lang, target_lang)
    st.image(uploaded_image, caption="Uploaded Image")
    st.write(f"Translated Text: {translated_text}")

# Text translation section
elif translation_mode == "Text Translation":
  text_to_translate = st.text_area("Enter text to translate:")

  # Language selection dropdowns (using the global translator object)
  source_languages = translator.get_languages()
  target_languages = translator.get_languages()

  source_lang = st.selectbox("Source Language", source_languages)
  target_lang = st.selectbox("Target Language", target_languages)

  # Translate button
  if st.button("Translate"):
    translated_text = translate_text(text_to_translate, source_lang, target_lang)
    st.write(f"Translated Text: {translated_text}")

# ... rest of the code for layout and styling can remain ...
