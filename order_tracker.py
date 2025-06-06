# order_tracker.py

import streamlit as st
from db_utils import fetch_all_orders

st.set_page_config(page_title="Track Your Order - NILA", page_icon="🔍")

st.title("🔍 Track Your NILA Order")
st.markdown("Enter your phone number or email address to find your recent order.")

# Input fields for search
search_input = st.text_input("📱 Enter your Phone Number or 📧 Email Address")

if search_input:
    # Fetch all orders
    orders = fetch_all_orders()

    # Filter orders by phone or email
    matched_orders = [
        order for order in orders
        if search_input in order[3] or (order[4] and search_input in order[4])
    ]

    if matched_orders:
        st.success(f"✅ Found {len(matched_orders)} order(s) for: {search_input}")

        for order in matched_orders:
            order_id, timestamp, name, phone, email, address, products, total_price, payment_method = order

            with st.expander(f"🧾 Order #{order_id} - ₹{total_price}"):
                st.markdown(f"**🕒 Order Date:** {timestamp}")
                st.markdown(f"**👤 Name:** {name}")
                st.markdown(f"**📞 Phone:** {phone}")
                if email:
                    st.markdown(f"**📧 Email:** {email}")
                st.markdown(f"**🏠 Address:** {address}")
                st.markdown(f"**📦 Products Ordered:**\n```\n{products}\n```")
                st.markdown(f"**💳 Payment Method:** {payment_method}")
                st.markdown(f"**💰 Total Price:** ₹{total_price}")
                st.markdown("🚚 *Your order is being processed. You will be contacted soon via phone/WhatsApp.*")
    else:
        st.warning("❌ No order found with that phone number or email. Please double-check and try again.")
else:
    st.info("Please enter your phone number or email to search.")
