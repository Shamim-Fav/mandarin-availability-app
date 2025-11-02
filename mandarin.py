# app.py
import streamlit as st
import pandas as pd
import requests
from datetime import timedelta
from io import BytesIO

API_URL = "https://www.mandarinoriental.com/api/v1/booking/check-room-availability"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Cookie": "YOUR_CURRENT_COOKIE_HERE",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

def fetch_availability(hotel_id, check_date):
    payload = {
        "hotelCode": str(hotel_id),
        "roomCodes": None,
        "roomName": None,
        "bedType": None,
        "rateCode": None,
        "adultGuestCount": "2",
        "childGuestCount": "0",
        "stayDateStart": check_date.strftime("%Y-%m-%d"),
        "stayDateEnd": (check_date + timedelta(days=1)).strftime("%Y-%m-%d"),
        "primaryLanguageId": "en"
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"HTTP {response.status_code} for hotel {hotel_id} on {check_date}")
        return None


def parse_response(hotel_id, check_date, data):
    if not data or not data.get("roomStays"):
        return []
    rows = []
    for room in data["roomStays"]:
        for rate in room.get("rates", []):
            rows.append({
                "Hotel Name": "Mandarin Oriental",  # Fixed value column
                "HotelID": hotel_id,
                "Date": check_date.strftime("%Y-%m-%d"),
                "RoomType": room.get("title"),
                "RoomCode": room.get("roomTypeCode"),
                "Total": rate.get("total"),
                "Taxes": rate.get("taxes"),
                "Fees": rate.get("fees"),
                "MaxGuests": room.get("maxGuests"),
                "ShortDescription": rate.get("shortDescription"),
                "LongDescription": rate.get("longDescription"),
                "Image": rate.get("image")
            })
    return rows


# 🏨 Streamlit UI
st.title("Hong Kong – Mandarin Oriental Availability Checker")
st.info("This app checks room availability for **Hong Kong – Mandarin Oriental** hotel (Hotel ID: 514).")

start_date = st.date_input("Select start date for checking availability")
num_days = st.number_input("How many days to check?", min_value=1, max_value=365, value=60)

if st.button("Start Checking"):
    hotel_id = 514  # Fixed hotel ID
    all_rows = []

    for day_offset in range(num_days):
        check_date = pd.to_datetime(start_date) + timedelta(days=day_offset)
        st.text(f"Checking Hong Kong – Mandarin Oriental for {check_date.strftime('%Y-%m-%d')}")
        data = fetch_availability(hotel_id, check_date)
        parsed_rows = parse_response(hotel_id, check_date, data)
        if parsed_rows:
            all_rows.extend(parsed_rows)

    if all_rows:
        result_df = pd.DataFrame(all_rows)
        buffer = BytesIO()
        result_df.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="Download Results Excel",
            data=buffer,
            file_name="hongkong_mandarin_oriental_availability.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No availability found.")
