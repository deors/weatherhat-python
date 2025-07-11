
import os
from time import sleep, strftime, localtime
import weatherhat
from Adafruit_IO import Client, Feed, Dashboard, RequestError

sensor = weatherhat.WeatherHAT()

print(f"""
Weather Hat station integrated with adafruit.io
-----------------------------------------------""")

print("Run starting at: " + strftime('%Y-%m-%d %H:%M:%S %Z', localtime()))

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '<<KEY>>'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = '<<USERNAME>>'

# We can compensate for the heat of the Pi and other environmental conditions using a simple offset.
# Change this number to adjust temperature compensation!
OFFSET = -15

try:
    # Create an instance of the REST client.
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Connect with data feeds
    temperature_feed = aio.feeds('temperature')
    humidity_feed = aio.feeds('relative-humidity')
    pressure_feed = aio.feeds('pressure')
    light_feed = aio.feeds('light')
    windspeed_feed = aio.feeds('wind-speed')
    winddirection_feed = aio.feeds('wind-direction')
    rain_feed = aio.feeds('rain')
except Exception:
    print("Error initializing feeds at adafruit.io")
    os._exit(1)

# Read the BME280 and discard the initial nonsense readings
sensor.update(interval=10.0)
sensor.temperature_offset = OFFSET
temperature = sensor.temperature
humidity = sensor.relative_humidity
pressure = sensor.pressure
print("Discarding the first few BME280 readings...")
sleep(10.0)

# Read all the sensors and start sending data
print("Reading data every 30 seconds and publishing it to adafruit.io...")

while True:
    print("Collecting data at: " + strftime('%Y-%m-%d %H:%M:%S %Z', localtime()))

    try:
        sensor.update(interval=30.0)

        wind_direction_cardinal = sensor.degrees_to_cardinal(sensor.wind_direction)

        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        pressure = sensor.pressure
        light = sensor.lux
        windspeed = sensor.wind_speed
        winddirection = wind_direction_cardinal
        rain = sensor.rain_total

        aio.send_data(temperature_feed.key, temperature)
        aio.send_data(humidity_feed.key, humidity)
        aio.send_data(pressure_feed.key, pressure)
        aio.send_data(light_feed.key, light)
        aio.send_data(windspeed_feed.key, windspeed)
        aio.send_data(winddirection_feed.key, winddirection)
        aio.send_data(rain_feed.key, rain)
        print("Data sent to adafruit.io: " + strftime('%Y-%m-%d %H:%M:%S %Z', localtime())
            + " // temp: {:.2f} // hum: {:.2f} // press: {:.2f} // light: {:.0f} // wind spd: {:.2f} // wind dir: {} // rain: {:.2f}".format(temperature, humidity, pressure, light, windspeed, winddirection, rain))
    except Exception:
        print("Error sending data to adafruit.io")
        os._exit(1)

    # Wait for next data point -- aligned with update interval
    sleep(30.0)
