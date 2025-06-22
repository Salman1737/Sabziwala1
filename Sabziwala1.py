from datetime import datetime
import random
import urllib.parse
import streamlit as st

# App Configuration
st.set_page_config(page_title="Sabziwala", page_icon="🥦", layout="centered")

# CSS Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #27ae60;
        padding-top: 10px;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #e74c3c;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: bold;
        font-size: 1.05rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header: Logo + Title
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("sabziwala_logo.png", width=100)
with col_title:
    st.markdown('<div class="main-title">Sabziwala 🥕🥔🍅</div>', unsafe_allow_html=True)

st.markdown('<div class="subtitle">(Currently, services are offered in Lahore only 🚚)</div>', unsafe_allow_html=True)

# Session State Initialization
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "cart" not in st.session_state:
    st.session_state.cart = {
        "🍅 Tomato": 0,
        "🧅 Onion": 0,
        "🥔 Potato": 0
    }
if "order_id" not in st.session_state:
    st.session_state.order_id = f"SW{random.randint(1000, 9999)}"

# Vegetable Prices
prices = {
    "🍅 Tomato": 80,
    "🧅 Onion": 60,
    "🥔 Potato": 60
}

# Tabs
tab1, tab2 = st.tabs(["📝 Customer Info", "🛒 Products & Order"])

# Tab 1: Customer Info
with tab1:
    st.subheader("👤 Enter your details:")
    name = st.text_input("Name")
    address = st.text_area("Address")
    contact = st.text_input("Contact Number (e.g., 03XXXXXXXXX)")

    if st.button("✅ Submit & Proceed"):
        if not name or not address or not contact:
            st.warning("Please fill in all fields.")
        else:
            st.session_state.name = name
            st.session_state.address = address
            st.session_state.contact = contact
            st.session_state.submitted = True
            st.success("Information saved. Go to 'Products & Order' tab.")

# Tab 2: Product Selection & Order
with tab2:
    if not st.session_state.submitted:
        st.info("👉 Please submit your information first in the 'Customer Info' tab.")
    else:
        st.subheader("🧺 Select quantity of vegetables:")
        for item in st.session_state.cart:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{item}** — Rs. {prices[item]}/Kg")
            with col2:
                if st.button("➖", key=f"{item}-minus"):
                    if st.session_state.cart[item] > 0:
                        st.session_state.cart[item] -= 1
            with col3:
                if st.button("➕", key=f"{item}-plus"):
                    st.session_state.cart[item] += 1
            st.write(f"**Quantity:** {st.session_state.cart[item]} Kg")

        st.divider()
        st.subheader("🧾 Order Summary")
        total = 0
        summary_lines = ""

        for item, qty in st.session_state.cart.items():
            if qty > 0:
                amount = qty * prices[item]
                total += amount
                summary_lines += f"🔹 {item}: {qty} Kg — Rs. {amount}\n"

        if summary_lines:
            st.text(summary_lines)
            st.markdown(f"**💰 Total: Rs. {total}**")

            payment_method = st.selectbox("💳 Payment Method", ["Cash on Delivery", "Bank Transfer", "Online Payment"])

            if st.button("📦 Order via WhatsApp"):
                message = (
                    "📦 *I want to place my following order with Sabziwala:*\n\n"
                    f"🆔 *Order ID:* {st.session_state.order_id}\n"
                    f"👤 *Customer:* {st.session_state.name}\n"
                    f"📍 *Address:* {st.session_state.address}\n"
                    f"📞 *Contact:* {st.session_state.contact}\n"
                    f"📅 *Date:* {datetime.now().strftime('%Y-%m-%d')}\n\n"
                    f"🧾 *Order Summary:*\n{summary_lines}\n"
                    f"💰 *Total Amount:* Rs. {total}\n"
                    f"💳 *Payment Method:* {payment_method}"
                )
                encoded = urllib.parse.quote(message)
                whatsapp_url = f"https://wa.me/923034123570?text={encoded}"
                st.markdown(f"[👉 Click to Send WhatsApp Order]({whatsapp_url})", unsafe_allow_html=True)
                st.success("✅ Order message prepared. Please send it via WhatsApp.")
        else:
            st.warning("⚠️ Please select at least one item to generate order summary.")
