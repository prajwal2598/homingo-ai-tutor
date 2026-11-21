# 🎓 MasteryAI — A Tutor for Every Learner

**MasteryAI** is an adaptive, multilingual AI tutor built for **Homingo Hack Days (Track C3: A tutor for every learner)**. Instead of dumping generic textbook lectures, MasteryAI diagnoses where a student is stuck, adapts its teaching style and language to their profile, and requires them to prove real understanding before unlocking mastery badges.

🌐 **Live App:** [Try MasteryAI Live on Streamlit](https://streamlit.app)

---

## ✨ Key Features
* **Adaptive Diagnostic Chat:** Starts with targeted diagnostic questions to uncover exact misconceptions before teaching.
* **Multilingual & Multimodal Learning:** Supports **English, Kannada, Hindi, Tamil, Telugu, and Malayalam**, and lets students upload **images or PDFs** of their notes or textbook problems.
* **Personalized Learner Profiles:** Adapts explanations by **Education Level** (School, PUC/High School, College, Self-Learner) and **Teaching Style** (Real-World Analogies, Step-by-Step Examples, Mini-Puzzles, Exam Revision).
* **Proof of Mastery ("Teach-Back" Verification):** Students explain the concept back in their own words and must score **8/10 or higher** to earn XP and unlock topic badges.

---

## 🛠️ Tech Stack & AI Tools Used
* **Frontend & App Framework:** Python, Streamlit
* **AI Model & SDK:** Google Gemini API (`google-genai` Python SDK)
* **Hosting & Version Control:** Streamlit Community Cloud & GitHub

---

## 🚀 Run Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd homingo-ai-tutor
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your Gemini API key:**
   Create a `.streamlit/secrets.toml` file in the root directory and add:
   ```toml
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
   ```
4. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

---

## 🔮 Future Roadmap
* **Voice-First Interaction:** Add speech-to-text and audio read-aloud for younger students and auditory learners.
* **Persistent Progress Tracking:** Store XP, streaks, and mastered topics across sessions using a cloud database.
* **Smart Flashcard Generator:** Automatically export missed diagnostic questions into downloadable revision cards.
