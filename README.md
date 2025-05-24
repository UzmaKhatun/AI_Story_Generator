# 🧙‍♀️ AI Story Generator – Powered by Groq LLM
A web app that generates imaginative, unique stories based on your selected genre, theme, writing style, and custom characters – all in a few seconds using the Groq LLM API. Built with Streamlit and designed for creators, writers, and AI enthusiasts.

---

## 🚀 Demo
🌐 Live App: [Click here to try it out!](https://ai-story-generator-webapp.streamlit.app/)
📽️ Video Walkthrough: [LinkedIn Demo]()

----

## 🔮 Features
- 📚 Select from various genres: Sci-fi, Fantasy, Mystery, Thriller...
- 🎭 Choose a story theme: Good vs Evil, Betrayal, Redemption...
- 🖋️ Pick your preferred writing style: Light, Neutral, Dark
- 🧑‍🤝‍🧑 Add your own character names
- 🌈 Optional emoji enhancement for fun storytelling
- 📥 Download stories as .txt or .html (PDF coming soon)
- 📜 View and filter past story history

---

## 🛠️ Tech Stack
|Tool | Purpose |
|Streamlit |	Frontend UI for story customization and output |
|Groq | LLM	Story generation engine (via API) |
|Dotenv	|API key protection |
|Tempfile |	Dynamic file download handling |
|Python	| Core scripting and logic |

⚙️ Setup Instructions
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/uzma-khatun/ai-story-generator.git
cd ai-story-generator
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Add Your Groq API Key
Create a .env file in the root directory and add:

env
Copy
Edit
GROQ_API_KEY=your_api_key_here
4. Run the App
bash
Copy
Edit
streamlit run app.py
📦 Upcoming Features
✅ PDF download support

✅ Login/Signup for user-based story tracking

🧠 Prompt fine-tuning for more creative control

📊 Analytics dashboard for user activity

👩‍💻 Author
Uzma Khatun – LinkedIn | GitHub

⭐ Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.
