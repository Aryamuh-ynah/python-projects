import cv2
import pyautogui
import numpy as np
import time
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

dim = (width, height)

f = cv2.VideoWriter_fourcc(*'XVID', 20.0, dim)

output = cv2.VideoWriter("test.mp4", f, 30,dim)

now_time = time.time()

dur = 10+4

end_time = now_time + dur   # Duration of the recording in seconds

while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output.write(frame2)
    if time.time()>end_time:
        break

output.release()

print("Recording finished. Video saved as test.mp4")