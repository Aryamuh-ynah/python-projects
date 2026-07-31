from plyer import notification
import time
import os

ICON_PATH = "/home/humayra/Downloads/icon.png"

def send_notification():
    # Check if icon exists
    icon = ICON_PATH if os.path.exists(ICON_PATH) else None

    notification.notify(
        title="Take Rest",
        message="You have been working for 2 hours. Please take a break.",
        app_icon=icon,          # Can be None if icon doesn't exist
        timeout=10,
        app_name="Rest Reminder"
    )

if __name__ == "__main__":
    print("Notification reminder started... Press Ctrl+C to stop.")
    while True:
        send_notification()
        time.sleep(20)   # 20 seconds for testing (change to 7200 for 2 hours)