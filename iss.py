from datetime import datetime
import requests
import smtplib

# Latitude and Longitude for New York. You can change it but putting your adress in latlong.net
MY_LAT = 40.712776
MY_LNG = -74.005974

# Use your email if you want to be informed when the ISS is above you
MY_EMAIL = "email@gmail.com"
MY_PASSWORD = "mypassword123"
SOME_EMAIL = "someemail@gmail.com"

# ISS API
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

# ISS Position
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}

# Sunset and sunrise API
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()

sunrise_hour = int(response.json()["results"]["sunrise"].split("T")[1].split(":")[0])
sunset_hour = int(response.json()["results"]["sunset"].split("T")[1].split(":")[0])

# Current time
hour_now = datetime.now().hour

print(f"Sunrise: {sunrise_hour}\nSunset: {sunset_hour}\nCurrent hour: {hour_now}")

# If the ISS is close to my current position
if abs(MY_LAT - iss_latitude) <= 5 and abs(MY_LNG - iss_longitude) <= 5:
    # And it is currently dark
    if sunset_hour <= hour_now <= sunrise_hour:
        # Then send me an email to tell me to look up.
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, SOME_EMAIL, "Subject: Hey\n\nLook up!")
        connection.close()
