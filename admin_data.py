# admin_dashboard.py

import streamlit as st
from db_utils import fetch_all_orders
from datetime import datetime
import pandas as pd

# Set page config
st.set_page_config(page_title="NILA Admin Dashboard", page_icon="📦", layout="wide")

# Title
st.title("📦 NILA Admin Dashboard")
st.markdown("Manage and review all incoming orders from customers.")

# Fetch all orders from DB
orders = fetch_all_orders()

if not orders:
    st.warning("No orders found.")
else:
    # Show summary
    st.success(f"📊 Total Orders: {len(orders)}")

    # --- TABLE FORMAT ---
    columns = [
        "Order ID", "Timestamp", "Name", "Phone", "Email", "Address",
        "Products", "Total Price", "Payment Method", "Payment Status"
    ]
    df = pd.DataFrame(orders, columns=columns)
    st.subheader("📋 All Orders (Table View)")
    st.dataframe(df, use_container_width=True)

    # --- OLD FORMAT (EXPANDERS) ---
    st.subheader("🧾 Detailed Orders (Expanders)")
    for order in orders:
        order_id, timestamp, name, phone, email, address, products, total_price, payment_method = order[:9]
        with st.expander(f"🧾 Order #{order_id} - {name} - ₹{total_price} - {payment_method}"):
            st.markdown(f"**🕒 Date:** {datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"**📞 Phone:** {phone}")
            st.markdown(f"**📧 Email:** {email if email else 'N/A'}")
            st.markdown(f"**🏠 Address:** {address}")
            st.markdown("**📦 Products Ordered:**")
            st.text(products)
            st.markdown(f"**💰 Total Amount:** ₹{total_price}")
            st.markdown(f"**💳 Payment Method:** {payment_method}")
