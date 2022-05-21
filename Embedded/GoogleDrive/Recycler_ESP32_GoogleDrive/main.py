# Credits to Priyansh Shankhdhar for the origianl code

import cv2
import urllib.request
import numpy as np
import time
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from datetime import datetime

# Account: smart.recycler@gmail.com
# Password: ozxelq12

url = 'http://192.168.0.147/images'                 # URL Connection. Change IP accordingly
cv2.namedWindow("ESP32 Cam", cv2.WINDOW_AUTOSIZE)   # Window that will display ESP32 Images
gauth = GoogleAuth()                                # Google drive authentication
folder = "1N-FuOM1iyJ_UkIWBrwi6qNvDsuppHn9r"        # Drive folder where the images will be saved
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

while True:
    # Request and handle the image
    image = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(image.read()), dtype=np.uint8)
    frame = cv2.imdecode(imgnp, -1)

    # Display the image in the window
    cv2.imshow("ESP32 Cam", frame)

    # Wait 5 ms for a key event
    key = cv2.waitKey(5)

    # If key pressed if K than save image to the drive
    if key == ord('k'):
        # Set image name to current date and time
        name = time.strftime("%Y%m%d-%H%M%S")
        img = str(name) + '.png'
        cv2.imwrite(img, frame)
        # Create image file and upload to google drive folder
        f = drive.CreateFile({'parents': [{'id': folder}], 'title': img})
        f.SetContentFile(f'{name}.png')
        f.Upload()
        print("image uploaded as: " + img)

    # If Q key is pressed, exit, else continue
    if key == ord('q'):
        break
    else:
        continue

cv2.destroyAllWindows()
