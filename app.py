import streamlit as st
from google.cloud import translate_v2 as translate

# Replace with your Google Cloud project ID
project_id = "your_project_id"

# Create a translation client
client = translate.Client(project=project_id)

# Function to translate text
def translate_text(text, source_lang, target_lang):
  """
  Translates text from source language to target language using Google Cloud Translation API.

  Args:
      text: The text to translate.
      source_lang: The source language code (e.g., 'en').
      target_lang: The target language code (e.g., 'es').

  Returns:
      The translated text.
  """
  # Translate the text
  translation = client.translate(
      input_=translate.TranslateText(text=text, language=source_lang),
      target_language=target_lang,
  )

  # Return the translated text
  return translation.text

# App layout
st.title("Linguify")  # Set the app name

# Select translation mode
translation_mode = st.selectbox("Choose Mode", ["Text Translation"])

# Text translation section
if translation_mode == "Text Translation":
  text_to_translate = st.text_area("Enter text to translate:")

  # Language selection dropdowns
  # Use the Google Cloud Translation API to retrieve language codes
  languages = client.get_languages()
  source_languages = [lang["code"] for lang in languages]
  target_languages = source_languages

  source_lang = st.selectbox("Source Language", source_languages)
  target_lang = st.selectbox("Target Language", target_languages)

  # Translate button
  if st.button("Translate"):
    translated_text = translate_text(text_to_translate, source_lang, target_lang)
    st.write(f"Translated Text: {translated_text}")

# ... rest of the code for layout and styling can remain ...
