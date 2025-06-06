import streamlit as st
from PIL import Image
from db_utils import init_db, store_order
from email_utils import send_order_email

# Initialize DB
init_db()

# Set page config
st.set_page_config(page_title="NILA Products Booking", page_icon="🌿")

# App banner
st.image("NILA Herbal Banner.png", caption="Explore Our Herbal Collection 🌿", use_container_width=True)


# --- Product Data ---
products = {
    "NILA Herbal Hair Oil 100ml": {
        "price": 199,
        "image": "Nila_oil_bottle.png",
        "ingredients": "Hibiscus, Amla, Curry Leaves, Fenugreek, Neem, Almond, Aloe Vera, Bhringraj, Holy Basil, Indian Nettle",
        "benefits": "Reduces Hair Fall, Promotes Growth, Nourishes Scalp"
    },
    "NILA Herbal Hair Pack 50g": {
        "price": 99,
        "image": "Nila_hairpack.png",
        "ingredients": "Amla Powder, Hibiscus Powder, Neem Powder, Rose Petals",
        "benefits": "Cleanses Scalp, Controls Dandruff, Strengthens Roots"
    }
}

# --- Product Display ---
st.subheader("🌿 Our Products")
for product, details in products.items():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(details["image"], use_container_width=True)
    with col2:
        st.markdown(f"**{product}**")
        st.markdown(f"💰 Price: ₹{details['price']}")
        st.markdown(f"🌿 Ingredients: {details['ingredients']}")
        st.markdown(f"✨ Benefits: {details['benefits']}")
    st.divider()

# --- Cart Selection ---
st.subheader("🛒 Select Products")
selected_quantities = {}
total_price = 0

for product in products:
    qty = st.number_input(f"{product} - Quantity", 0, 10, key=product)
    if qty > 0:
        selected_quantities[product] = qty
        total_price += qty * products[product]['price']

if not selected_quantities:
    st.info("Please select at least one product to continue.")

# --- Delivery Form ---
st.subheader("📦Delivery Details")
name = st.text_input("Full Name *")
phone = st.text_input("Phone Number *")
email = st.text_input("Email Address (Optional)")
address = st.text_area("Delivery Address *")

payment_method = st.radio("Payment Method", ["Cash on Delivery", "UPI Payment"])
payment_screenshot = None

if payment_method == "UPI Payment":
    st.markdown("📎 UPI ID: `sugunasundarajothi@okhdfcbank`")
    payment_screenshot = st.file_uploader("Upload UPI Payment Screenshot (JPG/PNG)", type=["jpg", "jpeg", "png"])

# --- Order Summary ---
st.markdown(f"💰 **Total Amount:** ₹{total_price}")

# --- Place Order Logic ---
if st.button("✅ Place Order"):
    if not selected_quantities:
        st.error("Please add at least one product.")
    elif not (name and phone and address):
        st.error("All fields marked with * are required.")
    elif payment_method == "UPI Payment" and not payment_screenshot:
        st.error("Please upload a UPI screenshot.")
    else:
        # Prepare summary
        order_summary = ""
        for p, qty in selected_quantities.items():
            price = products[p]["price"]
            subtotal = qty * price
            order_summary += f"{p} x {qty} = ₹{subtotal}\n"

        # Save to DB
        store_order(name, phone, email, address, order_summary, total_price, payment_method)

        # Send confirmation email
        send_order_email(name, phone, email, address, order_summary, total_price, payment_method)

        # Show Success
        st.success("🎉 Order placed successfully!")
        st.markdown("### ✅ Order Summary")
        st.text(order_summary)
        st.markdown(f"**Name:** {name}")
        st.markdown(f"**Phone:** {phone}")
        st.markdown(f"**Address:** {address}")
        st.markdown(f"**Total Price:** ₹{total_price}")
        st.markdown(f"**Payment Method:** {payment_method}")
        if payment_screenshot:
            st.image(payment_screenshot, caption="Payment Screenshot", use_column_width=True)
        st.markdown("📦 You will be contacted shortly via WhatsApp or call.")

# --- Footer ---
st.divider()
st.markdown("---")
st.markdown("📸 Follow us on [Instagram](https://instagram.com/nila_herbal_hairoil)")
st.markdown("📸 Support [Instagram](https://instagram.com/queen_of_hills_queenpapa)")
st.markdown("📞 For inquiries, call us at: +91 8344987196")
st.markdown("🌿 Experience the power of nature with NILA Herbal Hair Oil!")
