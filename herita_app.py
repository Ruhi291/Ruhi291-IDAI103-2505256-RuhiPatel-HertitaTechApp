import streamlit as st
from google import genai
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🎨 ArtRestorer AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini API with secrets
@st.cache_resource
def initialize_gemini():
    """Initialize Gemini client with API key from secrets"""
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("❌ API Key not found! Please add GEMINI_API_KEY to .streamlit/secrets.toml")
            st.stop()
        
        api_key = st.secrets["GEMINI_API_KEY"]
        
        if not api_key or api_key.strip() == "":
            st.error("❌ API Key is empty!")
            st.stop()
        
        client = genai.Client(api_key=api_key)
        return client
    
    except Exception as e:
        st.error(f"❌ Error initializing Gemini: {str(e)}")
        st.stop()

# Initialize the client
client = initialize_gemini()

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

# Feature definitions
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
2. **Restoration Approach**: Detail the step-by-step restoration process specific to Baroque paintings, including cleaning, stabilization, and inpainting techniques.
3. **Materials & Techniques**: Recommend period-appropriate materials and modern conservation methods.
4. **Color Matching**: Guidance on matching the rich, deep colors characteristic of Baroque art.
5. **Preservation**: Long-term care recommendations to preserve this historical artwork.

Be detailed, historically accurate, and consider the dramatic nature of Baroque art."""
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

Please provide:
1. **Historical Context**: Explain the painting's historical significance and Renaissance techniques (sfumato, linear perspective, naturalism).
2. **Condition Assessment**: Detailed analysis of the damage and its impact on the artwork.
3. **Restoration Plan**: Step-by-step conservation process respecting Renaissance materials and techniques.
4. **Technical Considerations**: Address challenges specific to Renaissance art (egg tempera, wood panels, gold leaf).
5. **Documentation**: Recommendations for documenting the restoration process.
6. **Ethical Considerations**: Balance between preserving original work and necessary interventions.

Focus on historical accuracy and reverence for the masterwork."""
    },
    "mughal_miniature": {
        "name": "🕌 Mughal Miniature Conservation",
        "icon": "🕌",
        "description": "Preserve intricate Mughal miniature paintings with traditional methods",
        "prompt_template": """You are an expert conservator specializing in Mughal miniature paintings (16th-19th century).

School/Period: {school}
Subject Matter: {subject}
Base Material: {material}
Damage Description: {damage}

Please provide:
1. **Cultural Context**: Explain the painting's historical and cultural significance in Mughal art tradition.
2. **Technical Analysis**: Assess the intricate details, gold work, natural pigments, and traditional techniques.
3. **Damage Assessment**: Analyze specific issues (pigment loss, paper deterioration, binding damage, foxing).
4. **Conservation Approach**: Detailed restoration plan using traditional Indian conservation methods combined with modern techniques.
5. **Materials**: Recommend appropriate conservation materials respecting traditional Mughal painting techniques.
6. **Handling Guidelines**: Special care instructions for these delicate artworks.
7. **Display Recommendations**: Lighting, humidity, and mounting suggestions.

Be culturally sensitive and technically precise."""
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

Please provide:
1. **Material Analysis**: Assess the sculpture's material (stone, bronze, wood, etc.) and its condition.
2. **Structural Assessment**: Evaluate structural integrity and stability issues.
3. **Damage Evaluation**: Analyze breaks, missing pieces, surface deterioration, patina loss, etc.
4. **Restoration Strategy**: Detailed plan for cleaning, stabilization, reconstruction, and finishing.
5. **Technical Methods**: Specific techniques for the material type (welding, bonding, carving, molding).
6. **Color/Patina Matching**: Guidelines for matching original surface treatments.
7. **Support & Display**: Recommendations for mounting and display systems.
8. **Environmental Control**: Temperature, humidity, and light exposure guidelines.

Focus on both aesthetic and structural integrity."""
    },
    "textile_tapestry": {
        "name": "🧵 Textile & Tapestry Conservation",
        "icon": "🧵",
        "description": "Restore historical textiles, tapestries, and fabric artworks",
        "prompt_template": """You are an expert textile conservator specializing in historical fabrics and tapestries.

Textile Type: {textile_type}
Period: {period}
Material/Fibers: {material}
Damage Description: {damage}

Please provide:
1. **Fiber Analysis**: Assess the textile's material, weave structure, and dye analysis.
2. **Condition Report**: Detail all damage (tears, fading, moth damage, weakened fibers, stains).
3. **Conservation Plan**: Step-by-step process for cleaning, stabilization, and repair.
4. **Stabilization Methods**: Techniques for supporting weakened areas and preventing further damage.
5. **Cleaning Approach**: Safe cleaning methods appropriate for the textile type and dyes.
6. **Repair Techniques**: Detailed guidance on weaving, patching, or invisible mending.
7. **Storage & Display**: Proper mounting, hanging, and storage recommendations.
8. **Pest Prevention**: Protection against moths, beetles, and other textile pests.

Be gentle and preservation-focused in your approach."""
    },
    "medieval_manuscript": {
        "name": "📜 Medieval Manuscript Restoration",
        "icon": "📜",
        "description": "Preserve illuminated manuscripts and ancient texts",
        "prompt_template": """You are an expert manuscript conservator specializing in medieval illuminated manuscripts and ancient texts.

Manuscript Type: {manuscript_type}
Period: {period}
Damage Description: {damage}

Please provide:
1. **Manuscript Analysis**: Assess the parchment/paper, ink types, illuminations, and binding.
2. **Condition Assessment**: Evaluate all damage (tears, ink fading, water damage, mold, binding issues).
3. **Conservation Priority**: Prioritize interventions based on urgency and risk.
4. **Treatment Plan**: Detailed restoration process for pages, illuminations, and binding.
5. **Cleaning Methods**: Safe techniques for removing dirt and stains without damaging ink or illuminations.
6. **Repair Techniques**: Methods for mending tears, reinforcing pages, and stabilizing the binding.
7. **Illumination Preservation**: Special care for gold leaf and colored illuminations.
8. **Digitization Recommendations**: Guidance for safe digitization to reduce handling.
9. **Storage Environment**: Optimal conditions for long-term preservation.

Handle with reverence and historical sensitivity."""
    },
    "expressionist_abstract": {
        "name": "🎨 Expressionist & Abstract Art Restoration",
        "icon": "🎨",
        "description": "Restore modern and abstract artworks with contemporary techniques",
        "prompt_template": """You are an expert conservator specializing in modern and contemporary art, particularly Expressionist and Abstract works.

Art Style: {style}
Period: {period}
Medium: {medium}
Damage Description: {damage}

Please provide:
1. **Artistic Intent**: Consider the artist's original intent and techniques (impasto, dripping, collage, etc.).
2. **Material Analysis**: Assess modern materials (acrylics, mixed media, unconventional materials).
3. **Condition Report**: Evaluate damage specific to modern art (texture loss, cracking, fading, surface issues).
4. **Conservation Approach**: Balance preservation with respecting the artist's intent and materials.
5. **Technical Challenges**: Address issues unique to modern materials and techniques.
6. **Surface Treatment**: Methods for cleaning and stabilizing while preserving texture and finish.
7. **Color Matching**: Techniques for matching modern pigments and surface qualities.
8. **Ethical Considerations**: When to restore vs. when to preserve as-is.

Be innovative while respecting the artwork's integrity."""
    },
    "fresco_mural": {
        "name": "🏛️ Fresco & Mural Restoration",
        "icon": "🏛️",
        "description": "Restore wall paintings and frescoes with specialized techniques",
        "prompt_template": """You are an expert fresco and mural conservator.

Fresco Type: {fresco_type}
Period: {period}
Location: {location}
Damage Description: {damage}

Please provide:
1. **Technical Analysis**: Assess the fresco technique (buon fresco, secco, mixed) and wall substrate.
2. **Damage Assessment**: Evaluate issues like detachment, water damage, salt efflorescence, paint loss, biological growth.
3. **Structural Evaluation**: Check wall stability and moisture problems.
4. **Conservation Strategy**: Detailed plan for cleaning, consolidation, and reattachment.
5. **Consolidation Methods**: Techniques for stabilizing flaking or detaching paint layers.
6. **Desalination**: Processes for removing harmful salts if present.
7. **Retouching Approach**: Guidelines for integrating losses while respecting the original.
8. **Environmental Control**: Address humidity, water infiltration, and climate issues.
9. **Long-term Monitoring**: Plan for ongoing assessment and maintenance.

Focus on both immediate and long-term preservation."""
    },
    "asian_scroll": {
        "name": "🎋 Asian Scroll & Screen Restoration",
        "icon": "🎋",
        "description": "Preserve East Asian scrolls, screens, and paintings",
        "prompt_template": """You are an expert conservator specializing in East Asian paintings, scrolls, and screens.

Origin: {origin}
Style: {style}
Period: {period}
Damage Description: {damage}

Please provide:
1. **Cultural Context**: Explain the artwork's cultural significance and traditional techniques.
2. **Material Analysis**: Assess silk, paper, mounting materials, and inks used.
3. **Condition Assessment**: Evaluate damage (tears, water stains, detached mounting, foxing, insect damage).
4. **Traditional Techniques**: Incorporate traditional Asian conservation methods (remounting, lining).
5. **Conservation Plan**: Step-by-step process respecting Eastern conservation philosophies.
6. **Remounting Strategy**: If needed, plan for traditional remounting techniques.
7. **Ink & Color Preservation**: Special care for delicate inks and pigments.
8. **Handling & Storage**: Traditional methods for rolling, storing, and displaying scrolls.
9. **Humidity Control**: Critical environmental guidelines for Asian artworks.

Be culturally informed and technically precise."""
    },
    "icon_religious": {
        "name": "✝️ Icon & Religious Art Conservation",
        "icon": "✝️",
        "description": "Restore religious icons with reverence and traditional methods",
        "prompt_template": """You are an expert conservator specializing in religious icons and sacred art.

Religious Tradition: {tradition}
Period: {period}
Panel Type: {panel_type}
Damage Description: {damage}

Please provide:
1. **Theological Significance**: Acknowledge the sacred nature and theological importance of the icon.
2. **Technical Analysis**: Assess the panel, gesso layer, tempera paint, and any gilding.
3. **Condition Report**: Evaluate cracks, flaking paint, darkened varnish, losses, structural issues.
4. **Conservation Philosophy**: Balance reverence with necessary interventions.
5. **Treatment Plan**: Detailed restoration process including cleaning, consolidation, and retouching.
6. **Varnish Removal**: Safe methods for removing darkened varnish layers.
7. **Gilding Restoration**: Techniques for repairing or stabilizing gold leaf.
8. **Retouching Ethics**: Guidelines for minimal, reversible interventions.
9. **Blessing & Ritual**: Acknowledge any religious protocols for handling sacred objects.

Approach with reverence and cultural sensitivity."""
    },
    "photography_restoration": {
        "name": "📸 Historic Photography Restoration",
        "icon": "📸",
        "description": "Restore and preserve vintage photographs and prints",
        "prompt_template": """You are an expert photograph conservator specializing in historic photographic processes.

Photographic Process: {process}
Period: {period}
Damage Description: {damage}

Please provide:
1. **Process Identification**: Explain the specific photographic process and its characteristics.
2. **Chemical Analysis**: Assess the chemical stability and deterioration patterns.
3. **Condition Assessment**: Evaluate fading, tears, foxing, silver mirroring, vinegar syndrome, etc.
4. **Conservation Approach**: Detailed plan specific to the photographic process.
5. **Stabilization Methods**: Techniques for halting chemical deterioration.
6. **Cleaning Techniques**: Safe methods for removing surface dirt and stains.
7. **Repair Strategies**: Approaches for mending tears and reinforcing fragile areas.
8. **Digitization**: Guidelines for creating digital surrogates.
9. **Storage Environment**: Optimal conditions for photographic materials.
10. **Handling Protocols**: Safe handling to prevent further damage.

Be process-specific and chemistry-aware."""
    },
    "pottery_ceramic": {
        "name": "🏺 Pottery & Ceramic Restoration",
        "icon": "🏺",
        "description": "Restore ceramic vessels, pottery, and clay artworks",
        "prompt_template": """You are an expert ceramics conservator specializing in pottery and ceramic artifacts.

Ceramic Type: {ceramic_type}
Period/Culture: {period}
Glaze Type: {glaze}
Damage Description: {damage}

Please provide:
1. **Archaeological Context**: If applicable, consider the artifact's archaeological or cultural significance.
2. **Material Analysis**: Assess the clay body, firing technique, and glaze composition.
3. **Condition Report**: Evaluate cracks, missing pieces, glaze loss, staining, previous repairs.
4. **Conservation Plan**: Step-by-step process for cleaning, bonding, filling, and surface treatment.
5. **Cleaning Methods**: Appropriate techniques for removing dirt, salts, and old adhesives.
6. **Bonding Strategy**: Recommend adhesives and techniques for rejoining fragments.
7. **Gap Filling**: Methods for filling losses and achieving proper contours.
8. **Surface Integration**: Techniques for matching glaze, color, and texture.
9. **Reversibility**: Ensure treatments can be reversed if needed in the future.
10. **Support & Display**: Recommendations for safe mounting and display.

Balance completeness with historical integrity."""
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
                artist = st.text_input("🎨 Artist/Region", placeholder="e.g., Leonardo da Vinci, Florentine School, Venetian")
                period = st.text_input("📅 Period", placeholder="e.g., Early Renaissance (1400-1490), High Renaissance")
                medium = st.selectbox("🖌️ Medium", ["Egg Tempera on Wood", "Oil on Canvas", "Fresco", "Mixed Tempera and Oil"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe condition issues, paint flaking, wood panel damage...")
                input_data = {"artist": artist, "period": period, "medium": medium, "damage": damage}

            elif st.session_state.selected_feature == "mughal_miniature":
                school = st.selectbox("🏛️ School/Period", ["Akbar Period", "Jahangir Period", "Shah Jahan Period", "Aurangzeb Period", "Later Mughal", "Provincial Mughal"])
                subject = st.text_input("🎭 Subject Matter", placeholder="e.g., Court scene, Battle, Portrait, Garden, Religious")
                material = st.selectbox("📜 Base Material", ["Paper (Wasli)", "Ivory", "Vellum", "Cloth"])
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe pigment loss, paper tears, gold work damage, binding issues...")
                input_data = {"school": school, "subject": subject, "material": material, "damage": damage}

            elif st.session_state.selected_feature == "sculpture_3d":
                sculpture_type = st.selectbox("🗿 Sculpture Type", ["Statue", "Bust", "Relief", "Architectural Element", "Figurine", "Monument"])
                material = st.selectbox("🪨 Material", ["Marble", "Bronze", "Wood", "Stone (Limestone/Sandstone)", "Terracotta", "Plaster", "Mixed Materials"])
                period = st.text_input("📅 Period/Style", placeholder="e.g., Classical Greek, Roman, Gothic, Baroque, Modern")
                damage = st.text_area("⚠️ Damage Description", placeholder="Describe breaks, missing parts, surface erosion, patina loss, structural issues...")
                input_data = {"sculpture_type": sculpture_type, "material": material, "period": period, "damage": damage}

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

                            # Updated API call for new google-genai package
                            response = client.models.generate_content(
                                model='gemini-1.5-flash',
                                contents=prompt,
                                config={
                                    'temperature': temperature,
                                    'max_output_tokens': 2000,
                                }
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
                            st.info("💡 Tip: Make sure your GEMINI_API_KEY is valid in .streamlit/secrets.toml")
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
        through AI-generated restoration guidance using Google Gemini 1.5 Flash.</p>
    </div>

    <div class="info-card">
        <h3>✨ Key Features</h3>
        <ul>
            <li>12 specialized restoration tools for different art forms</li>
            <li>Period-specific and culturally accurate recommendations</li>
            <li>Adjustable creativity level for different restoration needs</li>
            <li>Dark mode and light mode support</li>
            <li>Restoration history tracking</li>
            <li>AI-powered using Google Gemini 1.5 Flash</li>
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
        <p><strong>AI Model:</strong> Google Gemini 1.5 Flash</p>
        <p><strong>Framework:</strong> Streamlit</p>
        <p><strong>Language:</strong> Python</p>
        <p><strong>Purpose:</strong> Educational & Professional Art Conservation Support</p>
    </div>
    """, unsafe_allow_html=True)
