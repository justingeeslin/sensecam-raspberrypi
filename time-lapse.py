import os
import time
from datetime import datetime
from time import sleep
import picamera

WAIT_TIME = 10

home_directory = os.path.expanduser("~")

directory_name = "sensecam"

# Create the full path to the directory within the home directory
full_path = os.path.join(home_directory, directory_name)

# Check if the directory doesn't exist, then create it
if not os.path.exists(full_path):
    os.makedirs(full_path)
    print(f"Directory '{directory_name}' created successfully in '{home_directory}'.")

with picamera.PiCamera() as camera:
    # Set resolution to the maximum supported by the camera
    # camera.resolution = camera.MAX_RESOLUTION
    
    # Set exposure mode (options: 'auto', 'night', 'nightpreview', 'backlight', etc.)
    camera.exposure_mode = 'auto'
    
    # Adjust white balance (options: 'auto', 'sunlight', 'cloudy', 'shade', etc.)
    camera.awb_mode = 'auto'
    
    # Increase sharpness (0 to 100)
    camera.sharpness = 100
    
    # Increase contrast (-100 to 100)
    camera.contrast = 50
    
    # Increase saturation (-100 to 100)
    camera.saturation = 50
   
    camera.start_preview()
    try:
       for i, filename in enumerate(
               camera.capture_continuous( os.path.join(f'{home_directory}/{directory_name}/', 'photo{timestamp}.jpg') )):
           print("Photo captured:")
           print(filename)
           time.sleep(WAIT_TIME)
    finally:
       camera.stop_preview()
