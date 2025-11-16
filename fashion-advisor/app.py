import streamlit as st
from advisor import get_recommendation

st.set_page_config(page_title="AI Fashion Advisor", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f4f8, #e0eaf1);
    font-family: 'Segoe UI', sans-serif;
    color: #333333;
}
.hero-section {
    background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    color: #ffffff;
    margin-bottom: 30px;
    animation: heroFade 1s ease-in-out;
}
.hero-section h1 { font-size: 48px; margin-bottom: 10px; animation: slideDown 1s ease-in-out; }
.hero-section p { font-size: 18px; animation: slideUp 1s ease-in-out; }

@keyframes heroFade { 0% { opacity: 0; } 100% { opacity: 1; } }
@keyframes slideDown { 0% { transform: translateY(-30px); opacity:0; } 100% { transform: translateY(0); opacity:1; } }
@keyframes slideUp { 0% { transform: translateY(30px); opacity:0; } 100% { transform: translateY(0); opacity:1; } }

.outfit-card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    margin-bottom: 30px;
    transition: transform 0.3s, box-shadow 0.3s;
    opacity: 0;
    animation: fadeInCard 0.6s forwards;
}
.outfit-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 16px 30px rgba(0,0,0,0.2);
}

@keyframes fadeInCard { to { opacity: 1; } }

.top-badge { 
    background: linear-gradient(135deg, #1f77b4, #3fa2ff); 
    color: white; padding: 6px 12px; border-radius: 6px; font-weight:bold; 
    transition: box-shadow 0.3s, transform 0.3s;
}
.top-badge:hover { box-shadow: 0 0 12px #3fa2ff; transform: scale(1.1); }

.bottom-badge { 
    background: linear-gradient(135deg, #ffbf00, #ffd633); 
    color: black; padding: 6px 12px; border-radius: 6px; font-weight:bold; 
    transition: box-shadow 0.3s, transform 0.3s;
}
.bottom-badge:hover { box-shadow: 0 0 12px #ffd633; transform: scale(1.1); }

.shoes-badge { 
    background: linear-gradient(135deg, #8b4513, #a0522d); 
    color: white; padding: 6px 12px; border-radius: 6px; font-weight:bold; 
    transition: box-shadow 0.3s, transform 0.3s;
}
.shoes-badge:hover { box-shadow: 0 0 12px #a0522d; transform: scale(1.1); }

.color-circle {
    display: inline-block;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-right: 5px;
    border: 1px solid #ccc;
    animation: pulseRotate 1.5s infinite alternate;
    transition: transform 0.3s;
}
.color-circle:hover { transform: scale(1.3) rotate(10deg); }

@keyframes pulseRotate {
    0% { transform: scale(1) rotate(0deg); opacity: 0.8; }
    100% { transform: scale(1.2) rotate(5deg); opacity: 1; }
}

.stExpanderHeader { color: #333333; font-weight: bold; }

.footer {
    text-align: center;
    padding: 20px;
    color: #555555;
    font-size: 14px;
    margin-top: 50px;
    animation: fadeInFooter 2s ease-in-out;
}
@keyframes fadeInFooter {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <h1>👔 AI Fashion Advisor</h1>
    <p>Get stylish, professional outfit recommendations tailored for you!</p>
</div>
""", unsafe_allow_html=True)

with st.expander("Select Your Preferences", expanded=True):
    weather = st.selectbox("🌡 Weather:", ["hot", "mild", "cold"])
    occasion = st.selectbox("🎉 Occasion:", ["formal", "casual", "party"])
    body_type = st.selectbox("💪 Body Type:", ["athletic", "slim", "heavy"])
    style = st.selectbox("✨ Style Preference:", ["Classic", "Sporty", "Trendy"])
    preferred_colors = st.multiselect("🎨 Preferred Colors:", ["Red", "Blue", "Green", "Black", "White", "Brown", "Grey"])

if st.button("Get Recommendations"):
    outfits = get_recommendation(weather, occasion, body_type, style, preferred_colors)

    for idx, outfit in enumerate(outfits):
        st.markdown(f"<div class='outfit-card' style='animation-delay: {idx*0.2}s'>", unsafe_allow_html=True)
        st.markdown(f"### 🌟 Outfit Option {idx+1}")

        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<span class='top-badge'>👕 {outfit['Top']}</span>", unsafe_allow_html=True)
        col2.markdown(f"<span class='bottom-badge'>👖 {outfit['Bottom']}</span>", unsafe_allow_html=True)
        col3.markdown(f"<span class='shoes-badge'>👞 {outfit['Shoes']}</span>", unsafe_allow_html=True)

        if "Occasion Add-on" in outfit:
            st.markdown(f"**🎩 Add-on:** {outfit['Occasion Add-on']}")
        if "Occasion Shoes" in outfit:
            st.markdown(f"**👟 Occasion Shoes:** {outfit['Occasion Shoes']}")
        if "Fit Advice" in outfit:
            st.markdown(f"**💡 Fit Advice:** {outfit['Fit Advice']}")

        if preferred_colors:
            st.markdown("**Preferred Colors:** " + " ".join(
                [f"<span class='color-circle' style='background-color:{c.lower()}'></span>" for c in preferred_colors]
            ), unsafe_allow_html=True)

        with st.expander("Why this outfit?"):
            for reason in outfit["reasoning"]:
                st.write(f"- {reason}")

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Made by <strong>Aaraiz Ali</strong> &copy; 2025
</div>
""", unsafe_allow_html=True)
