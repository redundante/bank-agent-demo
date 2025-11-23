import streamlit as st
import time
import re
import textwrap 

# --- CONFIGURATION & CSS (SAME AS BEFORE) ---

# [CSS BLOCK REMAINS UNCHANGED]

st.markdown("""
<style>
    /* ... (CSS block is unchanged, hidden for brevity) ... */
    .stApp {
        background-color: #343541;
        color: #ECECF1;
        font-family: 'Söhne', 'ui-sans-serif', system-ui, -apple-system, sans-serif;
    }
    /* ... */
</style>
""", unsafe_allow_html=True)

# --- LOGIC & SESSION STATE (SAME AS BEFORE) ---
# [Logic and Session State setup remains unchanged, hidden for brevity]

def get_zinia_decision(query, price):
    query_lower = query.lower()
    if any(w in query_lower for w in ["laptop", "macbook", "flight", "course", "hotel"]):
        return True, "Safe"
    elif any(w in query_lower for w in ["casino", "bet", "crypto"]):
        return False, "High Risk"
    return True, "General"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI: SIDEBAR (SAME AS BEFORE) ---
with st.sidebar:
    st.markdown("### ChatGPT 4o")
    st.markdown("---")
    st.success("✅ **Zinia Plugin Active**")
    st.caption("Connected to Zinia Credit Engine via MCP Protocol.")
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT HISTORY RENDERER (FIXED) ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        # If the message is marked as a widget, we MUST use st.markdown(..., unsafe_allow_html=True)
        # Otherwise, use st.write for safe text display.
        if msg.get("type") == "zinia_widget":
            st.markdown(msg["content"], unsafe_allow_html=True) 
        else:
            st.write(msg["content"])

# --- INPUT LOOP (FIXED) ---
if prompt := st.chat_input("Ask ChatGPT to buy something..."):
    
    # 1. User Message (Unchanged)
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # 2. Assistant Response (Processing)
    with st.chat_message("assistant", avatar="✨"):
        status = st.empty()
        status.markdown("`Contacting Zinia...`")
        time.sleep(1.0)
        status.empty()

        # Parse Price (Unchanged)
        try:
            price_match = re.search(r'\d+', prompt)
            price = float(price_match.group()) if price_match else 1200.00
        except:
            price = 1200.00

        approved, risk_class = get_zinia_decision(prompt, price)

        if approved:
            intro = "I've generated a financing offer using your linked Zinia account."
            
            # 2a. Display Intro Text Immediately
            st.write(intro)
            
            # 2b. Generate HTML (dedented)
            installment = price / 3
            logo_url = "https://www.zinia.com/assets/logo_topbar/ZiniaBySantanderTopbarCustomer.svg"
            
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
            
            # 2c. Display Widget HTML Immediately (FIXED: Ensure the flag is here)
            st.markdown(zinia_html, unsafe_allow_html=True)
            
            # 3. Save History: Save the text and the widget separately.
            st.session_state.messages.append({"role": "assistant", "content": intro, "avatar": "✨", "type": "text"})
            st.session_state.messages.append({"role": "assistant", "content": zinia_html, "type": "zinia_widget", "avatar": "✨"})
        
        else:
            decline = "Transaction declined by Zinia risk engine."
            st.write(decline)
            st.session_state.messages.append({"role": "assistant", "content": decline, "avatar": "✨", "type": "text"})
