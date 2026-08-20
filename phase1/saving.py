import cv2
image = cv2.imread("phase1/qrcode.png")

if image is not None:
    succ = cv2.imwrite("output.png", image)

    if succ:
        print("Image saved successfully.")
    else:
        print("Failed to save the image.")
else:
    print("Image not loaded successfully.")