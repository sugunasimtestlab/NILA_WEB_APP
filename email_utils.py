import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st  # Add this import

# Use Streamlit secrets for email credentials
email_user = st.secrets["general"]["email_user"]
email_password = st.secrets["general"]["email_password"]

def send_order_email(name, phone, email, address, order_summary, total_price, payment_method):
    sender_email = email_user
    sender_password = email_password

    # Fallback if customer email not provided
    receiver_email = email if email else sender_email

    subject = "Thank you for your order - NILA Herbal"
    body = f"""
Hi {name},

Thank you for placing your order with NILA Herbal Hair Oil! 🌿

Here are your order details:

🧾 Order Summary:
{order_summary}

💵 Total Price: ₹{total_price}
💳 Payment Method: {payment_method}

📍 Delivery Details:
Name: {name}
Phone: {phone}
Address: {address}

We will contact you shortly to confirm delivery and share shipping updates.

Regards,
🌿 NILA Herbal Hair Oil Team
📞 +91 8344987196
Instagram: @nila_herbal_hairoil
"""

    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()
    except Exception as e:
        print(f"[ERROR] Email failed to send: {e}")
