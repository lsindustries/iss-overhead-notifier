import smtplib
import requests
from datetime import datetime
import time

#YOUR EMAIL
MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"
#YOUR POSITION
MY_LAT = 51.112477039404816 # Your latitude
MY_LONG = 20.853292156467184 # Your longitude
LAST_NOTIF = 0

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


def calc_pos():
    if 46.1124 <= iss_latitude <= 56 and 15.853 <= iss_longitude <= 25:
        return True
    else:
        return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


def once_a_day():
    #checks when the last notification was sent (only 1 notification by day
    now = str(datetime.now()).split(" ")
    if now[0] != LAST_NOTIF:
        return True
    else:
        return False

while True:
    if once_a_day():
        if calc_pos() and is_night():
            connection = smtplib.SMTP("smtp.server.your")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="to_addres_you_want@gmail.com",
                msg="Subject: Look Up! The ISS is coming!\n\nThe ISS is above you in the sky."
            )
            notif = time.strftime("%Y-%m-%d")
            LAST_NOTIF = notif

        time.sleep(60)
    else:
        time.sleep(3600)



