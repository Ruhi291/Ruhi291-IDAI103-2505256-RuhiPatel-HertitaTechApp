🎨 ArtRestorer AI
AI-Powered Cultural Heritage Preservation Assistant
📌 Project Overview

ArtRestorer AI is a Generative AI-powered web application built using Python, Streamlit, and Google Gemini 1.5 Pro API.

The system is designed to assist museums, art historians, conservators, and heritage professionals by generating stylistically accurate restoration suggestions based on textual descriptions of damaged artworks.

Instead of using image uploads, the system works purely on descriptive metadata, allowing AI to simulate historical artistic reasoning and restoration techniques.

🌍 Problem Statement

Many historical artworks suffer from:

Water damage

Fading due to sunlight

Fire damage

Surface erosion

Missing sections

Mold and biological decay

Museums and restoration labs often lack complete documentation of the original artwork.

There is a need for:

AI-assisted restoration guidance

Culturally accurate reconstruction suggestions

Educational interpretation for public engagement

ArtRestorer AI bridges this gap using generative AI.

🎯 Objectives

Use Gemini 1.5 Pro API to generate restoration guidance.

Simulate historical artistic techniques using prompt engineering.

Provide culturally sensitive and period-specific outputs.

Allow creativity control using temperature tuning.

Develop a user-friendly web interface using Streamlit.

Deploy the system on GitHub and Streamlit Cloud.

🧠 Research Findings

The project research focused on:

Traditional restoration methods (sfumato, chiaroscuro, gold leaf repair).

Mughal miniature detailing techniques.

Fresco lime-based pigment restoration.

Sculpture reconstruction using symmetry analysis.

Textile weaving and embroidery conservation.

AI-based cultural preservation systems.

Generative AI can:

Emulate historical styles.

Suggest realistic color palettes.

Infer missing sections using contextual cues.

Maintain cultural and theological authenticity.

🛠 Technology Stack
Component	Technology Used
Programming Language	Python
Web Framework	Streamlit
AI Model	Google Gemini 1.5 Pro
API Integration	google-generativeai
Deployment	Streamlit Cloud
Version Control	GitHub
🔑 Gemini Model Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

Hyperparameter Tuning

Temperature range: 0.3 – 0.9

0.3 → Conservative, historically accurate restoration

0.7–0.9 → Creative, stylistic suggestions

Max output tokens: 2000

✨ Key Features (12 AI Restoration Modules)

ArtRestorer AI includes 12 specialized restoration features:

🎭 Baroque Painting Restoration

🖼 Renaissance Art Restoration

🕌 Mughal Miniature Restoration

🗿 Sculpture & 3D Art Restoration

🧵 Textile & Tapestry Restoration

📜 Medieval Manuscript Restoration

🎨 Modern & Abstract Art Restoration

🏛 Fresco & Mural Restoration

🎋 Asian Scroll & Screen Restoration

✝ Religious Icon Restoration

📸 Historic Photography Restoration

🏺 Pottery & Ceramic Restoration

Each feature:

Uses a customized prompt template

Includes cultural and period-specific instructions

Generates step-by-step restoration plans

Suggests materials and conservation techniques

🧩 Prompt Engineering Strategy

Each module uses structured prompts including:

Artwork type

Period/style

Artist (if known)

Damage description

Restoration goals

Example prompt:

“A Renaissance oil painting featuring a noblewoman. The lower right section is faded due to water damage. Suggest historically accurate restoration techniques maintaining sfumato effects.”

Prompts were refined to:

Improve cultural accuracy

Maintain stylistic consistency

Provide technical conservation steps

📊 Output Quality & Validation

Outputs were evaluated based on:

Historical accuracy

Cultural sensitivity

Technical feasibility

Artistic coherence

Relevance to input damage

Different artwork types and damage scenarios were tested to validate performance.

Temperature tuning was adjusted to balance creativity and realism.

🚀 Deployment
Files Included:
app.py
requirements.txt
README.md
.gitignore
.streamlit/secrets.toml

Deployment Steps:

Push repository to GitHub.

Connect repository to Streamlit Cloud.

Add GEMINI_API_KEY in Streamlit Cloud secrets.

Deploy and test on desktop & mobile.

📈 Strengths of the System

Multi-domain restoration coverage

Adjustable creativity

User-friendly interface

Secure API handling

Restoration history tracking

Dark & light mode support

Educational and professional value

🔮 Future Improvements

Image upload integration with AI image analysis

Multi-language support

Expert feedback validation module

AI-generated visual reconstruction previews

Database of historical references

🏁 Conclusion

ArtRestorer AI demonstrates how Generative AI can meaningfully support cultural heritage preservation.

By integrating Gemini 1.5 Pro with structured prompt engineering and user-friendly Streamlit deployment, this project successfully bridges:

Artificial Intelligence

Art Conservation

Historical Research

Educational Accessibility

The system provides scalable, culturally respectful, and technically detailed restoration guidance, proving that AI can enhance preservation efforts while maintaining historical authenticity.

<img width="1836" height="836" alt="image" src="https://github.com/user-attachments/assets/3c8e64b1-f46f-4bac-a0c6-9dd43213082c" />
