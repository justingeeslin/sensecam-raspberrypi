import io
import os
import time
import picamera
from PIL import Image
import zbarlight
from urllib.parse import urlparse
import csv
print("Running SenseCam Script..")
WAIT_TIME = 1

home_directory = os.path.expanduser("~")

directory_name = "sensecam"

# Create a stream to capture images
stream = io.BytesIO()

# Create the full path to the directory within the home directory
full_path = os.path.join(home_directory, directory_name)

# Check if the directory doesn't exist, then create it
if not os.path.exists(full_path):
    os.makedirs(full_path)
    print(f"Directory '{directory_name}' created successfully in '{home_directory}'.")
    
print("About to open the camera")

with picamera.PiCamera() as camera:
    # Set resolution to the maximum supported by the camera
    camera.resolution = camera.MAX_RESOLUTION
    
    # Set exposure mode (options: 'auto', 'night', 'nightpreview', 'backlight', etc.)
    camera.exposure_mode = 'auto'
    
    # Adjust white balance (options: 'auto', 'sunlight', 'cloudy', 'shade', etc.)
    camera.awb_mode = 'auto'
    
    # Increase sharpness (0 to 100)
    # camera.sharpness = 50
    
    # Increase contrast (-100 to 100)
    # camera.contrast = 0
    
    # Increase saturation (-100 to 100)
    # camera.saturation = 0
   
    camera.start_preview()
    
    # Create a CSV file to write URLs and timestamps
    with open('qr_urls.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'URL'])
    
        try:
           for i, _ in enumerate(camera.capture_continuous(stream, format='jpeg')):
               # print("Photo captured:")
               # print(filename)
               
               # Rewind the stream to the beginning
               stream.seek(0)
               
               # Open the image from the stream
               with Image.open(stream) as img:
                   # Rotate the image 90 degrees
                   rotated_img = img.rotate(90)
                   
                   timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                   
                   # Scan the rotated image for a QR code
                   qr_code = zbarlight.scan_codes('qrcode', rotated_img)
                   if qr_code is not None:
                       print("Saw a QR code")
                       # Decode the QR code bytes to a string
                       qr_data = qr_code[0].decode('utf-8')
                       
                       # Check if the decoded data is a URL
                       if qr_data.startswith('http://') or qr_data.startswith('https://'):
                           # Parse the URL to get its components
                           parsed_url = urlparse(qr_data)

                           
                           # Write the timestamp and URL to the CSV file
                           writer.writerow([timestamp, qr_data])
                           
                           print(f'QR code URL: {qr_data}')
                       else:
                           print(f'QR code data: {qr_data}')
                   
                   # Save the rotated image to the specified directory
                   print("Saved a photo")
                   rotated_img.save(os.path.join(f'{home_directory}/{directory_name}/', f'photo{timestamp}.jpg') )
               
               # Reset the stream for the next capture
               stream.seek(0)
               stream.truncate()
               
               time.sleep(WAIT_TIME)
        finally:
           camera.stop_preview()
