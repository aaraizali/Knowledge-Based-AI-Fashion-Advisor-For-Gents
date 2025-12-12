import streamlit as st
from advisor import get_recommendation

# ---------------------------
# Page Config & Styling
# ---------------------------
st.set_page_config(page_title="Knowledge-Based Fashion Advisor", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f4f8, #e0eaf1);
    font-family: 'Segoe UI', sans-serif;
    color: #333333;
}
.hero-section {
    background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
    padding: 36px;
    border-radius: 18px;
    text-align: center;
    color: #ffffff;
    margin-bottom: 24px;
}
.outfit-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    transition: transform 0.25s, box-shadow 0.25s;
}
.outfit-card:hover { transform: translateY(-6px); box-shadow: 0 12px 24px rgba(0,0,0,0.12); }

.top-outfit-card {
    background: linear-gradient(135deg, #fff3cc, #ffe066);
    border: 3px solid #ffbf00;
    box-shadow: 0 0 20px rgba(255, 191, 0, 0.7);
    transform: scale(1.03);
}
.top-outfit-card:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(255, 191, 0, 0.9);
}

.badge { padding:6px 10px; border-radius:8px; font-weight:600; color:#fff; }
.top-badge { background: linear-gradient(90deg,#1f77b4,#3fa2ff); }
.bottom-badge { background: linear-gradient(90deg,#ffbf00,#ffd633); color:#222; }
.shoes-badge { background: linear-gradient(90deg,#8b4513,#a0522d); }
.accessories-badge { background: linear-gradient(90deg,#6a0dad,#9b30ff); }

.rule-pill { background:#eef2ff; padding:6px 10px; border-radius:999px; margin-right:6px; color:#1f3c88; font-weight:600; }
.score { font-weight:700; color:#333; background:#f7f7f7; padding:6px 10px; border-radius:8px; }

.footer { text-align:center; color:#666; margin-top:30px; padding:10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <h1>👔 Knowledge-Based Fashion Advisor</h1>
    <p>Rule-based outfit recommendations (no AI/ML) — clear rules, deterministic results.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# User Input Section
# ---------------------------
with st.expander("Select Your Preferences", expanded=True):
    weather = st.selectbox("Weather", ["hot", "mild", "cold"])
    occasion = st.selectbox("Occasion", ["formal", "casual", "party"])
    body_type = st.selectbox("Body Type", ["athletic", "slim", "heavy"])
    style = st.selectbox("Style Preference", ["Classic", "Sporty", "Trendy"])
    preferred_colors = st.multiselect(
        "Preferred Colors",
        ["White", "Black", "Brown", "Navy", "Light Blue", "Khaki", "Grey", "Olive"]
    )

# ---------------------------
# Helper: Convert score to stars & label
# ---------------------------
def score_to_label(score):
    if score >= 9:
        return "⭐⭐⭐⭐⭐ Excellent Match"
    elif score >= 6:
        return "⭐⭐⭐ Good Match"
    elif score >= 3:
        return "⭐⭐ Fair Match"
    else:
        return "⭐ Poor Match"

# ---------------------------
# Get Recommendations
# ---------------------------
if st.button("Get Recommendations"):
    outfits = get_recommendation(weather, occasion, body_type, style, preferred_colors)
    st.write("")  # spacing

    if not outfits:
        st.warning("No recommendations found for your input.")
    else:
        for idx, outfit in enumerate(outfits):
            # Highlight top outfit
            card_class = "top-outfit-card" if idx == 0 else "outfit-card"
            st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)

            # Friendly score
            friendly_score = score_to_label(outfit.get('score', 0))
            if idx == 0:
                st.markdown(f"### ✨ Outfit Option {idx+1}  &nbsp;&nbsp; 🏆 Top Pick! &nbsp;&nbsp; <span class='score'>{friendly_score}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"### ✨ Outfit Option {idx+1}  &nbsp;&nbsp; <span class='score'>{friendly_score}</span>", unsafe_allow_html=True)

            # Display outfit items
            col1, col2, col3, col4 = st.columns([3,3,2,2])
            col1.markdown(f"<div class='badge top-badge'>👕 {outfit.get('top','N/A')}</div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='badge bottom-badge'>👖 {outfit.get('bottom','N/A')}</div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='badge shoes-badge'>👞 {outfit.get('shoes','N/A')}</div>", unsafe_allow_html=True)
            col4.markdown(f"<div class='badge accessories-badge'>👜 {outfit.get('accessories','N/A')}</div>", unsafe_allow_html=True)

            # Show colors
            colors = outfit.get('colors', [])
            st.markdown(f"**Colors:** {', '.join(colors) if colors else 'N/A'}")

            # Friendly reasoning
            reasoning = outfit.get('reasoning', [])
            applied_rules = outfit.get('fired', [])
            if reasoning or applied_rules:
                with st.expander("Why this outfit? (Friendly Explanation)"):
                    for r in reasoning:
                        msg = ""
                        if "weather matches" in r:
                            msg = f"This outfit is suitable for {weather} weather."
                        elif "occasion matches" in r:
                            msg = f"Perfect for your {occasion} occasion."
                        elif "body type matches" in r:
                            msg = f"It complements your {body_type} body type."
                        elif "style preference matches" in r:
                            msg = f"It matches your {style} style preference."
                        elif "preferred colors matched" in r:
                            matched_colors = [c for c in preferred_colors if c.lower() in r.lower()]
                            if matched_colors:
                                msg = f"Your preferred color(s) {', '.join(matched_colors)} match this outfit."
                        elif "shorts are not suitable" in r.lower():
                            msg = "Shorts are not suitable for a formal occasion."

                        if not msg:
                            msg = r
                        st.write(f"- {msg}")

                    if applied_rules:
                        st.markdown("**Matched Rules (internal codes):** " + ", ".join(applied_rules))

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div class='footer'>Made by <strong>Aaraiz Ali</strong> &nbsp;|&nbsp; Group: Aaraiz Ali, Muhammad Khizer</div>", unsafe_allow_html=True)
