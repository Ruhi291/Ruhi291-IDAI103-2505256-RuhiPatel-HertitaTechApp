import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🎨 ArtRestorer AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

genai.configure(api_key="AIzaSyDQ1INhcUHP0Iou4EAuZRo5f3Y6JcZg5Ns")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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

# Initialize Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("⚠️ Gemini API key not found. Please add GEMINI_API_KEY to .streamlit/secrets.toml")
    st.stop()

# All 12 Restoration Features
RESTORATION_FEATURES = {
    "baroque_restoration": {
        "icon": "🎭",
        "name": "Baroque Painting Restoration",
        "description": "Restore Baroque artworks with dramatic lighting and rich shadows",
        "prompt_template": """You are an expert art restoration specialist for Baroque period artworks (1600-1750).

Artwork Details:
- Type: {artwork_type}
- Period: Baroque (1600-1750)
- Artist: {artist}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Analysis of Baroque characteristics (dramatic lighting, intense emotions, rich colors, chiaroscuro)
2. Specific step-by-step techniques to restore the damaged area
3. Color palette recommendations typical of Baroque period (deep reds, golds, browns)
4. Brushstroke patterns and texturing methods used by Baroque masters
5. How to maintain the dramatic chiaroscuro (light and shadow) effect
6. Materials needed for restoration
7. Conservation tips to prevent future damage

Be specific, technical, and historically accurate in your recommendations."""
    },

    "renaissance_restoration": {
        "icon": "🖼️",
        "name": "Renaissance Art Restoration",
        "description": "Restore Renaissance masterpieces with classical techniques",
        "prompt_template": """You are an expert art restoration specialist for Renaissance period artworks (1400-1600).

Artwork Details:
- Type: {artwork_type}
- Period: Renaissance (1400-1600)
- Artist: {artist}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Analysis of Renaissance characteristics (perspective, naturalism, balanced composition)
2. Techniques for restoring sfumato and chiaroscuro effects
3. Traditional pigments and materials (lapis lazuli, lead white, vermillion)
4. Methods to restore facial features and anatomical accuracy
5. Gold leaf restoration if applicable
6. Varnish removal and reapplication techniques
7. Panel vs canvas specific restoration approaches

Be historically accurate and technically precise."""
    },

    "mughal_miniature": {
        "icon": "🕌",
        "name": "Mughal Miniature Restoration",
        "description": "Restore intricate Mughal-era miniature paintings and manuscripts",
        "prompt_template": """You are an expert in Mughal miniature painting restoration.

Artwork Details:
- Type: Mughal Miniature
- Period: {period}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Analysis of Mughal miniature characteristics (fine details, vibrant colors, Persian influence)
2. Techniques for restoring floral borders and geometric patterns
3. Gold and silver leaf application methods
4. Traditional Mughal pigments (vermillion, indigo, gold)
5. Methods to restore facial features in the distinctive Mughal profile style
6. Border and margin restoration techniques
7. Paper support stabilization
8. Ink reconstruction methods

Focus on authenticity and traditional methods."""
    },

    "sculpture_restoration": {
        "icon": "🗿",
        "name": "Sculpture & 3D Art Restoration",
        "description": "Restore damaged sculptures, statues, and 3D artworks",
        "prompt_template": """You are an expert in sculpture and three-dimensional art restoration.

Sculpture Details:
- Material: {material}
- Period/Style: {period}
- Type: {sculpture_type}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Structural assessment and stability analysis
2. Material-specific restoration techniques for {material}
3. Methods to reconstruct missing features using symmetry and period references
4. Surface treatment and patina restoration
5. Adhesive and fill material recommendations
6. Support and mounting recommendations
7. Environmental protection strategies
8. Documentation methods before and after restoration

Be specific about materials, tools, and techniques."""
    },

    "textile_tapestry": {
        "icon": "🧵",
        "name": "Textile & Tapestry Restoration",
        "description": "Restore historic textiles, tapestries, and fabric artworks",
        "prompt_template": """You are an expert in textile and tapestry restoration.

Textile Details:
- Type: {textile_type}
- Period: {period}
- Material: {material}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Fiber analysis and conservation assessment
2. Thread matching and color restoration techniques
3. Weaving pattern reconstruction methods
4. Embroidery restoration techniques
5. Support backing recommendations
6. Wet cleaning vs dry cleaning considerations
7. Display and storage recommendations
8. Moth damage and biological threat treatment

Focus on preserving original materials while ensuring longevity."""
    },

    "medieval_manuscript": {
        "icon": "📜",
        "name": "Medieval Manuscript Restoration",
        "description": "Restore illuminated manuscripts, ancient texts, and religious scrolls",
        "prompt_template": """You are an expert in medieval manuscript and illuminated text restoration.

Manuscript Details:
- Type: {manuscript_type}
- Period: {period}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Parchment or vellum stabilization techniques
2. Ink restoration and missing text reconstruction
3. Illumination and gold leaf restoration
4. Margin decoration and border pattern restoration
5. Calligraphy style matching techniques
6. Binding repair recommendations
7. Pigment analysis and color matching
8. Humidity and environmental control for preservation

Maintain historical accuracy and use period-appropriate materials."""
    },

    "expressionist_abstract": {
        "icon": "🎨",
        "name": "Modern & Abstract Art Restoration",
        "description": "Restore Expressionist, Abstract, Cubist and Modern artworks",
        "prompt_template": """You are an expert in modern and abstract art restoration.

Artwork Details:
- Style: {style}
- Period: {period}
- Medium: {medium}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Analysis of the artist's unique technique and intention
2. Methods to recreate abstract brushwork and texture
3. Color field restoration techniques
4. Impasto and thick paint reconstruction
5. Techniques for restoring spontaneity and energy of brushstrokes
6. Modern material considerations (acrylic, synthetic pigments, mixed media)
7. Documentation of restoration decisions
8. Ethical considerations in restoring intentional damage or decay

Respect the artist's original vision and spontaneous energy."""
    },

    "fresco_mural": {
        "icon": "🏛️",
        "name": "Fresco & Mural Restoration",
        "description": "Restore ancient wall paintings, frescoes, and large-scale murals",
        "prompt_template": """You are an expert in fresco and mural restoration.

Fresco Details:
- Type: {fresco_type}
- Period: {period}
- Location: {location}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Structural assessment of wall, plaster, and support
2. True fresco (buon fresco) vs. secco fresco restoration differences
3. Lime-based pigment matching techniques
4. Water damage and salt efflorescence treatment
5. Detached plaster reattachment methods
6. Color restoration while preserving historical patina
7. Environmental control to prevent future damage
8. Documentation and photographic recording methods

Consider architectural context and historical significance."""
    },

    "asian_scroll": {
        "icon": "🎋",
        "name": "Asian Scroll & Screen Restoration",
        "description": "Restore Japanese, Chinese, Korean scroll paintings and screens",
        "prompt_template": """You are an expert in East Asian scroll and screen painting restoration.

Artwork Details:
- Origin: {origin}
- Style: {style}
- Period: {period}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Silk or paper support restoration and lining techniques
2. Ink wash painting reconstruction methods
3. Traditional mounting and remounting (hyogu) techniques
4. Seal and signature restoration
5. Brocade border and mounting fabric repair
6. Traditional East Asian pigment matching
7. Scroll roller and hanging mechanism restoration
8. Japanese or Chinese paper selection for repairs

Use traditional East Asian conservation methods."""
    },

    "icon_religious": {
        "icon": "✝️",
        "name": "Religious Icon Restoration",
        "description": "Restore Byzantine icons, sacred panel paintings and religious art",
        "prompt_template": """You are an expert in religious icon and sacred art restoration.

Icon Details:
- Tradition: {tradition}
- Period: {period}
- Panel Type: {panel_type}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Traditional icon painting techniques (egg tempera on gesso)
2. Symbolic color meanings and theologically accurate restoration
3. Face (liki) and hand (desnitsa) restoration following iconographic canons
4. Gold leaf (gilding) and halo restoration methods
5. Wood panel stabilization and crack consolidation
6. Darkened varnish (olifa) removal techniques
7. Respect for religious significance during restoration
8. Documentation respecting theological importance

Maintain theological authenticity and artistic tradition."""
    },

    "photography_restoration": {
        "icon": "📸",
        "name": "Historic Photography Restoration",
        "description": "Restore vintage photographs and early photographic processes",
        "prompt_template": """You are an expert in historic photography and photographic print restoration.

Photograph Details:
- Process: {process}
- Period: {period}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Identification and analysis of photographic process characteristics
2. Chemical deterioration assessment and stabilization
3. Physical damage repair (tears, creases, missing sections)
4. Fading and silver mirroring treatment
5. Foxing and mold removal techniques
6. Digital vs. analog restoration decision framework
7. Archival housing and storage recommendations
8. Digitization best practices for preservation

Preserve historical integrity while ensuring long-term stability."""
    },

    "pottery_ceramic": {
        "icon": "🏺",
        "name": "Pottery & Ceramic Restoration",
        "description": "Restore ceramic vessels, ancient pottery and glazed artworks",
        "prompt_template": """You are an expert in ceramic and pottery restoration.

Ceramic Details:
- Type: {ceramic_type}
- Period/Culture: {period}
- Glaze Type: {glaze}
- Damage Description: {damage}

Provide detailed restoration suggestions including:
1. Fragment identification, sorting, and cleaning
2. Adhesive selection for different ceramic bodies
3. Missing section fill and reconstruction methods
4. Glaze matching techniques for different glaze types
5. Surface retouching and color matching
6. Structural reinforcement for display
7. Documentation of all restoration decisions
8. Display mount and support recommendations

Balance aesthetic restoration with archaeological integrity."""
    }
}

# Sidebar
with st.sidebar:
    st.title("🎨 ArtRestorer AI")
    st.markdown("---")

    # Dark mode toggle
    if st.button("🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'home'
        st.session_state.selected_feature = None
        st.rerun()

    if st.button("📊 My Restorations", use_container_width=True):
        st.session_state.page = 'history'
        st.rerun()

    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = 'about'
        st.rerun()

    st.markdown("---")
    st.markdown("### 📈 Statistics")
    st.metric("Total Restorations", len(st.session_state.restorations))
    unique_types = len(set(r.get('feature', '') for r in st.session_state.restorations))
    st.metric("Art Types Explored", unique_types)

# ---- HOME PAGE ----
if st.session_state.page == 'home':

    if st.session_state.selected_feature is None:
        st.markdown('<div class="main-header"><h1>🎨 ArtRestorer AI</h1><p>AI-Powered Cultural Heritage Preservation Assistant</p></div>', unsafe_allow_html=True)

        st.markdown("### 🎯 Select a Restoration Feature")
        st.markdown("Choose the type of artwork you want to restore:")
        st.markdown("")

        cols = st.columns(3)
        for idx, (key, feature) in enumerate(RESTORATION_FEATURES.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{feature['icon']} {feature['name']}</h3>
                    <p>{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {feature['icon']}", key=key, use_container_width=True):
                    st.session_state.selected_feature = key
                    st.rerun()

    else:
        feature = RESTORATION_FEATURES[st.session_state.selected_feature]
        st.markdown(f'<div class="main-header"><h1>{feature["icon"]} {feature["name"]}</h1><p>{feature["description"]}</p></div>', unsafe_allow_html=True)

        with st.form("restoration_form"):
            st.markdown("### 📝 Enter Artwork Details")

            if st.session_state.selected_feature == "baroque_restoration":
                artwork_type = st.selectbox("🖼️ Artwork Type", ["Oil Painting", "Canvas Painting", "Wood Panel", "Copper Plate"])
                artist = st.text_input("🎨 Artist (if known)", placeholder="e.g., Caravaggio, Rembrandt, Rubens")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe damage in detail e.g., Top right corner has water damage with paint flaking and color fading...")
                input_data = {"artwork_type": artwork_type, "artist": artist if artist else "Unknown", "damage": damage}

            elif st.session_state.selected_feature == "renaissance_restoration":
                artwork_type = st.selectbox("🖼️ Artwork Type", ["Oil Painting", "Tempera on Wood", "Fresco", "Canvas", "Wood Panel"])
                artist = st.text_input("🎨 Artist (if known)", placeholder="e.g., Leonardo da Vinci, Michelangelo, Raphael")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe damage in detail...")
                input_data = {"artwork_type": artwork_type, "artist": artist if artist else "Unknown", "damage": damage}

            elif st.session_state.selected_feature == "mughal_miniature":
                period = st.selectbox("📅 Period", ["Early Mughal (1526-1605)", "Classical Mughal (1605-1707)", "Late Mughal (1707-1857)"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe fading, tears, or missing sections...")
                input_data = {"period": period, "damage": damage}

            elif st.session_state.selected_feature == "sculpture_restoration":
                material = st.selectbox("🪨 Material", ["Marble", "Bronze", "Sandstone", "Limestone", "Terracotta", "Wood", "Plaster"])
                period = st.text_input("📅 Period/Style", placeholder="e.g., Classical Greek, Gothic, Renaissance, Modern")
                sculpture_type = st.selectbox("🗿 Sculpture Type", ["Freestanding Statue", "Relief Sculpture", "Bust", "Figurine", "Architectural Element"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe cracks, missing parts, erosion, surface damage...")
                input_data = {"material": material, "period": period, "sculpture_type": sculpture_type, "damage": damage}

            elif st.session_state.selected_feature == "textile_tapestry":
                textile_type = st.selectbox("🧵 Textile Type", ["Wall Tapestry", "Embroidered Panel", "Carpet/Rug", "Ceremonial Banner", "Religious Textile"])
                period = st.text_input("📅 Period", placeholder="e.g., Medieval, Renaissance, 18th Century, Victorian")
                material = st.selectbox("🧶 Material", ["Wool", "Silk", "Cotton", "Linen", "Gold Thread", "Mixed Fibers"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe tears, fading, moth damage, missing sections...")
                input_data = {"textile_type": textile_type, "period": period, "material": material, "damage": damage}

            elif st.session_state.selected_feature == "medieval_manuscript":
                manuscript_type = st.selectbox("📜 Manuscript Type", ["Illuminated Manuscript", "Religious Scripture", "Royal Charter", "Book of Hours", "Scientific Text", "Poetry Collection"])
                period = st.text_input("📅 Period", placeholder="e.g., 12th Century, Gothic Era, Early Medieval")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe ink fading, torn pages, water damage, mold...")
                input_data = {"manuscript_type": manuscript_type, "period": period, "damage": damage}

            elif st.session_state.selected_feature == "expressionist_abstract":
                style = st.selectbox("🎨 Art Style", ["Abstract Expressionism", "Expressionism", "Cubism", "Surrealism", "Pop Art", "Minimalism", "Fauvism"])
                period = st.text_input("📅 Period", placeholder="e.g., 1950s, Post-War, 1920s")
                medium = st.selectbox("🖌️ Medium", ["Oil on Canvas", "Acrylic on Canvas", "Mixed Media", "Collage", "Watercolor"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe texture loss, cracking, fading, surface damage...")
                input_data = {"style": style, "period": period, "medium": medium, "damage": damage}

            elif st.session_state.selected_feature == "fresco_mural":
                fresco_type = st.selectbox("🏛️ Fresco Type", ["Buon Fresco (True Fresco)", "Secco Fresco", "Modern Wall Mural", "Cave Painting"])
                period = st.text_input("📅 Period", placeholder="e.g., Renaissance, Ancient Roman, Byzantine")
                location = st.text_input("📍 Location", placeholder="e.g., Church ceiling, Villa wall, Public building")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe water damage, detachment, salt efflorescence, fading...")
                input_data = {"fresco_type": fresco_type, "period": period, "location": location, "damage": damage}

            elif st.session_state.selected_feature == "asian_scroll":
                origin = st.selectbox("🌏 Origin", ["Japanese", "Chinese", "Korean", "Vietnamese", "Tibetan"])
                style = st.selectbox("🖌️ Style", ["Ink Wash Painting (Sumi-e)", "Yamato-e", "Literati Painting", "Bird-and-Flower", "Landscape Painting"])
                period = st.text_input("📅 Period", placeholder="e.g., Edo Period, Ming Dynasty, Joseon Dynasty")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe tears, water stains, detached mounting, foxing...")
                input_data = {"origin": origin, "style": style, "period": period, "damage": damage}

            elif st.session_state.selected_feature == "icon_religious":
                tradition = st.selectbox("✝️ Tradition", ["Byzantine", "Russian Orthodox", "Greek Orthodox", "Coptic", "Ethiopian"])
                period = st.text_input("📅 Period", placeholder="e.g., 14th Century, Byzantine Period, Medieval")
                panel_type = st.selectbox("🖼️ Panel Type", ["Wood Panel with Gesso", "Canvas on Wood", "Metal Plate", "Stone"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe cracks, flaking paint, darkened varnish, missing gilding...")
                input_data = {"tradition": tradition, "period": period, "panel_type": panel_type, "damage": damage}

            elif st.session_state.selected_feature == "photography_restoration":
                process = st.selectbox("📷 Photographic Process", ["Daguerreotype", "Albumen Print", "Gelatin Silver Print", "Cyanotype", "Platinum/Palladium Print", "Tintype", "Calotype"])
                period = st.text_input("📅 Period", placeholder="e.g., 1890s, Victorian Era, 1920s, World War II era")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe fading, tears, foxing, chemical damage, silver mirroring...")
                input_data = {"process": process, "period": period, "damage": damage}

            elif st.session_state.selected_feature == "pottery_ceramic":
                ceramic_type = st.selectbox("🏺 Ceramic Type", ["Decorative Vase", "Storage Vessel", "Ritual Bowl", "Figurine", "Decorative Tile", "Funerary Urn", "Serving Plate"])
                period = st.text_input("📅 Period/Culture", placeholder="e.g., Ancient Greek, Ming Dynasty, Pre-Columbian, Edo Period")
                glaze = st.selectbox("✨ Glaze Type", ["Fully Glazed", "Unglazed (Terracotta)", "Partially Glazed", "Hand-Painted Decoration", "Celadon Glaze", "Blue and White"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe cracks, missing pieces, glaze loss, chips, staining...")
                input_data = {"ceramic_type": ceramic_type, "period": period, "glaze": glaze, "damage": damage}

            st.markdown("---")
            temperature = st.slider(
                "🎚️ Creativity Level",
                min_value=0.3,
                max_value=0.9,
                value=0.7,
                step=0.1,
                help="Lower (0.3) = Conservative, accurate restorations | Higher (0.9) = Creative, imaginative suggestions"
            )

            submit = st.form_submit_button("🎨 Generate Restoration Plan", use_container_width=True, type="primary")

            if submit:
                if all(str(v).strip() for v in input_data.values()):
                    with st.spinner("🤖 AI is analyzing your artwork and generating restoration recommendations..."):
                        try:
                            prompt = feature["prompt_template"].format(**input_data)

                            response = model.generate_content(
                                prompt,
                                generation_config=genai.types.GenerationConfig(
                                    temperature=temperature,
                                    max_output_tokens=2000,
                                )
                            )

                            result = response.text

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
                            st.success("✅ Restoration plan generated successfully!")
                            st.balloons()

                        except Exception as e:
                            st.error(f"❌ Error generating restoration plan: {str(e)}")
                else:
                    st.error("⚠️ Please fill in all fields before generating a restoration plan.")

        st.markdown("---")
        if st.button("← Back to All Features", use_container_width=True):
            st.session_state.selected_feature = None
            st.rerun()

# ---- HISTORY PAGE ----
elif st.session_state.page == 'history':
    st.markdown('<div class="main-header"><h1>📊 My Restoration History</h1><p>View all your previous art restoration projects</p></div>', unsafe_allow_html=True)

    if len(st.session_state.restorations) == 0:
        st.info("📭 No restorations yet! Go to Home and select a restoration feature to get started.")
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
    st.markdown('<div class="main-header"><h1>ℹ️ About ArtRestorer AI</h1><p>Bridging AI and Cultural Heritage Preservation</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card">
        <h3>🎯 Mission</h3>
        <p>ArtRestorer AI bridges the gap between artificial intelligence and cultural preservation,
        helping museums, conservators, and heritage experts digitally reconstruct cultural masterpieces
        through AI-generated restoration guidance using Google Gemini 2.0 Flash.</p>
    </div>

    <div class="info-card">
        <h3>✨ Key Features</h3>
        <ul>
            <li>12 specialized restoration tools for different art forms</li>
            <li>Period-specific and culturally accurate recommendations</li>
            <li>Adjustable creativity level for different restoration needs</li>
            <li>Dark mode and light mode support</li>
            <li>Restoration history tracking</li>
            <li>AI-powered using Google Gemini 2.0 Flash</li>
        </ul>
    </div>

    <div class="info-card">
        <h3>🎨 Supported Art Forms</h3>
        <ul>
            <li>🎭 Baroque Paintings</li>
            <li>🖼️ Renaissance Masterpieces</li>
            <li>🕌 Mughal Miniatures</li>
            <li>🗿 Sculptures & 3D Artworks</li>
            <li>🧵 Textiles & Tapestries</li>
            <li>📜 Medieval Manuscripts</li>
            <li>🎨 Modern & Abstract Art</li>
            <li>🏛️ Frescoes & Murals</li>
            <li>🎋 Asian Scrolls & Screens</li>
            <li>✝️ Religious Icons</li>
            <li>📸 Historic Photography</li>
            <li>🏺 Pottery & Ceramics</li>
        </ul>
    </div>

    <div class="info-card">
        <h3>🔬 Technology Stack</h3>
        <p><strong>AI Model:</strong> Google Gemini 2.0 Flash</p>
        <p><strong>Framework:</strong> Streamlit</p>
        <p><strong>Language:</strong> Python</p>
        <p><strong>Purpose:</strong> Educational & Professional Art Conservation Support</p>
    </div>
    """, unsafe_allow_html=True)