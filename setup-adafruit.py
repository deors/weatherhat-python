import os
from time import sleep, strftime, localtime
from Adafruit_IO import Client, Feed, Dashboard, RequestError

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '<<KEY>>'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = '<<USERNAME>>'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create new feeds
aio.create_feed(Feed(name="Temperature"))
aio.create_feed(Feed(name="Relative Humidity"))
aio.create_feed(Feed(name="Pressure"))
aio.create_feed(Feed(name="Light"))
aio.create_feed(Feed(name="Wind Speed"))
aio.create_feed(Feed(name="Wind Direction"))
aio.create_feed(Feed(name="Rain"))

print("Feeds created!")

# Create new dashboard
dashboard = aio.create_dashboard(Dashboard(name="Weather Dashboard"))

print("Dashboard created!")

# Print dashboard URL
print("Find the dashboard at: " +
      "https://io.adafruit.com/{0}/dashboards/{1}".format(ADAFRUIT_IO_USERNAME,
                                                          dashboard.key))
