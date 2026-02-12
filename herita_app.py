import streamlit as st
import requests
import json
from datetime import datetime
 
# Page configuration
st.set_page_config(
    page_title="🎨 ArtRestorer AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# Initialize Gemini API with secrets
def get_api_key():
    """Get API key from secrets"""
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("❌ API Key not found! Please add GEMINI_API_KEY to .streamlit/secrets.toml")
            st.stop()
       
        api_key = st.secrets["GEMINI_API_KEY"]
       
        if not api_key or api_key.strip() == "":
            st.error("❌ API Key is empty!")
            st.stop()
       
        return api_key
   
    except Exception as e:
        st.error(f"❌ Error loading API key: {str(e)}")
        st.stop()
 
# Function to call Gemini API using REST
def generate_content_with_gemini(prompt, temperature=0.7):
    """Generate content using Gemini REST API"""
    api_key = get_api_key()
   
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
   
    headers = {
        "Content-Type": "application/json"
    }
   
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 2000,
        }
    }
   
    try:
        response = requests.post(url, headers=headers, json=data)
       
        if response.status_code == 200:
            result = response.json()
           
            # Extract text from response
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text
            else:
                return "❌ No response generated. Please try again."
       
        elif response.status_code == 400:
            error_data = response.json()
            return f"❌ Bad Request: {error_data.get('error', {}).get('message', 'Unknown error')}"
       
        elif response.status_code == 403:
            return "❌ API Key is invalid or doesn't have permission. Please check your key."
       
        elif response.status_code == 404:
            return "❌ Model not found. The API endpoint may have changed."
       
        else:
            return f"❌ Error {response.status_code}: {response.text}"
   
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {str(e)}"
   
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
 
# Dark mode state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'restorations' not in st.session_state:
    st.session_state.restorations = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_feature' not in st.session_state:
    st.session_state.selected_feature = None
 
# CSS based on dark mode
if st.session_state.dark_mode:
    bg = "#1e1e1e"
    text = "#e0e0e0"
    card = "#2d2d2d"
    header = "linear-gradient(135deg, #2d3436 0%, #34495e 100%)"
    border = "#4a5568"
    h1_color = "#90caf9"
    h2_color = "#80cbc4"
    label_color = "#a5d6a7"
    output_bg = "#1a237e"
    output_text = "#bbdefb"
    info_bg = "#1b5e20"
    info_text = "#c8e6c9"
else:
    bg = "#ffffff"
    text = "#2c3e50"
    card = "#f8f9fa"
    header = "linear-gradient(135deg, #fce4ec 0%, #f3e5f5 100%)"
    border = "#880e4f"
    h1_color = "#4a148c"
    h2_color = "#6a1b9a"
    label_color = "#1b5e20"
    output_bg = "#e1f5fe"
    output_text = "#0d47a1"
    info_bg = "#e8f5e9"
    info_text = "#1b5e20"
 
st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg};
        color: {text};
    }}
    .main-header {{
        text-align: center;
        padding: 2rem;
        background: {header};
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 2px solid {border};
    }}
    .main-header h1 {{
        color: {h1_color};
        font-weight: bold;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}
    .main-header p {{
        color: {h2_color};
        font-size: 1.2rem;
        font-weight: 600;
    }}
    .feature-card {{
        background: {card};
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid {border};
        margin: 0.5rem 0;
        text-align: center;
    }}
    .feature-card h3 {{
        color: {h1_color};
        font-weight: bold;
        font-size: 1.1rem;
    }}
    .feature-card p {{
        color: {h2_color};
        font-size: 0.9rem;
        font-weight: 500;
    }}
    .info-card {{
        background: {info_bg};
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid {border};
        margin: 1rem 0;
    }}
    .info-card h3 {{
        color: {info_text};
        font-weight: bold;
        font-size: 1.3rem;
    }}
    .info-card p, .info-card li {{
        color: {info_text};
        font-weight: 500;
        font-size: 1.05rem;
        line-height: 1.8;
    }}
    .output-box {{
        background: {output_bg};
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #01579b;
        border: 2px solid #0277bd;
        margin: 1rem 0;
    }}
    .output-box h3 {{
        color: {output_text};
        font-weight: bold;
        font-size: 1.3rem;
    }}
    .output-box p {{
        color: {output_text};
        font-weight: 500;
        font-size: 1.05rem;
        line-height: 1.8;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {h1_color} !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }}
    .stMarkdown h1, .stMarkdown h2,
    .stMarkdown h3, .stMarkdown h4 {{
        color: {h1_color} !important;
        font-weight: 900 !important;
        font-size: 1.5rem !important;
    }}
    p, li, span {{
        color: {text} !important;
        font-weight: 500 !important;
    }}
    label, .stSelectbox label,
    .stTextInput label, .stTextArea label,
    .stSlider label {{
        color: {label_color} !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }}
    .stMetric label {{
        color: {label_color} !important;
        font-weight: 800 !important;
    }}
    .stMetric .metric-value {{
        color: {h1_color} !important;
        font-weight: 900 !important;
    }}
    .stSidebar {{
        background-color: {card} !important;
    }}
    .stSidebar h1, .stSidebar h2,
    .stSidebar h3, .stSidebar p {{
        color: {h1_color} !important;
        font-weight: 800 !important;
    }}
</style>
""", unsafe_allow_html=True)
 
# Sidebar navigation
with st.sidebar:
    st.markdown("### 🎨 Navigation")
   
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.page == 'home' else "secondary"):
        st.session_state.page = 'home'
        st.session_state.selected_feature = None
        st.rerun()
   
    if st.button("📊 My History", use_container_width=True, type="primary" if st.session_state.page == 'history' else "secondary"):
        st.session_state.page = 'history'
        st.rerun()
   
    if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.page == 'about' else "secondary"):
        st.session_state.page = 'about'
        st.rerun()
   
    st.markdown("---")
   
    # Dark mode toggle
    dark_mode_toggle = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode_toggle
        st.rerun()
   
    st.markdown("---")
    st.markdown("### 📈 Statistics")
    st.metric("Total Restorations", len(st.session_state.restorations))
 
# Feature definitions (simplified - showing just 3 for testing)
FEATURES = {
    "baroque_painting": {
        "name": "🎭 Baroque Painting Restoration",
        "icon": "🎭",
        "description": "Restore dramatic Baroque masterpieces with chiaroscuro techniques",
        "prompt_template": """You are an expert art conservator specializing in Baroque period paintings (1600-1750).
 
Artist/School: {artist}
Period: {period}
Medium: {medium}
Damage Description: {damage}
 
Please provide:
1. **Assessment**: Analyze the painting's condition, typical Baroque techniques (chiaroscuro, dramatic lighting, rich colors), and the extent of damage.
2. **Restoration Approach**: Detail the step-by-step restoration process specific to Baroque paintings.
3. **Materials & Techniques**: Recommend period-appropriate materials and modern conservation methods.
4. **Color Matching**: Guidance on matching the rich, deep colors characteristic of Baroque art.
5. **Preservation**: Long-term care recommendations.
 
Be detailed and historically accurate."""
    },
    "renaissance_painting": {
        "name": "🖼️ Renaissance Masterpiece Restoration",
        "icon": "🖼️",
        "description": "Restore Renaissance paintings with classical techniques and precision",
        "prompt_template": """You are an expert art conservator specializing in Renaissance paintings (1400-1600).
 
Artist/Region: {artist}
Period: {period}
Medium: {medium}
Damage Description: {damage}
 
Please provide detailed restoration recommendations including assessment, restoration plan, and preservation guidelines."""
    },
    "sculpture_3d": {
        "name": "🗿 Sculpture & 3D Artwork Restoration",
        "icon": "🗿",
        "description": "Restore sculptures, statues, and three-dimensional artworks",
        "prompt_template": """You are an expert conservator specializing in three-dimensional artworks and sculptures.
 
Sculpture Type: {sculpture_type}
Material: {material}
Period/Style: {period}
Damage Description: {damage}
 
Provide detailed restoration recommendations."""
    }
}
 
# ---- HOME PAGE ----
if st.session_state.page == 'home':
    if st.session_state.selected_feature is None:
        st.markdown('<div class="main-header"><h1>🎨 ArtRestorer AI</h1><p>AI-Powered Cultural Heritage Preservation</p></div>', unsafe_allow_html=True)
       
        st.markdown("### 🎯 Select a Restoration Type")
        st.markdown("Choose from our specialized AI restoration tools designed for different art forms and periods.")
       
        cols = st.columns(3)
       
        for idx, (feature_key, feature) in enumerate(FEATURES.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{feature['icon']} {feature['name'].split(' ', 1)[1]}</h3>
                    <p>{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
               
                if st.button(f"Select {feature['icon']}", key=f"btn_{feature_key}", use_container_width=True):
                    st.session_state.selected_feature = feature_key
                    st.rerun()
   
    else:
        feature = FEATURES[st.session_state.selected_feature]
        st.markdown(f'<div class="main-header"><h1>{feature["icon"]} {feature["name"]}</h1><p>{feature["description"]}</p></div>', unsafe_allow_html=True)
       
        with st.form("restoration_form"):
            st.markdown("### 📝 Artwork Details")
           
            input_data = {}
           
            if st.session_state.selected_feature == "baroque_painting":
                artist = st.text_input("🎨 Artist/School", placeholder="e.g., Caravaggio, Rembrandt, Rubens School")
                period = st.text_input("📅 Period", placeholder="e.g., Early Baroque (1600-1625), High Baroque")
                medium = st.selectbox("🖌️ Medium", ["Oil on Canvas", "Oil on Wood Panel", "Tempera", "Mixed Media"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe cracks, darkened varnish, paint loss, canvas tears...")
                input_data = {"artist": artist, "period": period, "medium": medium, "damage": damage}
 
            elif st.session_state.selected_feature == "renaissance_painting":
                artist = st.text_input("🎨 Artist/Region", placeholder="e.g., Leonardo da Vinci, Florentine School")
                period = st.text_input("📅 Period", placeholder="e.g., Early Renaissance, High Renaissance")
                medium = st.selectbox("🖌️ Medium", ["Egg Tempera on Wood", "Oil on Canvas", "Fresco"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe condition issues...")
                input_data = {"artist": artist, "period": period, "medium": medium, "damage": damage}
 
            elif st.session_state.selected_feature == "sculpture_3d":
                sculpture_type = st.selectbox("🗿 Sculpture Type", ["Statue", "Bust", "Relief", "Monument"])
                material = st.selectbox("🪨 Material", ["Marble", "Bronze", "Wood", "Stone"])
                period = st.text_input("📅 Period/Style", placeholder="e.g., Classical Greek, Roman, Gothic")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe breaks, missing parts...")
                input_data = {"sculpture_type": sculpture_type, "material": material, "period": period, "damage": damage}
 
            st.markdown("---")
            temperature = st.slider(
                "🎚️ Creativity Level",
                min_value=0.3,
                max_value=0.9,
                value=0.7,
                step=0.1,
                help="Lower = Conservative | Higher = Creative"
            )
 
            submit = st.form_submit_button("🎨 Generate Restoration Plan", use_container_width=True, type="primary")
 
            if submit:
                if all(str(v).strip() for v in input_data.values()):
                    with st.spinner("🤖 AI is analyzing your artwork..."):
                        try:
                            prompt = feature["prompt_template"].format(**input_data)
                           
                            # Call Gemini API using REST
                            result = generate_content_with_gemini(prompt, temperature)
 
                            st.session_state.restorations.append({
                                'feature': st.session_state.selected_feature,
                                'feature_name': feature['name'],
                                'input_data': input_data,
                                'result': result,
                                'timestamp': datetime.now().isoformat(),
                                'temperature': temperature
                            })
 
                            st.markdown("### ✅ AI Restoration Recommendations")
                            st.markdown(f'<div class="output-box"><h3>🎨 Restoration Analysis & Plan</h3><p>{result}</p></div>', unsafe_allow_html=True)
                           
                            if not result.startswith("❌"):
                                st.success("✅ Restoration plan generated successfully!")
                                st.balloons()
 
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.error("⚠️ Please fill in all fields.")
 
        st.markdown("---")
        if st.button("← Back to All Features", use_container_width=True):
            st.session_state.selected_feature = None
            st.rerun()
 
# ---- HISTORY PAGE ----
elif st.session_state.page == 'history':
    st.markdown('<div class="main-header"><h1>📊 My Restoration History</h1><p>View all your previous projects</p></div>', unsafe_allow_html=True)
 
    if len(st.session_state.restorations) == 0:
        st.info("📭 No restorations yet! Go to Home to get started.")
    else:
        st.success(f"✅ You have completed {len(st.session_state.restorations)} restoration(s)!")
        for idx, restoration in enumerate(reversed(st.session_state.restorations)):
            with st.expander(f"🎨 {restoration['feature_name']} — {restoration['timestamp'][:10]}", expanded=(idx == 0)):
                st.markdown("**📝 Input Details:**")
                for key, value in restoration['input_data'].items():
                    st.write(f"- **{key.replace('_', ' ').title()}:** {value}")
                st.markdown("**🎨 Restoration Plan:**")
                st.markdown(f'<div class="output-box"><p>{restoration["result"]}</p></div>', unsafe_allow_html=True)
 
# ---- ABOUT PAGE ----
elif st.session_state.page == 'about':
    st.markdown('<div class="main-header"><h1>ℹ️ About ArtRestorer AI</h1><p>AI-Powered Art Conservation</p></div>', unsafe_allow_html=True)
 
    st.markdown(f"""
    <div class="info-card">
        <h3>🎯 Mission</h3>
        <p>ArtRestorer AI helps museums, conservators, and heritage experts with AI-generated
        restoration guidance using Google Gemini.</p>
    </div>
 
    <div class="info-card">
        <h3>🔬 Technology</h3>
        <p><strong>AI Model:</strong> Google Gemini 1.5 Flash</p>
        <p><strong>Framework:</strong> Streamlit</p>
        <p><strong>API:</strong> REST API (Direct HTTP calls)</p>
    </div>
    """, unsafe_allow_html=True)