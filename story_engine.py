# Load API key from .env
from dotenv import load_dotenv
load_dotenv()

import os
from groq import Groq

# ✅ Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_story(genre, theme, characters, style="normal", use_emojis=False):
    """
    Generate a creative story based on the given genre, theme, style, and characters using Groq LLM.
    """
    emoji_instruction = "Include appropriate emojis throughout the story to enhance emotional and visual appeal. 😊📚✨" if use_emojis else ""
    style_instruction = f"Make the story {style.lower()} in tone." if style.lower() != "normal" else ""

    prompt = (
        f"You are a professional storyteller.\n"
        f"Write a detailed and engaging story based on the following details:\n\n"
        f"Genre: {genre}\n"
        f"Theme: {theme}\n"
        f"Main Characters: {characters}\n\n"
        f"{style_instruction}{emoji_instruction}"
        f"Make the story engaging, imaginative, well-structured, and suitable for a wide audience.\n"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # You can change this to a model Groq supports
            messages=[
                {"role": "system", "content": "You are a creative story writer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.9,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error generating story:\n\n{e}"
