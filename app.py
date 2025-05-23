from story_engine import generate_story
import streamlit as st
import tempfile
import datetime
import requests

from dotenv import load_dotenv
load_dotenv()
import os

# Replace this with your Google Apps Script webhook URL
GOOGLE_SHEET_WEBHOOK_URL = os.getenv("G_URL")

# Page configuration with enhanced styling
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced UI (same as before)
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Root variables for theme-aware colors */
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --secondary-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --warning-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        --neutral-gradient: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
    }
    
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    /* Custom header styling */
    .custom-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .custom-subtitle {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    /* Enhanced card styling */
    .stExpander {
        border: none !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        margin-bottom: 2rem !important;
    }
    
    .stExpander > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
    }
    
    /* Dark theme adjustments */
    [data-theme="dark"] .stExpander > div > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Light theme adjustments */
    [data-theme="light"] .stExpander > div > div > div {
        background: rgba(0, 0, 0, 0.02) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Enhanced selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 12px !important;
        border: 2px solid rgba(99, 102, 241, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Enhanced text input styling */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid rgba(99, 102, 241, 0.2) !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(99, 102, 241, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Enhanced toggle styling */
    .stCheckbox {
        padding: 1rem 0 !important;
    }
    
    /* Primary button styling */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3) !important;
        width: 100% !important;
        margin: 1rem 0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Download buttons styling */
    .stDownloadButton > button {
        background: var(--success-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        margin: 0.25rem !important;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Story display area */
    .story-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        font-size: 1.1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Dark theme story container */
    [data-theme="dark"] .story-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Light theme story container */
    [data-theme="light"] .story-container {
        background: rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Success message */
    .stSuccess {
        background: var(--success-gradient) !important;
        color: white !important;
    }
    
    /* Warning message */
    .stWarning {
        background: var(--warning-gradient) !important;
        color: white !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: rgba(99, 102, 241, 0.3) rgba(99, 102, 241, 0.3) rgba(99, 102, 241, 0.3) #6366f1 !important;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        font-size: 1.5rem;
        margin: 2rem 0 1rem 0;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* History section styling */
    .history-stats {
        background: rgba(99, 102, 241, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .story-metadata {
        background: rgba(107, 114, 128, 0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    /* Enhanced expander for history */
    .stExpander[data-testid="expander"] {
        margin-bottom: 1rem !important;
    }
    
    .stExpander[data-testid="expander"] > div > div {
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Search and filter styling */
    .history-controls {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .custom-header {
            font-size: 2.5rem;
        }
        
        .custom-subtitle {
            font-size: 1rem;
        }
        
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown('<h1 class="custom-header">AI Story Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="custom-subtitle">Generate creative stories with AI-powered storytelling using <strong>Groq LLM</strong></p>', unsafe_allow_html=True)
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# Dropdown options
genres = ["Fantasy", "Science Fiction", "Mystery", "Adventure", "Romance", "Horror", "Western", "Thriller", "Drama"]
themes = ["Friendship", "Good vs Evil", "Self-discovery", "Courage", "Betrayal", "Revenge", "Hope", "Identity", "Redemption"]
styles = ["Normal", "Humorous", "Dark", "Poetic", "Action-packed", "Philosophical", "Whimsical"]

# Initialize session state for story history
if 'story_history' not in st.session_state:
    st.session_state.story_history = []

# Story Configuration Section
with st.expander("Story Configuration", expanded=True):
    st.markdown("### Customize Your Story")
    col1, col2 = st.columns(2)
    with col1:
        genre = st.selectbox("Choose a Genre", genres)
        theme = st.selectbox("Select a Theme", themes)
    with col2:
        style = st.selectbox("Pick a Style", styles)
        characters_input = st.text_input("Characters", placeholder="Enter character names separated by commas...")
    use_emojis = st.toggle("Include emojis in story", value=True)

# Generate Story Button
st.markdown("### Generate Your Story")
story = ""
if st.button("Generate Story"):
    if characters_input.strip():
        characters = [name.strip() for name in characters_input.split(",") if name.strip()]
        with st.spinner("Crafting your story... Please wait..."):
            try:
                story = generate_story(genre, theme, characters, style, use_emojis)
                st.success("Story generated successfully!")

                # Log interaction to Google Sheet
                tracking_data = {
                    "genre": genre,
                    "theme": theme,
                    "style": style,
                    "characters": characters,
                    "use_emojis": use_emojis
                }
                try:
                    response = requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=tracking_data)
                except Exception as e:
                    pass  # Fail silently

                # Add to session state history
                story_entry = {
                    'timestamp': datetime.datetime.now(),
                    'genre': genre,
                    'theme': theme,
                    'style': style,
                    'characters': characters,
                    'use_emojis': use_emojis,
                    'story_preview': story[:200] + "..." if len(story) > 200 else story,
                    'story': story
                }
                st.session_state.story_history.insert(0, story_entry)

                # Display story
                st.markdown('<h3 class="section-header">Your Generated Story</h3>', unsafe_allow_html=True)
                st.markdown(f'<div class="story-container">{story}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please try again with different parameters.")
    else:
        st.warning("Please enter at least one character name.")

# Download Section
if story:
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">Download Your Story</h3>', unsafe_allow_html=True)
    download_col1, download_col2, download_col3 = st.columns([1, 1, 1])
    with download_col1:
        if st.download_button(
            "Download as TXT",
            data=story,
            file_name=f"story_{genre.replace(' ', '_').lower()}.txt",
            mime="text/plain"
        ):
            tracking_data = {
                "genre": genre,
                "theme": theme,
                "style": style,
                "characters": characters,
                "use_emojis": use_emojis,
                "downloaded": "TXT"
            }
            try:
                requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=tracking_data)
            except Exception as e:
                pass

    with download_col2:
        st.button("PDF (Coming Soon)", disabled=True)

    with download_col3:
        html_story = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generated Story</title>
            <style>
                body {{ font-family: 'Georgia', serif; line-height: 1.6; margin: 40px; }}
                h1 {{ color: #6366f1; text-align: center; }}
                .story {{ background: #f9f9f9; padding: 20px; border-radius: 10px; }}
            </style>
        </head>
        <body>
            <h1>Generated Story</h1>
            <div class="story">{story.replace(chr(10), '<br>')}</div>
        </body>
        </html>
        """
        if st.download_button(
            "Download as HTML",
            data=html_story,
            file_name=f"story_{genre.replace(' ', '_').lower()}.html",
            mime="text/html",
            key="html_download"
        ):
            tracking_data = {
                "genre": genre,
                "theme": theme,
                "style": style,
                "characters": characters,
                "use_emojis": use_emojis,
                "downloaded": "HTML"
            }
            try:
                requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=tracking_data)
            except Exception as e:
                pass

# Story History Section
if st.session_state.story_history:
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">Story History</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("Search stories", placeholder="Search by genre, theme, characters...")
    with col2:
        filter_genre = st.selectbox("Filter by Genre", ["All"] + genres)
    with col3:
        if st.button("Clear History"):
            st.session_state.story_history = []
            st.rerun()

    filtered_stories = st.session_state.story_history.copy()
    if search_term:
        filtered_stories = [
            s for s in filtered_stories
            if (search_term.lower() in s['genre'].lower() or
                search_term.lower() in s['theme'].lower() or
                search_term.lower() in ' '.join(s['characters']).lower())
        ]
    if filter_genre != "All":
        filtered_stories = [s for s in filtered_stories if s['genre'] == filter_genre]

    total_stories = len(st.session_state.story_history)
    st.markdown(f"**Showing {len(filtered_stories)} of {total_stories} stories**")

    for idx, entry in enumerate(filtered_stories):
        with st.expander(f"{entry['genre']} | {entry['theme']} | {entry['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Genre:** {entry['genre']}")
                st.markdown(f"**Theme:** {entry['theme']}")
                st.markdown(f"**Style:** {entry['style']}")
            with col2:
                st.markdown(f"**Characters:** {', '.join(entry['characters'])}")
                st.markdown(f"**Emojis:** {'Yes' if entry['use_emojis'] else 'No'}")
                st.markdown(f"**Created:** {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f'<div class="story-container">{entry["story"]}</div>', unsafe_allow_html=True)

            st.markdown("**Download this story:**")
            colA, colB = st.columns(2)
            with colA:
                st.download_button(
                    "TXT",
                    data=entry['story'],
                    file_name=f"story_{entry['genre'].replace(' ', '_').lower()}_{entry['timestamp'].strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    key=f"txt_{idx}"
                )
            with colB:
                html_content = f"""
                <!DOCTYPE html>
                <html><body>
                <h1>{entry['genre']} Story</h1>
                <p><strong>Genre:</strong> {entry['genre']}</p>
                <p><strong>Theme:</strong> {entry['theme']}</p>
                <p><strong>Characters:</strong> {', '.join(entry['characters'])}</p>
                <p><strong>Generated:</strong> {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                <div>{entry['story'].replace(chr(10), '<br>')}</div>
                </body></html>
                """
                st.download_button(
                    "HTML",
                    data=html_content,
                    file_name=f"story_{entry['genre'].replace(' ', '_').lower()}_{entry['timestamp'].strftime('%Y%m%d_%H%M')}.html",
                    mime="text/html",
                    key=f"html_{idx}"
                )

else:
    st.info("No stories generated yet. Create your first story above!")

# Footer
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.6;'>Made with Streamlit and Groq LLM</p>", unsafe_allow_html=True)
