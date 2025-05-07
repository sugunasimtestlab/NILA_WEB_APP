
# NILA Herbal Hair Oil - Booking Web App (Streamlit)
# To run this app: streamlit run nila_web_app.py

import streamlit as st
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(page_title="NILA Products Booking", page_icon="🌿")


# Show banner image correctly
st.image("NILA Herbal Banner.png", caption="Explore Our Herbal Collection 🌿", use_container_width=True)

# Correct image path handling for products
products = {
    "NILA Herbal Hair Oil 100ml": {
        "price": 199,
        "image": "Nila_oil_bottle.png",
        "ingredients": "Hibiscus, Amla, Curry Leaves,Fenugreek, Neem, Almond, Aloe Vera, Bhringraj, Holy Basil, Indian Nettle,Ect....",
        "benefits": "Reduces Hair Fall, Promotes Hair Growth, Nourishes Scalp, Strengthens Hair Roots"
    },
    "NILA Herbal Hair Pack 50g": {
        "price": 99,
        "image": "Nila_hairpack.png",
        "ingredients": "Amla Powder, Hibiscus Powder, Neem Powder, Rose Petals",
        "benefits": "Cleanses Scalp, Controls Dandruff,Strengthens Roots"
    }
}

# --- Product Catalog Preview ---
st.markdown("### 🌿 Our Products")
for product_name, details in products.items():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(details["image"], use_container_width=True)
    with col2:
        st.markdown(f"**{product_name}**")
        st.markdown(f"💰 **Price:** ₹{details['price']}")
        st.markdown(f"🌿 **Ingredients:** {details.get('ingredients', 'Details coming soon')}")
        st.markdown(f"✨ **Benefits:** {details.get('benefits', 'Details coming soon')}")
        st.markdown("---")


# --- Product Selection ---
st.markdown("🛍️ Choose your product(s) below and place your order:")
selected_products = st.multiselect("Select Product Categories", list(products.keys()))

# Dictionary to store selected product quantities
selected_quantities = {}
total_price = 0

if selected_products:
    st.header("🧾 Selected Products & Quantity")
    for product in selected_products:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.image(products[product]["image"], caption=product, use_container_width=True)
        with col2:
            qty = st.number_input(f"Quantity for {product}", min_value=1, max_value=10, step=1, key=product)
            selected_quantities[product] = qty
            total_price += qty * products[product]["price"]

else:
    st.info("Please select at least one product category to proceed.")

# --- Order Form ---
st.header("📦 Delivery Details")

name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address (optional)")
address = st.text_area("Delivery Address")

payment_method = st.radio("Payment Method", ["Cash on Delivery", "UPI Payment"])
payment_screenshot = None
if payment_method == "UPI Payment":
    payment_screenshot = st.file_uploader("📎 Upload UPI Payment Screenshot (JPG/PNG)", type=["jpg", "jpeg", "png"])

st.markdown(f"💰 **Total Amount:** ₹{total_price}** ")
st.markdown("💳 **UPI ID for Payment:** `sugunasundarajothi@okhdfcbank`")

email_user = st.secrets["general"]["email_user"]
email_password = st.secrets["general"]["email_password"]
# Email sending function
def send_order_email(name, phone, email, address, order_summary, total_price, payment_method):
    sender_email = email_user
    sender_password = email_password  
    receiver_email = "suguna.sundarajothi@outlook.com"

    subject = "New NILA Product Order Received"
    body = f"""
    New order received:

    Name: {name}
    Phone: {phone}
    Email: {email if email else 'sugunasundarajothi@gmail.com'}
    Address: {address}
    Products Ordered:
    {order_summary}
    
    Total Price: ₹{total_price}
    Payment Method: {payment_method}
    """

    message = MIMEMultipart()
    message["From"] = email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Place Order Button
if st.button("Place Order"):
    if not selected_products:
        st.error("❗ Please select at least one product.")
    elif name and phone and address:
        if payment_method == "UPI Payment" and payment_screenshot is None:
            st.error("❗ Please upload a payment screenshot for UPI Payment.")
        else:
            # Generate order summary
            order_summary = ""
            for product, qty in selected_quantities.items():
                price = products[product]["price"]
                subtotal = qty * price
                order_summary += f"{product} x {qty} = ₹{subtotal}\n"
            
            send_order_email(name, phone, email, address, order_summary, total_price, payment_method)
            st.success("✅ Your order has been placed successfully!")
            st.markdown("### Order Summary:")
            st.text(order_summary)
            st.markdown(f"**Name:** {name}")
            st.markdown(f"**Phone:** {phone}")
            if email:
                st.markdown(f"**Email:** {email}")
            st.markdown(f"**Address:** {address}")
            st.markdown(f"**Total Price:** ₹{total_price}")
            st.markdown(f"**Payment Method:** {payment_method}")
            if payment_screenshot:
                st.image(payment_screenshot, caption="Payment Screenshot", use_column_width=True)
            st.markdown("📦 Your order will be confirmed shortly via WhatsApp or call.")
    else:
        st.error("❗ Please fill all required fields to place an order.")

# Footer
st.markdown("---")
st.markdown("📸 Follow us on [Instagram](https://instagram.com/nila_herbal_hairoil)")
st.markdown("📸 Support [Instagram](https://instagram.com/queen_of_hills_queenpapa)")
st.markdown("📞 For inquiries, call us at: +91 8344987196")
st.markdown("🌿 Experience the power of nature with NILA Herbal Hair Oil!")
