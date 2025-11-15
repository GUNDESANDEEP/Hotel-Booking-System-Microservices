# app.py (FRONTEND FIXED FOR MICROSERVICES)

import streamlit as st
import requests

# --------------------------
# CONFIG
# --------------------------
st.set_page_config(page_title="Hotel Booking System", layout="wide")

# Correct Microservices URLs
HOTEL_API = "http://localhost:8001"
BOOKING_API = "http://localhost:8003"
AUTH_API = "http://localhost:8002"


# --------------------------
# HOME PAGE
# --------------------------
def home():
    st.title("🏨 Hotel Booking System (Microservices)")

    st.write("Welcome to the hotel booking system powered by microservices!")

    menu = ["Search Hotels", "Book Room", "View Booking", "Admin – Add Hotel"]
    choice = st.selectbox("Select a service:", menu)

    if choice == "Search Hotels":
        search_hotels()

    elif choice == "Book Room":
        book_room()

    elif choice == "View Booking":
        view_booking()

    elif choice == "Admin – Add Hotel":
        admin_add_hotel()


# --------------------------
# FEATURE 1 – SEARCH HOTELS
# --------------------------
def search_hotels():
    st.subheader("🔍 Search Hotels")

    city = st.text_input("Enter city name")

    if st.button("Search"):
        try:
            response = requests.get(f"{HOTEL_API}/hotels/search?city={city}")

            if response.status_code != 200:
                st.error("Backend error while fetching hotels")
                return

            data = response.json()

            if len(data) == 0:
                st.warning("No hotels found.")
            else:
                for h in data:
                    st.success(f"🏨 {h['name']} – ⭐ {h['rating']}")
                    st.write(f"📍 Location: {h['city']}")
                    st.write(f"💰 Price per Night: ₹{h['price']}")
                    st.write("---")

        except Exception as e:
            st.error(f"Backend error: {e}")


# --------------------------
# FEATURE 2 – BOOK ROOM
# --------------------------
def book_room():
    st.subheader("🛏️ Book Hotel Room")

    hotel_id = st.text_input("Hotel ID")
    user_name = st.text_input("Your Name")

    if st.button("Book"):
        payload = {"hotel_id": hotel_id, "user_name": user_name}

        try:
            response = requests.post(f"{BOOKING_API}/booking/book", json=payload)

            if response.status_code == 200:
                st.success("Room booked successfully!")
                st.json(response.json())
            else:
                st.error("Booking failed.")

        except Exception as e:
            st.error(f"Backend error: {e}")


# --------------------------
# FEATURE 3 – VIEW BOOKING
# --------------------------
def view_booking():
    st.subheader("📄 View Booking")

    booking_id = st.text_input("Enter Booking ID")

    if st.button("Get Details"):
        try:
            response = requests.get(f"{BOOKING_API}/booking/{booking_id}")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error("Booking not found.")
        except Exception as e:
            st.error(f"Backend error: {e}")


# --------------------------
# FEATURE 4 – ADMIN: ADD HOTEL
# --------------------------
def admin_add_hotel():
    st.subheader("⚙️ Admin – Add New Hotel")

    name = st.text_input("Hotel Name")
    city = st.text_input("City")
    rating = st.number_input("Rating", 1.0, 5.0)
    price = st.number_input("Price per Night")

    if st.button("Add Hotel"):
        payload = {
            "name": name,
            "city": city,
            "rating": rating,
            "price": price
        }

        try:
            response = requests.post(f"{HOTEL_API}/hotels/add", json=payload)

            if response.status_code == 200:
                st.success("Hotel added successfully!")
            else:
                st.error("Unable to add hotel.")

        except Exception as e:
            st.error(f"Backend error: {e}")


# --------------------------
# RUN APP
# --------------------------
home()
