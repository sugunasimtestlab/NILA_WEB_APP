# NILA Herbal Hair Oil - Booking Web App (Streamlit)
# To run this app: streamlit run nila_web_app.py

import streamlit as st
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(page_title="NILA Oil Booking", page_icon="🌿")

# Load and display product image
image = Image.open(r"C:\\Users\\Hello\\Downloads\\Nila_oil_bottle.png")  # Update path if needed
st.image(image, caption="NILA Herbal Hair Oil - 100ml", use_container_width=True)

# UI Layout
st.title("🌿 NILA Herbal Hair Oil")
st.subheader("Nurture Your Hair Naturally")

st.markdown("""
Welcome to our online booking assistant! Fill out the form below to place your order.
""")

# Booking Form
st.header("🛒 Place Your Order")

name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address (optional)")
address = st.text_area("Delivery Address")
quantity = st.selectbox("Select Quantity (100ml per bottle)", [1, 2, 3, 5, 10])
payment_method = st.radio("Payment Method", ["Cash on Delivery", "UPI Payment", "Bank Transfer"])

payment_screenshot = None
if payment_method == "UPI Payment":
    payment_screenshot = st.file_uploader("📎 Upload UPI Payment Screenshot (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Price calculation
price_per_100ml = 199
total_volume_ml = quantity * 100
total_price = quantity * price_per_100ml

st.markdown(f"💰 **Price per bottle (100ml): ₹{price_per_100ml}**")
st.markdown(f"🚞 **Total Volume:** {total_volume_ml}ml")
st.markdown(f"🧾 **Total Amount:** ₹{total_price}")

# Display UPI ID
st.markdown("**UPI ID for Payment:** `sugunasundarajothi@okhdfcbank`")

# Email sending function
def send_order_email(name, phone, email, address, quantity, total_volume_ml, total_price, payment_method):
    sender_email = "sugunasundarajothi@gmail.com"  # Replace with your Gmail address
    sender_password = "gwza aqdf smra pmgp"  # Replace with your generated app password
    receiver_email = "suguna.sundarajothi@outlook.com"

    subject = "New NILA Oil Order Received"
    body = f"""
    New order received:

    Name: {name}
    Phone: {phone}
    Email: {email if email else 'N/A'}
    Address: {address}
    Quantity: {quantity} bottle(s) ({total_volume_ml}ml)
    Total Price: ₹{total_price}
    Payment Method: {payment_method}
    """

    message = MIMEMultipart()
    message["From"] = sender_email
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
    if name and phone and address:
        if payment_method == "UPI Payment" and payment_screenshot is None:
            st.error("❗ Please upload a payment screenshot for UPI Payment.")
        else:
            send_order_email(name, phone, email, address, quantity, total_volume_ml, total_price, payment_method)
            st.success("✅ Your order has been placed successfully!")
            st.markdown(f"**Name:** {name}")
            st.markdown(f"**Phone:** {phone}")
            if email:
                st.markdown(f"**Email:** {email}")
            st.markdown(f"**Address:** {address}")
            st.markdown(f"**Quantity:** {quantity} bottle(s) ({total_volume_ml}ml)")
            st.markdown(f"**Total Price:** ₹{total_price}")
            st.markdown(f"**Payment Method Selected:** {payment_method}")
            if payment_screenshot:
                st.image(payment_screenshot, caption="Payment Screenshot", use_column_width=True)
            st.markdown("📦 Your order will be confirmed shortly via WhatsApp or call.")
    else:
        st.error("❗ Please fill all required fields to place an order.")

# Footer
st.markdown("---")
st.markdown("📧 Contact us at: suguna.sundarajothi@outlook.com | 📍 Coimbatore, India")
st.markdown("📸 Follow us on [Instagram](https://instagram.com/nila_herbal_hairoil)")
st.markdown("📸 Any problem [Instagram](https://instagram.com/queen_of_hills_queenpapa)")
st.markdown("📞 For inquiries, call us at: +91 8344923310")
st.markdown("🌿 Experience the power of nature with NILA Herbal Hair Oil!")
