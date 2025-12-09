import requests, time
from relay import control_relay
from temprature import mesure_humidity_and_temp
from soil import measure_moisture
from water_level import is_water_at_bottom
from config import TOKEN, ALLOWED_USERS, DEBUG, proxies


BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
s1, s2, s3, s4 = 0, 0, 0, 0 # Rele states


def keyboard():
    return {
    "keyboard": [
        [{"text": "🟢 rele 1" if s1 else "🔴 rele 1"}, {"text": "🟢 rele 2" if s2 else "🔴 rele 2"}],
        [{"text": "Havo harorati"}, {"text": "Tuproq namligi"}],
        [{"text": "Suv sathi"}]
    ],
    "resize_keyboard": True
}

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    response = requests.post(f"{BASE_URL}/sendMessage", json=data, proxies = proxies)
    if response.status_code != 200 and DEBUG:
        print("Failed to send message:", response.text)

def handle_message(message):
    global s1, s2
    chat_id = message["chat"]["id"]
    if chat_id not in ALLOWED_USERS:
        return
    
    text : str = message.get("text", "")
    if DEBUG:
        print(f"Received message from {chat_id}: {text}")  # Debug

    if text.startswith("/start"):
        send_message(chat_id, "Welcome! Choose an option:", reply_markup=keyboard())

    elif text == "🟢 rele 1" and s1 == 1:
        control_relay(11, 0)
        s1 = 0
        send_message(chat_id, "Rele 1 o'chirildi", reply_markup=keyboard())
    elif text == "🔴 rele 1" and s1 == 0:
        control_relay(11, 1)
        s1 = 1
        send_message(chat_id, "Rele 1 yoqildi", reply_markup=keyboard())

    elif text == "🟢 rele 2" and s2 == 1:
        control_relay(13, 0)
        s2 = 0
        send_message(chat_id, "Rele 2 o'chirildi", reply_markup=keyboard())

    elif text == "🔴 rele 2" and s2 == 0:
        control_relay(13, 1)
        s2 = 1
        send_message(chat_id, "Rele 2 yoqildi", reply_markup=keyboard())
    
    elif text == "Havo harorati":
        humidity, temperature = mesure_humidity_and_temp()
        send_message(chat_id, f"🌡 Harorat: {temperature:.1f}°C   \n💧 Namlik: {humidity:.1f}%", reply_markup=keyboard())

    elif text == "Tuproq namligi":
        moisture, norm, raw, voltage = measure_moisture()
        send_message(chat_id, f"Namlik: {moisture}%  \nNormalized: {norm}  \nRaw: {raw}  \nVolt: {voltage:.4f}", 
                     reply_markup=keyboard())

    elif text == "Suv sathi":
        if is_water_at_bottom():
            send_message(chat_id, "Suv bor",
                         reply_markup=keyboard())
        else:
            send_message(chat_id, "Suv yo'q", 
                         reply_markup=keyboard())
    


def main():
    print("Bot started...")
    offset = 0

    # Fetch latest update to skip old messages
    try:
        resp = requests.get(f"{BASE_URL}/getUpdates", params={"timeout": 1}, proxies=proxies)
        data = resp.json()
        if "result" in data and len(data["result"]) > 0:
            last_update_id = data["result"][-1]["update_id"]
            offset = last_update_id + 1
            print(f"Skipping old messages, starting with offset {offset}")
    except Exception as e:
        print("Error fetching latest update:", e)

    while True:
        try:
            resp = requests.get(f"{BASE_URL}/getUpdates", params={"timeout": 100, "offset": offset}, proxies=proxies)
            data = resp.json()

            for result in data.get("result", []):
                if "message" in result:
                    offset = result["update_id"] + 1  # Move offset forward
                    handle_message(result["message"])

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()