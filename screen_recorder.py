# import cv2
# import pyautogui
# import numpy as np
# import time
# from win32api import GetSystemMetrics

# width = GetSystemMetrics(0)
# height = GetSystemMetrics(1)

# dim = (width, height)

# f = cv2.VideoWriter_fourcc(*'XVID', 20.0, dim)

# output = cv2.VideoWriter("test.mp4", f, 30,dim)

# now_time = time.time()

# dur = 10+4

# end_time = now_time + dur   # Duration of the recording in seconds

# while True:
#     img = pyautogui.screenshot()
#     frame = np.array(img)
#     frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output.write(frame2)
#     if time.time()>end_time:
#         break

# output.release()

# print("Recording finished. Video saved as test.mp4")


##################----Ubuntu----#################

import cv2
import numpy as np
import time
from mss import mss
# Screen size
with mss() as sct:
    monitor = sct.monitors[1]  # Primary monitor
    width = monitor["width"]
    height = monitor["height"]

dim = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter("/home/humayra/test.mp4", fourcc, 20.0, dim)
duration = 10  # seconds
end_time = time.time() + duration
print("Recording started...")
with mss() as sct:
    while time.time() < end_time:
        # Capture screen
        img = sct.grab(monitor)       
        # Convert to numpy array (BGRA → BGR)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)        
        output.write(frame)

output.release()
print("Recording finished → test.mp4")