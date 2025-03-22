import streamlit as st 
import google.generativeai as genai
import requests

api_key = "AIzaSyAPnCL9l44PiY8fJscAyhjPgysR2HpIH3w"
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

def generate_design_idea(style, size, rooms):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )
    context = f"create a custom home design plan with the following details: \nstyle: {style}\nSize: {size}\nRooms: {rooms}"
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    context
                ],
            },
        ]
    )

    response = chat_session.send_message(context)
    text = response.candidates[0].content.parts[0].text if response.candidates and response.candidates[0].content.parts else "No response generated"
    return text


def fetch_image_from_lexica(style):
    lexica_url = f"https://lexica.art/api/v1/search?q={style}"
    try:
        response = requests.get(lexica_url)
        response.raise_for_status()
        data = response.json()
        if data['images']:
            return data['images'][0]['src'] # Return the first image URL
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from Lexica: {e}")
        return None
    except (ValueError, KeyError) as e:
        print(f"Error processing Lexica response: {e}")
        return None
st.title("Custom Home Design Assistant")
# Textboxes for style, size, and number of rooms input
style = st.text_input("Enter the home design style (e.g., Modern, Rustic)")
size = st.text_input("Enter the size of the home (e.g., 2000 sq ft)")
rooms = st.text_input("Enter the number of rooms")
if st.button("Generate Design"):
    if style and size and rooms:
        design_idea = generate_design_idea(style, size, rooms)
        image_url = fetch_image_from_lexica(style)
        st.markdown("### Custom Home Design Idea")
        st.markdown(design_idea)
        if image_url:
            st.image(image_url, caption="Design inspiration from Lexica.art")
        else:
            st.warning("No relevant images found on Lexica.art.")
    else:
        st.warning("Please fill in all the fields.")
