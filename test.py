# test_story.py

from story_engine import generate_story

# Test input
genre = "Horror"
theme = "Friendship"
characters = "A curious scientist, a loyal robot, and a time-traveling cat"
use_emojis = True
style = "poetic"

# Generate the story
story = generate_story(genre, theme, characters, style, use_emojis)

# Print the story
print("\n📘 Generated Story:\n")
print(story)
