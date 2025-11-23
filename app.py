import streamlit as st
import time
import re

# --- CONFIGURATION ---
st.set_page_config(
    page_title="ChatGPT | Zinia Plugin",
    page_icon="🤖",
    layout="centered"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    /* --- 1. CHATGPT BASE THEME (Clean, Minimalist) --- */
    .stApp {
        background-color: #FFFFFF;
        color: #0d0d0d;
        font-family: 'Söhne', 'ui-sans-serif', 'system-ui', -apple-system, 'Segoe UI', Roboto, Ubuntu, Cantarell, 'Noto Sans', sans-serif, 'Helvetica Neue', Arial, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
    }
    
    /* Remove Streamlit Header/Footer clutter */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Chat Bubbles - ChatGPT Style (Minimal padding, no borders) */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Avatar Styling */
    .stChatMessage .st-emotion-cache-1p1m4ay {
        background-color: #19c37d !important; /* OpenAI Green */
        color: white !important;
    }

    /* --- 2. ZINIA BRANDED COMPONENT (The "Plugin" Result) --- */
    /* Only applied to the offer card */
    .zinia-wrapper {
        font-family: 'Inter', Helvetica, Arial, sans-serif;
        margin-top: 12px;
        margin-bottom: 24px;
        filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.08));
    }
    
    .zinia-card {
        background-color: #FFFFFF;
        border: 2px solid #000000; /* Zinia Bold Border */
        border-radius: 12px;
        overflow: hidden;
        color: #000000;
    }
    
    .zinia-header-strip {
        background-color: #000000;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .zinia-logo-text {
        color: #D4F718; /* Zinia Neon Green */
        font-weight: 900;
        font-size: 1.1rem;
        letter-spacing: -0.5px;
    }
    
    .zinia-badge {
        background-color: #D4F718;
        color: #000000;
        font-size: 0.7rem;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    
    .zinia-body {
        padding: 20px;
    }
    
    .zinia-amount {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 5px;
    }
    
    .zinia-subtext {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    
    /* The Selection Rows */
    .zinia-option-row {
        display: flex;
        align-items: center;
        padding: 12px;
        border: 1px solid #E5E5E5;
        border-radius: 8px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .zinia-option-row.selected {
        background-color: #FBFEEC; /* Light Green Tint */
        border-color: #D4F718;
        box-shadow: 0 0 0 1px #D4F718;
    }
    
    .zinia-radio {
        height: 18px;
        width: 18px;
        border: 2px solid #000000;
        border-radius: 50%;
        margin-right: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .zinia-radio.filled::after {
        content: '';
        width: 10px;
        height: 10px;
        background-color: #D4F718;
        border-radius: 50%;
    }
    
    .zinia-btn {
        display: block;
        width: 100%;
        background-color: #000000;
        color: #D4F718;
        font-weight: 700;
        text-align: center;
        padding: 14px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 15px;
        transition: transform 0.1s;
    }
    
    .zinia-btn:hover {
        transform: scale(1.01);
        color: #D4F718; /* ensure link color stays */
    }

</style>
""", unsafe_allow_html=True)

# --- MOCK RISK LOGIC ---
def get_zinia_decision(query, price):
    # Determine risk based on keywords
    query_lower = query.lower()
    if any(w in query_lower for w in ["laptop", "flight", "course", "work", "business"]):
        return True, "Safe"
    elif any(w in query_lower for w in ["casino", "bet", "crypto"]):
        return False, "High Risk"
    return True, "General" # Default approve

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI: SIDEBAR (Simulating ChatGPT Sidebar) ---
with st.sidebar:
    st.markdown("### ChatGPT 4o")
    st.markdown("---")
    st.markdown("**Active Plugins:**")
    st.info("✅ **Zinia Pay** (Enabled)")
    st.caption("Allows ChatGPT to offer real-time financing via your Zinia credit line.")

# --- UI: CHAT HISTORY ---
# We use standard Streamlit chat but it looks like GPT due to CSS
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        if msg.get("type") == "zinia_widget":
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            st.write(msg["content"])

# --- UI: INPUT LOOP ---
if prompt := st.chat_input("Message ChatGPT..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # 2. Assistant Response
    with st.chat_message("assistant", avatar="✨"):
        # A. Thinking Simulation
        status_placeholder = st.empty()
        status_placeholder.markdown("`Using Zinia Pay...`")
        time.sleep(1.0)
        status_placeholder.empty()

        # B. Parse Intent
        try:
            price_match = re.search(r'\d+', prompt)
            price = float(price_match.group()) if price_match else 900.00
        except:
            price = 900.00

        approved, risk_class = get_zinia_decision(prompt, price)

        # C. Generate Response
        if approved:
            # Intro Text
            intro_text = f"I've found that item. Since you have the **Zinia Plugin** enabled, I checked your eligibility. You are approved to finance this purchase immediately."
            st.write(intro_text)
            
            # THE ZINIA CARD (HTML/CSS Injection)
            installment = price / 3
            
            zinia_html = f"""
            <div class="zinia-wrapper">
                <div class="zinia-card">
                    <div class="zinia-header-strip">
                        <div class="zinia-logo-text">zinia</div>
                        <div class="zinia-badge">Pre-Approved</div>
                    </div>
                    <div class="zinia-body">
                        <div class="zinia-amount">€{price:,.2f}</div>
                        <div class="zinia-subtext">Total financing amount</div>
                        
                        <div class="zinia-option-row selected">
                            <div class="zinia-radio filled"></div>
                            <div style="flex-grow:1">
                                <div style="font-weight:700">Pay in 3 installments</div>
                                <div style="font-size:0.85rem; color:#555">0% APR • €{installment:,.2f} / month</div>
                            </div>
                        </div>

                        <div class="zinia-option-row">
                            <div class="zinia-radio"></div>
                            <div style="flex-grow:1">
                                <div style="font-weight:700">Pay in 30 days</div>
                                <div style="font-size:0.85rem; color:#555">Receive now, pay later</div>
                            </div>
                        </div>

                        <a href="#" class="zinia-btn">CONFIRM PURCHASE</a>
                    </div>
                </div>
            </div>
            """
            st.markdown(zinia_html, unsafe_allow_html=True)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": intro_text, "avatar": "✨"})
            st.session_state.messages.append({"role": "assistant", "content": zinia_html, "type": "zinia_widget", "avatar": "✨"})
        
        else:
            # Declined path
            decline_text = f"I checked with Zinia. Unfortunately, this transaction exceeds the risk parameters for the '{risk_class}' category."
            st.write(decline_text)
            st.session_state.messages.append({"role": "assistant", "content": decline_text, "avatar": "✨"})
