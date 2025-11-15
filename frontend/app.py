# frontend/app.py
import streamlit as st
import requests
from typing import List, Dict

st.set_page_config(page_title="Hotel Booking System", layout="wide")
st.title("🏨 Hotel Booking System (Microservices)")

# service base URLs
AUTH_URL = "http://localhost:8001"
HOTEL_URL = "http://localhost:8002"
BOOKING_URL = "http://localhost:8003"

# simple session storage for user
if "user" not in st.session_state:
    st.session_state["user"] = None
if "token" not in st.session_state:
    st.session_state["token"] = None

menu = st.sidebar.selectbox("Menu", ["Home", "Login", "Browse Hotels", "My Bookings", "Health"])

# Home
if menu == "Home":
    st.subheader("Welcome to the Hotel Booking Demo")
    st.write("This demo uses three simple microservices (auth, hotel catalog, bookings) and a Streamlit frontend.")
    st.info("Start by logging in from the sidebar.")

# Login
elif menu == "Login":
    st.subheader("Login (prototype)")
    email = st.text_input("Email", value="demo@example.com")
    if st.button("Login"):
        try:
            r = requests.post(f"{AUTH_URL}/login", json={"email": email}, timeout=3)
            r.raise_for_status()
            data = r.json()
            st.session_state["user"] = data.get("user")
            st.session_state["token"] = data.get("token")
            st.success(f"Logged in as {st.session_state['user']['email']}")
        except Exception as e:
            st.error("Login failed. Is auth-service running?")
            st.exception(e)

# Browse Hotels
elif menu == "Browse Hotels":
    st.subheader("Available Hotels")
    try:
        r = requests.get(f"{HOTEL_URL}/hotels", timeout=3)
        r.raise_for_status()
        hotels: List[Dict] = r.json()
        for h in hotels:
            with st.container():
                cols = st.columns([3,1])
                with cols[0]:
                    st.markdown(f"### {h['name']}  —  {h['location']}")
                    st.write(f"**Price per night:** ${h['price']} — **Rating:** {h['rating']}")
                    if st.button("Show rooms", key=f"rooms-{h['id']}"):
                        # show rooms for this hotel (call hotel service)
                        rr = requests.get(f"{HOTEL_URL}/hotels/{h['id']}/rooms", timeout=3)
                        if rr.ok:
                            rooms = rr.json()
                            for rroom in rooms:
                                st.write(f"- Room {rroom['id']}: {rroom['room_type']} — ${rroom['price']}")
                with cols[1]:
                    st.write("")
                    st.write("")
                    st.write("")
                    if st.button("Book this hotel", key=f"bookhotel-{h['id']}"):
                        if st.session_state.get("user") is None:
                            st.warning("Please login first from the Login page.")
                        else:
                            st.session_state["selected_hotel"] = h
                            st.session_state["selected_hotel_id"] = h["id"]
                            st.experimental_rerun()
        # if user selected a hotel, show booking form
        if st.session_state.get("selected_hotel"):
            st.markdown("---")
            st.subheader("Booking Form")
            sel = st.session_state["selected_hotel"]
            st.write(f"Booking for **{sel['name']}**")
            room_id = st.number_input("Room ID", min_value=1, step=1, value=1)
            start_date = st.date_input("Start date")
            end_date = st.date_input("End date")
            if st.button("Confirm Booking"):
                payload = {
                    "user_id": st.session_state["user"]["id"],
                    "hotel_id": sel["id"],
                    "room_id": int(room_id),
                    "start_date": str(start_date),
                    "end_date": str(end_date)
                }
                try:
                    br = requests.post(f"{BOOKING_URL}/bookings", json=payload, timeout=3)
                    br.raise_for_status()
                    st.success(f"Booking created (id={br.json()['id']})")
                    # clear selected hotel
                    st.session_state.pop("selected_hotel", None)
                except Exception as e:
                    st.error("Booking failed. Is booking-service running?")
                    st.exception(e)
    except Exception as e:
        st.error("Failed to load hotels. Is hotel-service running?")
        st.exception(e)

# My Bookings
elif menu == "My Bookings":
    st.subheader("My Bookings")
    if st.session_state.get("user") is None:
        st.info("Please login first on the Login page.")
    else:
        try:
            r = requests.get(f"{BOOKING_URL}/bookings", timeout=3)
            r.raise_for_status()
            bookings = r.json()
            my = [b for b in bookings if b["user_id"] == st.session_state["user"]["id"]]
            if not my:
                st.info("No bookings yet.")
            else:
                for b in my:
                    st.write(f"Booking #{b['id']}: hotel_id={b['hotel_id']}, room_id={b['room_id']}, {b['start_date']} → {b['end_date']}")
        except Exception as e:
            st.error("Could not fetch bookings. Is booking-service running?")
            st.exception(e)

# Health (quick diagnostics)
elif menu == "Health":
    st.subheader("Service Health")
    services = {
        "Auth": f"{AUTH_URL}/health",
        "Hotel": f"{HOTEL_URL}/health",
        "Booking": f"{BOOKING_URL}/health"
    }
    for name, url in services.items():
        try:
            r = requests.get(url, timeout=2)
            if r.ok:
                st.success(f"{name} OK")
            else:
                st.error(f"{name} returned {r.status_code}")
        except Exception as e:
            st.error(f"{name} not reachable")
