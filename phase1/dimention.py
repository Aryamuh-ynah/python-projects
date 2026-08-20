import cv2
image = cv2.imread("phase1/qrcode.png")

if image is not None:
    h, w, c = image.shape
    print(f"Image dimensions: Height={h}, Width={w}, Channels={c}")

else:
    print("Image not loaded successfully.") 