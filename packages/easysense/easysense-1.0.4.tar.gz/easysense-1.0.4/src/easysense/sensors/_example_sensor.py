# This is a example code for how you implement a new sensor
# Make sure to name your file exactly like the sensor name + '_sensor'
# (e.g. The sensor is named 'BME280', then call your file 'bme280_sensor.py')

# If your sensor needs additional files, like a config file put them in a folder named as the sensor
# (e.g. The sensor is named 'BME280', then name the folder 'bme280')

# Also make sure to define everything inside the Easysense class
# If you need to initialise something, do it in the __init__() of Easysense
# (Note: All files fith leading "_" will be ignored)

# Install build-in modules normally, for modules that need to be installed via pip see __init__()
from src.easysense import Easysense


# create a class that inherits from Easysense
class Example(Easysense):

    def __init__(self):
        # !!! Import modules that need to be installed via pip / are not build-in here
        Easysense.install_dependency("numpy")
        import numpy as np
        # put everything in here you need to initialize or that have to be called once before start
        self.my_sensor = np.random.randint

    def give_data(self):
        # Implement the actual sensor reading logic here
        value = self.my_sensor(0, 10)
        return {"Number": value}  # return the data as dict with key, value pairs (key is the name displayed in Wiresense chart)
