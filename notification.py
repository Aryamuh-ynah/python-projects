from plyer import notification

import time

if __name__ == "__main__":
    while True:  
        notification.notify(
            title="Take Rest",
            message="You have been working for 2 hours. Please take a break.",
            app_icon="/home/humayra/Downloads/icon.png",
            timeout=10,
            )
        time.sleep(20)