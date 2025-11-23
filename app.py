import streamlit as st
import time
import re
import textwrap # <--- NEW IMPORT TO FIX INDENTATION BUG

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Zinia Agent | Dark Mode",
    page_icon="💳",
    layout="centered"
)

# --- CSS STYLING (DARK MODE + ZINIA BRANDING) ---
st.markdown("""
<style>
    /* --- 1. CHATGPT DARK MODE THEME --- */
    .stApp {
        background-color: #343541;
        color: #ECECF1;
        font-family: 'Söhne', 'ui-sans-serif', system-ui, -apple-system, sans-serif;
    }
    
    /* Hide Default Headers */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #202123;
    }
    
    /* Input Styling */
    .stChatInput textarea {
        background-color: #40414F !important;
        color: white !important;
        border: 1px solid #565869 !important;
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Avatar Styling */
    .stChatMessage .st-emotion-cache-1p1m4ay {
        background-color: #19c37d !important;
        color: white !important;
    }

    /* --- 2. ZINIA ARTIFACT STYLING --- */
    .zinia-wrapper {
        font-family: 'Inter', Helvetica, Arial, sans-serif;
        margin-top: 15px;
        margin-bottom: 25px;
        filter: drop-shadow(0px 4px 12px rgba(0,0,0,0.4));
    }
    
    .zinia-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        overflow: hidden;
        color: #000000;
        max-width: 500px;
        border: 1px solid #444; /* Subtle border for dark mode contrast */
    }
    
    .zinia-header-strip {
        background-color: #FFFFFF;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid #F0F0F0;
    }
    
    .zinia-logo-img {
        height: 24px;
        width: auto;
    }
    
    .zinia-badge {
        background-color: #D4F718; /* Zinia Neon Green */
        color: #000000;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .zinia-body {
        padding: 24px;
    }
    
    .zinia-amount {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 6px;
        color: #000000;
        letter-spacing: -1px;
    }
    
    .zinia-subtext {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 24px;
    }
    
    .zinia-option-row {
        display: flex;
        align-items: center;
        padding: 16px;
        border: 1px solid #E5E5E5;
        border-radius: 10px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s;
        background-color: #FFFFFF;
    }
    
    .zinia-option-row:hover {
        border-color: #D4F718;
    }
    
    .zinia-option-row.selected {
        background-color: #FBFEEC;
        border: 2px solid #D4F718;
        box-shadow: 0 4px 10px rgba(212, 247, 24, 0.2);
    }
    
    .zinia-radio {
        height: 20px;
        width: 20px;
        border: 2px solid #000000;
        border-radius: 50%;
        margin-right: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .zinia-radio.filled::after {
        content: '';
        width: 12px;
        height: 12px;
        background-color: #D4F718;
        border-radius: 50%;
    }
    
    .zinia-btn {
        display: block;
        width: 100%;
        background-color: #000000;
        color: #D4F718 !important;
        font-weight: 700;
        text-align: center;
        padding: 16px;
        border-radius: 10px;
        text-decoration: none;
        margin-top: 20px;
        font-size: 1rem;
        transition: transform 0.1s;
    }
    
    .zinia-btn:hover {
        transform: scale(1.02);
        opacity: 0.95;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
def get_zinia_decision(query, price):
    query_lower = query.lower()
    if any(w in query_lower for w in ["laptop", "macbook", "flight", "course", "hotel"]):
        return True, "Safe"
    elif any(w in query_lower for w in ["casino", "bet", "crypto"]):
        return False, "High Risk"
    return True, "General"

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ChatGPT 4o")
    st.markdown("---")
    st.success("✅ **Zinia Plugin Active**")
    st.caption("Connected to Zinia Credit Engine via MCP Protocol.")
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT HISTORY RENDERER ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        if msg.get("type") == "zinia_widget":
            # CRITICAL FIX: Ensure unsafe_allow_html is True for history items too
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            st.write(msg["content"])

# --- INPUT LOOP ---
if prompt := st.chat_input("Ask ChatGPT to buy something..."):
    
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # 2. Assistant Response
    with st.chat_message("assistant", avatar="✨"):
        status = st.empty()
        status.markdown("`Contacting Zinia...`")
        time.sleep(1.0)
        status.empty()

        # Parse Price
        try:
            price_match = re.search(r'\d+', prompt)
            price = float(price_match.group()) if price_match else 1200.00
        except:
            price = 1200.00

        approved, risk_class = get_zinia_decision(prompt, price)

        if approved:
            intro = "I've generated a financing offer using your linked Zinia account."
            st.write(intro)
            
            # THE ZINIA ARTIFACT
            installment = price / 3
            logo_url = "https://www.zinia.com/assets/logo_topbar/ZiniaBySantanderTopbarCustomer.svg"
            
            # CRITICAL FIX: textwrap.dedent removes the indentation that confuses Markdown
            zinia_html = textwrap.dedent(f"""
                <div class="zinia-wrapper">
                    <div class="zinia-card">
                        <div class="zinia-header-strip">
                            <img src="{logo_url}" class="zinia-logo-img" alt="Zinia Logo">
                            <div class="zinia-badge">Approved</div>
                        </div>
                        <div class="zinia-body">
                            <div class="zinia-amount">€{price:,.2f}</div>
                            <div class="zinia-subtext">Total amount to finance</div>
                            
                            <div class="zinia-option-row selected">
                                <div class="zinia-radio filled"></div>
                                <div style="flex-grow:1">
                                    <div style="font-weight:700; color:black;">Pay in 3 installments</div>
                                    <div style="font-size:0.85rem; color:#555">0% APR • €{installment:,.2f} / month</div>
                                </div>
                            </div>

                            <div class="zinia-option-row">
                                <div class="zinia-radio"></div>
                                <div style="flex-grow:1">
                                    <div style="font-weight:700; color:black;">Pay in 30 days</div>
                                    <div style="font-size:0.85rem; color:#555">No interest if paid by next month</div>
                                </div>
                            </div>

                            <a href="#" class="zinia-btn">CONFIRM PURCHASE</a>
                        </div>
                    </div>
                </div>
            """)
            
            # Render Widget
            st.markdown(zinia_html, unsafe_allow_html=True)
            
            # Save History
            st.session_state.messages.append({"role": "assistant", "content": intro, "avatar": "✨"})
            st.session_state.messages.append({"role": "assistant", "content": zinia_html, "type": "zinia_widget", "avatar": "✨"})
        
        else:
            decline = "Transaction declined by Zinia risk engine."
            st.write(decline)
            st.session_state.messages.append({"role": "assistant", "content": decline, "avatar": "✨"})
